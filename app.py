import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import os
import plotly.graph_objs as go
import numpy as np


dir_path = os.path.dirname(os.path.realpath(__file__))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server


app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

colors = {
    'background': '#ffffff',
    'text': '#7FDBFF'
}

# Load in your data
print(dir_path)

df = pd.DataFrame.from_csv(dir_path + '/data/dt_df.csv')
df['date'] = pd.to_datetime(df['date'])
df.set_index(df["date"],inplace=True)
dfplot = df.groupby(pd.Grouper(freq='M')).median()
dfplot.reset_index(inplace=True)
dimensions = df.shape


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Hansard Explorer',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

	html.H2(children = 'simple exploration of topic time series', style = {
		'textAlign': 'center'
	}),
	
	
	dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='topic-slider',
        value= str(0),
        marks={str(t): str(t) for t in range(100)}
    ),
	html.H2(id='topic-number')
	
	])
	
	

@app.callback(
    dash.dependencies.Output('topic-number', 'children'),
    [dash.dependencies.Input('topic-slider', 'value')])
def update_sliderlabel(selected_topic):
	return "you have selected topic: {}".format(selected_topic)

	
@app.callback(
    dash.dependencies.Output('graph-with-slider', 'figure'),
    [dash.dependencies.Input('topic-slider', 'value')])

def update_figure(selected_topic):
    
	filtered_df = dfplot[[str(selected_topic),'date']]
	return_data = [go.Scatter(
			mode = 'lines',
            x=dfplot['date'],
            y=dfplot[str(selected_topic)],
            
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            }
			)]
	return {
        'data': return_data,
        'layout': go.Layout(
            xaxis={ 'title': 'Date'},
            yaxis={'type': 'log','title': 'Topic probability (Log10)'},
            margin={'l': 80, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }	
	
if __name__ == '__main__':
	app.run_server(debug=True)