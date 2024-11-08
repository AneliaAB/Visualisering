import plotly.graph_objects as go # or plotly.express as px
import pandas as pd
from dash import Dash, dcc, html

#RADAR CHART DATA
league8 = pd.read_csv('data/analyse/countPerLeague/league8.csv')
league82 = pd.read_csv('data/analyse/countPerLeague/league82.csv')
league384 = pd.read_csv('data/analyse/countPerLeague/league384.csv')
league564 = pd.read_csv('data/analyse/countPerLeague/league564.csv')
print("Data loaded successfully")

categories = [i for i in league8['typeId']]
print("Categories:", categories)

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
      r=[i for i in league8['typeId']],
      theta=categories,
      fill='toself',
      name='Product A'
))
fig.add_trace(go.Scatterpolar(
      r=[i for i in league82['typeId']],
      theta=categories,
      fill='toself',
      name='Product B'
))

fig.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0, 5]
    )),
  showlegend=False
)


print("Figure created")
app = Dash(__name__)
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

    if __name__ == '__main__':
        app.run(debug=True)