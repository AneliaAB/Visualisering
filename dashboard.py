import plotly.graph_objects as go # or plotly.express as px
import pandas as pd
from dash import Dash, dcc, html, Input, Output, callback, State
import plotly.express as px
from plotly.subplots import make_subplots
import os

#RADAR CHART DATA
league8 = pd.read_csv('data/analyse/countPerLeague/league8.csv') 
league82 = pd.read_csv('data/analyse/countPerLeague/league82.csv')
league384 = pd.read_csv('data/analyse/countPerLeague/league384.csv')
league564 = pd.read_csv('data/analyse/countPerLeague/league564.csv')
print("Data loaded successfully")

categories = [i for i in league8['name']]
print("Categories:", categories)

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
      r=[i for i in league8['count']],
      theta=categories,
      fill='toself',
      name='Product A'
))
fig.add_trace(go.Scatterpolar(
      r=[i for i in league82['count']],
      theta=categories,
      fill='toself',
      name='Product B'
))

# Data for VAR introduction
leagues = ["serie A", "bundesliga", "la Liga", "premier League", "champions League"]
years = [2017, 2017, 2018, 2019, 2019]
y_positions = [0.40, 0.5, 0.5, 0.5, 0.4]  # Adjusted y positions for alternating labels


print("Figure created")

#import full VAR file for barchart and timeline (missing)
all_leagues = pd.read_csv('VAR_all.csv')

# timeline
fig_timeline=go.Figure(
            data = [
                go.Scatter(
                    x=years,
                    y=y_positions,  
                    mode="markers+text",
                    marker=dict(size=12, color=["blue", "red", "green", "orange", "purple"]),
                    text=leagues,
                    textposition=["bottom center", "top center", "bottom center", "top center", "bottom center"]
                )
            ],
            layout = go.Layout(
                xaxis=dict(title="Year", tickmode="linear", dtick=1, showgrid=False, zeroline=False),
                yaxis=dict(title="League", showticklabels=False, showgrid=False, zeroline=False, range=[0, 1.5]),
                title="VAR Introduction Timeline",
                plot_bgcolor="white",  
                showlegend=False,
                shapes=[
                    dict(type="line", x0=2016, x1=2020, y0=0.15, y1=0.15, line=dict(color="black", width=2))  # Lowered the line closer to the x-axis
                ]
            )
)

fig_timeline.update_layout(clickmode='event+select')

#Histogram setup
fig = px.histogram(all_leagues, 
                   x="league", 
                   y="type_id", 
                   barmode="overlay", 
                   color = 'league', 
                   hover_data = 'event', 
                   labels = {'type_id': 'VAR usage'},
                   category_orders = {'league': ['bundesliga', 'la liga', 'serie a', 'premier league']}, 
                   opacity = 1.0)

fig.update_layout(clickmode='event+select')

#var
path = 'data/analyse/countPerLeague'
size=[]
y=[]
league_names = []

for file in os.listdir(path):
    event_file = pd.read_csv(f'{path}/{file}')
    type_names = [i for i in event_file['name']]
    event_file = pd.read_csv(f'{path}/{file}')
    size = size + [i for i in event_file['count']]
    y = y + [i for i in event_file['Unnamed: 0']]
    league_names.append(file.split('.')[0])
    print(event_file)
cut_interval = [1500, 6500]

data=[
    go.Bar(name='VAR', x=league_names, y=[966, 837, 1184,686], marker_color='blue', showlegend=False),
    go.Bar(name='Yellowcard', x=league_names, y=[12158, 11755, 8966, 6902], marker_color='red', showlegend=False),
    go.Bar(name='Redcard', x=league_names, y=[374, 457, 177, 104], marker_color='yellow', showlegend=False),
    go.Bar(name='Yellow/Red card', x=league_names, y=[252, 293, 122, 132], marker_color='orange', showlegend=False)
]

fig_var_barplot = make_subplots(
    rows=2,
    cols=1,
    vertical_spacing=0.05,
    shared_xaxes=True,
)
for trace in data:
    fig_var_barplot.add_trace(trace, row=1, col=1)

