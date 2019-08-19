An experiment to visualize how football clubs in Europe have dominated
their respective national leagues.

To read more about the motivation and to see the visualization in
action, read this [blog post](http://sadique.io/blog/2012/07/21/visualization-how-european-clubs-dominate-their-leagues/)

Data pulled from Wikipedia.

To see the visualization:
```bash
cd league_champions
python -m SimpleHTTPServer
```

And navigate to `http://localhost:8000/index.html`

The visualization is self-explanatory. You can choose a league to view
and then choose the sliders to select an era for which you want to look
at the data. For fine adjustment, after clicking on either slider, you
can use your keyboard to select a time period.

For example, if you select `Spain` as the league and `2000-2012` as the
time period, you can observer the utter dominance of Real Madrid CF and
FC Barcelona.

The visualization is created with [d3.js](http://d3js.org) and the slider is
from [jQueryUI](http://jqueryui.com/demos/slider/)
