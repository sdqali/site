---
aliases:
- /blog/2012/07/21/visualization-how-european-clubs-dominate-their-leagues
categories:
- football
- visualisation
- data
- d3.js
- code
comments: true
date: 2012-07-21
ghcommentid: 44
image: /images/threaded-blue-on-black-cropped.jpg
tags:
- football
- visualisation
- data
- d3.js
- code
title: Visualisation - How European clubs dominate their leagues
---

*Click [here](/visualizations/league_champions/index.html) to see the visualisation.*

This is a visualization showing how various European football clubs have
dominated their respective national leagues over various time
periods. The visualization shows data for England, France, Germany,
Italy, Netherlands and Spain.

The visualization is self-explanatory. You can choose a league to view
from the dropdown and then choose the sliders to select an era for which you want to look
at the data. For fine adjustment, after clicking on either slider, you
can use your keyboard to select a time period.

## Interesting Trends
* [Athletic Bilabo](http://en.wikipedia.org/wiki/Athletic_Bilbao) was very dominant in Spain during the first 20 years
  of the La Liga from 1930 to 1950. However, throughout the rest of the
  time period, FC Barcelona and Real Madrid CF have absolutely dominated
  La Liga.
* [Torino](http://en.wikipedia.org/wiki/Torino_F.C.) dominated Italian
  football in the 1940's, winning 5 league titles.
* Except for the period between 2002 and 2008, French Ligue 1 had a lot
  of variety in terms of League champions.
* [Borussia Mönchengladbach](https://en.wikipedia.org/wiki/Borussia_M%C3%B6nchengladbach)
  had a golden period in the 1970's, winning 5 titles. They have never
  won the Bundesliga in any other decade. While it would appear that
  Bayern Munich totally dominates German football, they won exactly 1
  title in the 40 years between 1927 and 1967.
* Regardless of the era, Ajax has dominated Dutch football.
* For the 30 year period between 1962 and 1992, the English league
  invariable went to Merseyside. Liverpool won 13 and Everton won 4.

## Motivation
I happened to read this
[brilliant piece](http://frenchfootballweekly.com/2012/07/13/paris-saint-germain-forget-the-fans-its-all-about-winning/)
from French Football Weekly on how Paris Saint-Germain's and their
Qatari owners' desire to buy their way in to success may not be in the
best interest of the French game. Among other things, the author points
out that the last five years have shown that anybody can mount a title
challenge and this kind of diversity in contenders for the title is
unique in Europe. That was an Aha! moment. While the list of French
champions for the last five years reads "Lyon, Bordeaux, Marseille,
Lille, Montpellier", few would have forgotten how Lyon won 7 consecutive
titles from the 2001-2002 season to 2007-2008 season.

This kept me thinking about during certain time periods, certain teams
tend to dominate their leagues to a great extend. Other illustrious
examples similar to Lyon include Manchester United in the 1990s,
Liverpool in the 1970s and 80s, Torino in the 1940s and Borussia
Mönchengladbach in 1970s. I decided to create the above visualization to
make sense of this trend.

## Exaplanation
This is a [Treemap](http://en.wikipedia.org/wiki/Treemapping). A treemap
recursively divides area to in to rectangles, and the area of any node
is proportional to it's value. This is a treemap of depth `2`, where the
relationship is essentially `Club -> Championship Years`. You can see a
more comprehensive example of a Treemap visualization with more depth [here](http://mbostock.github.com/d3/ex/treemap.html).

## Code
All the data was obtained from Wikipedia. I used
[d3.js](http://d3js.org) to create the visualizations, and
[jQueryUI](http://jqueryui.com/demos/slider/) for the sliders.

I have put the code and the data used for creating this visualization
[here](https://github.com/sdqali/league_champions) on Github. Feel free
to take the data and code and make more awesome visualizations.