# Adjust y-axis range for the upper part
fig_var_barplot.update_yaxes(range=[cut_interval[1], max(max(trace.y for trace in data)) * 1.1], row=1, col=1)
fig_var_barplot.update_xaxes(visible=False, row=1, col=1)

# Add data to the second subplot (lower part) with low range
for trace in data:
    fig_var_barplot.add_trace(trace, row=2, col=1)

# Adjust y-axis range for the lower part
fig_var_barplot.update_yaxes(range=[0, cut_interval[0]], row=2, col=1)
fig_var_barplot.update_layout(clickmode='event+select')

# data
df = pd.DataFrame({'years': [1995, 1996, 1997, 1998, 1999, 2000,
                             2001, 2002, 2003, 2004, 2005, 2006,
                             2007, 2008, 2009, 2010, 2011, 2012],
                  'China': [219, 146, 112, 127, 124, 180, 236,
                            207, 236, 263,350, 430, 474, 1526,
                            488, 537, 500, 439],
                  'Rest of world': [16, 13, 10, 11, 28, 37,
                                        43, 55, 56, 88, 105, 156, 270,
                                        299, 340, 403, 549, 1499]})
df.set_index('years', inplace = True)

# colors and cut-offs
colors = px.colors.qualitative.Plotly
cut_interval = [600, 1400]

# subplot setup
fig2 = make_subplots(rows=2, cols=1, vertical_spacing = 0.04)
fig2.update_layout(title = "USA plastic scrap exports (...with some made-up values)")

# Traces for [2, 1]
# marker_color=colors[i] ensures that categories follow the same color cycle
for i, col in enumerate(df.columns):
    fig2.add_trace(go.Bar(x=df.index,
                    y=df[col],
                    name=col,
                    marker_color=colors[i],
                    legendgroup = col,
                    ), row=2, col=1)

# Traces for [1, 1]
# Notice that showlegend = False.
# Since legendgroup = col the interactivity is
# taken care of in the previous for-loop.
for i, col in enumerate(df.columns):
    fig2.add_trace(go.Bar(x=df.index,
                    y=df[col],
                    name=col,
                    marker_color=colors[i],
                    legendgroup = col,
                    showlegend = False,
                    ), row=1, col=1)

# Some aesthetical adjustments to layout
fig2.update_yaxes(range=[cut_interval[1], max(df.max()*1.1)], row=1, col=1)
fig2.update_xaxes(visible=False, row=1, col=1)
fig2.update_yaxes(range=[0, cut_interval[0]], row=2, col=1)
fig2.update_layout(clickmode='event+select')

#APP
app = Dash(__name__)
app.layout = html.Div([
    dcc.Graph(figure=fig, id='league_events', clickData=None), 
    html.H2('All leagues',id='league_title'),
    dcc.Store(id='last_click_store', data=None),
    html.H1("Timeline of VAR Introduction"),
    dcc.Graph(figure=fig_timeline, id = 'fig_timeline', clickData=None),
    html.H2('Var usage in different leagues (with full scale break)'),
    dcc.Graph(figure=fig2)
])

@callback(
    Output('league_title', 'children'),
    Output('last_click_store', 'data'),
    Input('league_events', 'clickData'),
    State('last_click_store', 'data'))
def display_relayout_data(clickData, last_click):
      print(f"ClickData: {clickData}")
      print(f"Last Click: {last_click}")
      if (clickData == None):
        return ' All leagues', None
      elif (clickData['points'][0]['x'] == last_click):
        return ' All leagues', None
      else: 
         return 'Clicked' + ' ' + clickData['points'][0]['x'], clickData['points'][0]['x']

@callback(
    Output('fig_timeline', 'clickData'),
    Input('league_events', 'clickData'))
def update_timeline(clickData):
      if (clickData == None):
        return None
      else:
        index = clickData['points'][0]['curveNumber']
        print(leagues[index])
      

if __name__ == '__main__':
    app.run(debug=True, port=8030)