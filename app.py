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

    html.Div(children='Demoing a single topic timeseries', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
	
	html.H2(children = 'the size of the dataframe is {} rows'.format(dimensions[0]), style = {
		'textAlign': 'center'
	}),
	
	
	dcc.Graph(
        id='topic-through-time',
        figure={
            'data': [
                go.Scatter(
							x = dfplot['date'],
							y = np.log10(dfplot['0']),
							mode = 'lines'
							)
							],
				'layout': go.Layout(
                xaxis={ 'title': 'Date'},
                yaxis={'title': 'Probability (log)'}
				)
				})
	
	])
	
	
if __name__ == '__main__':
	app.run_server(debug=True)