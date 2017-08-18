---
image: /images/threaded-blue-on-black-cropped.jpg
title: "Indian and Pakistani cricketers - who make better debuts?"
date: 2012-05-11
comments: true
categories:
- data
- development
- code
- visualisation
- javascript
- d3.js
- cricket
- india
- pakistan
tags:
- data
- development
- code
- visualisation
- javascript
- d3.js
- cricket
- india
- pakistan
---
Recently a friend and I had an argument about who makes better debuts among Indian and Pakistani cricket players. Now, I am not into cricket. But I do watch the odd matches here and there and am generally aware of what is going on in the game. My stand was that Pakistani players make better debuts compared to Indian players, while my friend was adamant that Indian players make better debuts. My friend is more of a cricket guy than I ever was and he asked me what is the basis of my stand. It was just a gut feel for me and I had to leave it as there was no way for me to prove that my gut feel was correct. But I did want to try, though.

I decided to see if I could prove my theory. Luckily, Cricinfo has all this data, although they dont make it easy for you to get it. I wrote some scripts to pull this data and decided to visualise this using the awesome d3 library. In the end, this became more about figuring out d3 than winning the argument, but doing this was fun.

<!--more-->
## Batsmen

[This scatter-plot](/visualizations/debuts/batsmen.html) shows debut batting performances by all the test players to have ever played for India and Paskistan (Except those players whose batting averages were not computed). As you would have guessed, the blue bubbles are Indian players and the green ones are Pakistanis. The number of runs scored by the each batsman is on the x-axis and batting average in the debut series is on the y-axis. The size of the bubble is representative of the highest score the player scored in the debut series.

I learned some interesting things from this graph:

* Sunil Gavaskar made an amazing debut. His score card for his debut series in 1971 against the might West Indies of 1970's read like this - Matches: 4, Total Runs: 774, High Score: 220, Batting Average: 154.80, 100s: 4, 50s: 3. That is incredible and adding him to this plot would have totally skewed this plot. So technically, I did not learn about Gavaskar's amazing debut from this plot, but from the process of plotting it. But you get the idea.
* It looks like Indian batsmen have historically made slightly better debuts. From my not-so-keen-cricket-lover point of view, anybody who scored 150 runs at an average of 40 had a good debut series. (I chose that arbitrarily, but if you are more of a cricket fan than me, you would have better scales to spot a good debut, and you can draw your own conclusions :-)


## Bowlers

[This scatter-plot](/visualizations/debuts/bowlers.html) shows debut bowling performances by all the test players to have ever played for India and Paskistan (Except those players who took no wickets and hence is not of interest to us). The X-axis shows bowling average and the Y-axis shows number of wickets. The size of the bubble is representative of the number of wickets the bowler had in his best bowling performance in the debut series. Since it is indicative of only the wickets, players with best performances of 2/12 and 2/76 would be shown with bubbles of same size.

Interesting bits:

* Pakistani bowlers make better debuts than Indian bowlers. In the crowd of players with a bowling average of less than 35 and 5 wickets of above, Pakistani players dominate. (Again, disclaimer about arbitrary scales to measure a good performance :-)
* There are a number of Indian bowlers like Dilip Doshi, Shivlal Yadav, Ravichandran Ashwin and Srinivas Venkataraghavn whose debut performances were clear outliers.


## The Code

All the code I used to pull data from Cricinfo, the actual dataset and the Javascript code that generated these plots is available [here](https://github.com/sdqali/debuts) on Github. Feel free to use the dataset to create better visualisations than mine.

## Credits

Srijayanth ([@craftybones](https://twitter.com/craftybones)) helped me a lot with d3 and choosing the colors for the visualisation.
