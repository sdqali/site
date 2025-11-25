---
title: Using GitHub and Bitbucket issues for comments on Static sites
date: 2025-11-24T11:49:27-08:00
tags:
- hugo
- github
- bitbucket
- codeberg
ghissueid: 151
bbissueid: 144
---
One thing that statically generated sites like this typically lack is a commenting system. There are solutions like Disqus that you can embed, but then the commenter will need to create an account there, and you now have one more dependency. Sometimes, that is a perfectly reasonable approach.

I came up with an approach [^1] that uses GitHub issues and Bitbucket issues to host comments.
Since this site is hosted on GitHub, and most people who would leave a comment on this site have a GitHub account, it doesn't feel like another account to sign up for. And for those who don't have a GitHub account, the approach supports Bitbucket as well.

## First Iteration

The easiest approach would be:
1. When publishing a new entry that accepts comments, a GitHub issue is created that links to the entry. A Bitbucket issue is also created, linking back to the entry.
2. Each entry links to the GitHub and Bitbucket issue, as the place to leave comments.

This has the glaring shortcoming that readers will need to open two separate pages to read comments, and comments from GitHub users aren't visible to Bitbucket users, and _vice versa_.

## Second Iteration

Both Bitbucket and GitHub offer public APIs that can fetch an Issue and the Comments on the Issue. This makes it possible for each entry to fetch the Comments from both sources, inter-leave them based on timestamps and render them directly on the page.

```javascript
document.addEventListener('DOMContentLoaded', function () {
  var renderComments = function(comments) {
    comments.sort(function(first, second) {
      return first.createdAt - second.createdAt;
    });

    var commentsList = document.getElementById('gh-comments-list');
    comments.forEach(function(comment) {
      var t = `
        <div class='gh-comment'>
          <div class='gh-comment-header'>
            <img src='${comment.user.avatarUrl}' width='24px'>
            <b><a href='${comment.user.profileUrl}'>${comment.user.username}</a></b>
            posted via ${comment.channel} at
            <em>${comment.createdAt.toUTCString()}</em>
          </div>
          <div id='gh-comment-hr'></div>
          ${comment.body}
        </div>
      `;
      commentsList.insertAdjacentHTML('beforeend', t);
    });
  };

  var fetchBbComments = function() {
    if (typeof bbUrl === 'undefined' || bbUrl === null) {
      return Promise.resolve([]);
    }
    return fetch(bbApiUrl, {
      headers: {"Content-Type": "application/json"}
    })
    .then(function(response) {
      if (!response.ok) throw new Error('Network response was not ok');
      return response.json();
    })
    .then(function(bbComments) {
      return bbComments.values.map(function(comment) {
        return {
          createdAt: new Date(comment.created_on),
          user: {
            avatarUrl: comment.user.links.avatar.href,
            profileUrl: comment.user.links.html.href,
            username: comment.user.nickname
          },
          body: comment.content.html,
          channel: "Bitbucket"
        };
      });
    })
    .catch(function() {
      return [];
    });
  };

  var fetchGhComments = function() {
    if (typeof ghUrl === 'undefined' || ghUrl === null) {
      return Promise.resolve([]);
    }
    return fetch(ghApiUrl, {
      headers: {Accept: "application/vnd.github.v3.html+json"}
    })
    .then(function(response) {
      if (!response.ok) throw new Error('Network response was not ok');
      return response.json();
    })
    .then(function(ghComments) {
      return ghComments.map(function(comment) {
        return {
          createdAt: new Date(comment.created_at),
          user: {
            avatarUrl: comment.user.avatar_url,
            profileUrl: comment.user.html_url,
            username: comment.user.login
          },
          body: comment.body_html,
          channel: "GitHub"
        };
      });
    })
    .catch(function() {
      return [];
    });
  };

  Promise.all([fetchGhComments(), fetchBbComments()]).then(function(results) {
    var allComments = results[0].concat(results[1]);
    renderComments(allComments);
  });
});

```

All that is left is to provide unique issue links to each entry. This could be achieved with a combination of config and front-matter on each of the entries. Since this site is generated using Hugo, I have the following in `config.yaml`:

```yaml
params:
  ghCommentsRepo: "sdqali/site"
  bbCommentsRepo: "sdqali/sadique.io-comments"
```

And in the front-matter of each page:

```
ghcommentId: 150
bbissueid: 143
```

A Hugo partial then uses these parameters to set up the JS in each page:

```go
// layouts/_partials/comments.snippet.html

{{ if isset .Params "ghissueid" }}
var ghUrl = "https://github.com/{{ .Site.Params.ghCommentsRepo }}/issues/{{ .Params.ghissueid }}";
var ghApiUrl = "https://api.github.com/repos/{{ .Site.Params.ghCommentsRepo }}/issues/{{ .Params.ghissueid }}/comments";

$("#gh-comments-list").append("<a class='issues-link'href='" + ghUrl + "'  target='_blank'>Comment via <span class='icon-github'/></a>");
{{ end }}

{{ if isset .Params "bbissueid" }}
var bbUrl = "https://bitbucket.org/{{ .Site.Params.bbCommentsRepo }}/issues/{{ .Params.bbissueid }}/"
var bbApiUrl = "https://api.bitbucket.org/2.0/repositories/{{ .Site.Params.bbCommentsRepo }}/issues/{{ .Params.bbissueid }}/comments";

$("#gh-comments-list").append("<a class='issues-link'href='" + bbUrl + "'  target='_blank'>Comment via <span class='icon-bitbucket'/></a>");
{{ end }}

// Rest of the JS
```

With this [GitHub issue](https://github.com/sdqali/site/issues/150) and this [Bitbucket issue](https://bitbucket.org/sdqali/sadique.io-comments/issues/143/example), this will render:

![Comments](/images/comments.png)

The front-matter parameters being `ghissueid` and `bbissueid` instead of `ghIssueId` and `bbIssueId` is down to a quirk of the Hugo templating system [^2]. Your static site generator may not have this issue.

## Nice to Haves
 - With the rising popularity of Codeberg, it is worth adding support for commenting via Codeberg - they have a similar API to retrieve comments on an issue [^3].
 - Issues are created for new entries manually. That gets old [^4], so it would be nice to create Issues via the script used to publish this site - [`publish.sh`](https://github.com/sdqali/site/blob/main/publish.sh).




[^1]: The [original version](https://github.com/sdqali/site/commit/0f5aa21f38a8d8274656a46bcc44ce4a04b09e93#diff-eb261796c12a10bc5993c763ce2923dfe48aa14d9cf9b66187aeddceda10bf56) was implemented in 2019, and I am sure there are others who came up with similar approaches.
[^2]: "Always have the front-matter keys in all-lowercase." - [Hugo Forum](https://discourse.gohugo.io/t/arent-all-front-matter-parameters-lower-cased-internally/11050).
[^3]: Forgejo [issue/issueGetComments](https://codeberg.org/api/swagger#/issue/issueGetComments)
[^4]: Or so, I assume, even though I didn't publish a single new entry between 2019 and this week.
