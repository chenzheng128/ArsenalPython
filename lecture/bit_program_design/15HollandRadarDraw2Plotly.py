#HollandRadarDraw2Ploly

# Source: https://plot.ly/python/radar-chart/

# Learn about API authentication here: https://plot.ly/pandas/getting-started
# Find your api_key here: https://plot.ly/settings/api

"""
pip install plotly
"""

import plotly
import plotly.plotly as py
import plotly.graph_objs as go

data = [go.Scatterpolar(
  r = [39, 28, 8, 7, 28, 39],
  theta = ['A','B','C', 'D', 'E', 'A'],
  fill = 'toself'
)]

layout = go.Layout(
  polar = dict(
    radialaxis = dict(
      visible = True,
      range = [0, 50]
    )
  ),
  showlegend = False
)

fig = go.Figure(data=data, layout=layout)
# 标准例子是在线绘制 Online plot
#py.iplot(fig, filename = "radar/basic")
# 修改为离线绘制
plotly.offline.plot(fig, filename = "15radar-plotly")