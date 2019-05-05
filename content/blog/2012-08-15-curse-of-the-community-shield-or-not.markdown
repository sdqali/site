---
categories:
- football
- data
- visualisation
- d3.js
comments: true
date: 2012-08-15
ghcommentid: 47
image: /images/threaded-blue-on-black-cropped.jpg
keywords: null
tags:
- football
- data
- visualisation
- d3.js
title: Curse of the Community Shield?
---

Click on the image to see the visualisation:
[![Community Shield visualisation](/images/community_shield.png "Community Shield Visualisation")](/visualizations/community_shield/index.html)

## Context
The football season in Europe began this weekend with countries hosting
their equivalents of the *Super Cup*. For those confused as to what a
super cup, the
[Wikipedia entry](http://en.wikipedia.org/wiki/Super_cup) is a good
starting point. Super cups, at least in European national
leagues are curtain-raisers for the season.

The FA [Community Shield](http://en.wikipedia.org/wiki/FA_Community_Shield)
is England's Super Cup and it pits the winners of the FA Cup against the
winners of the Premier League from the previous season. This year's game saw Manchester City
beat Chelsea.

Winning the Community Shield at the beginning of the
season is considered a bad omen by a lot of football fans - an indicator that the team who win it
would not win the subsequent league season. This supposed curse is
widely discussed in
[fan forums](http://www.redcafe.net/f6/curse-community-shield-165424/)
and
[blog posts](http://www.guardian.co.uk/football/2005/jan/26/theknowledge.sport). And
what would be complete on the Internet without a [dinosaur thinking
aloud](http://9gag.com/gag/5030472) about it?

<!--more-->

A Community Shield win has the
potential to positively influence how a football team performs in the
season. People love winning and a victory against an opposition that
beat them to win another trophy last season should act as a confidence
booster. But does this happen? What correlation exists between winning a
Super Cup and the team's performance in the subsequent season?

I wanted to see this and decided to create this visualisation. It shows
teams that won the Community Shield since 1908 and their position in the
table for the ensuing season.

The visualisation is [here](/visualizations/community_shield/index.html).

## Winners
If you observe the visualisation, there are a lot of seasons for which
there are no winners. These seasons fall in to two sets. The first set
signify the time period when the world wars meant there was no
Football. The second set is more interesting in that invitation teams
won the Community Shield and since these teams don't compete in the
League, they are absent from the visualisation. The invitation
teams to have won the Community Shield are *English Professionals XI*,
*English Amateurs XI* and *English World Cup XI*.

There are also some seasons when there are two winners shown on the
visualisation. This is due to the fact that until early 1990s, a draw in
a Community Shield match meant that the teams shared the trophy.

## Obervations
* Until the 1970s, winners of the Community Shield did not do well in
  the league.
* From 1908 to 1970, only 6 teams went on to win the league after
  winning the curtain raiser.
* The lowest point belongs Manchester City, who won the league in the
  1936/37 season and the Community Shield in 1937 and then went on to
  get relegated.
* Since the 1970s winners of Community Shield had better performances in
  the league.
* This trend was first set by the all conquering Merseyside teams of the
  1970s and 1980s.
* Between 1970 and 1990, 6 teams went on to win the league after winning
  Community  Shield.
* Manchester United set a similar trend in the early 2000s.
* After 1970s, the winners of Community Shield have done well. Winners
  finished 6th or better in all seasons since 1970, except for 5 times.

Looks like winning the Community Shield no longer incur a curse on the winners.

## Code
The data was pulled from Wikipedia and cleaned up using Excel. The
visualisation was created using [d3.js](http://d3js.org).

As always, the code and data used for this project is available on
[Github](https://github.com/sdqali/community_shield). I would greatly appreciate
feedback on this.