#!/usr/bin/env python3

import requests
import frontmatter
import os
import json
import glob
from requests_html import HTML

issues_url = "https://api.bitbucket.org/2.0/repositories/sdqali/sdqali.in-comments/issues"
entries = []
username = os.environ['BB_USER']
password = os.environ['BB_PASSWD']

for entry in glob.iglob("dist/blog/20**/**/*.html", recursive=True):
    with open(entry) as ef:
        contents = ef.read()
        html = HTML(html=contents)

        title = html.xpath("//title")[0].text.replace(' - {code that works} by Sadique Ali', '')
        if "http" in title:
            continue

        permalink = html.xpath("//meta[@name='hugo:permalink']")[0].attrs['content']
        filepath = html.xpath("//meta[@name='hugo:filepath']")[0].attrs['content']

        modified_post = None
        with open(filepath, "r") as f:
            post = frontmatter.load(f)

            payload = {'title': title, 'content': {'raw': f"Comment for [{title}]({permalink})", 'markup': 'markdown'}}
            headers = {'Content-Type': 'application/json'}
            if post.get('bbcommentid') is not None:
                continue

            resp = requests.post(issues_url, auth=(username, password), data=json.dumps(payload), headers=headers)

            print(resp.text)
            post['bbcommentid'] = json.loads(resp.text)['id']
            modified_post = frontmatter.dumps(post)


        with open(filepath, "w") as f:
            f.write(modified_post)

