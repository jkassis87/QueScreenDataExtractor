import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import csv
from datetime import datetime as dt
from datetime import timedelta
import re


app = dash.Dash(__name__)

colors = {
    'background': '#FFFFFF',
}

app.layout = html.Div([
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='Single Day', children=[
            html.Div([
                dcc.DatePickerSingle(
                    id='cal-tab1',
                    min_date_allowed=dt(2019, 1, 15),
                    max_date_allowed=dt(2019, 2, 16),
                    initial_visible_month=dt(2019, 2, 16),
                    date=dt(2019, 2, 15)),
                dcc.Graph(
                    id='graph-tab1',
                )
            ])
        ]),
        dcc.Tab(label='Compare 2 Days', children=[
            dcc.DatePickerSingle(
                id='cal-tab2A',
                min_date_allowed=dt(2019, 1, 15),
                max_date_allowed=dt(2019, 2, 16),
                initial_visible_month=dt(2019, 2, 16),
                date=dt(2019, 2, 15),
            ),
            dcc.DatePickerSingle(
                id='cal-tab2B',
                min_date_allowed=dt(2019, 1, 15),
                max_date_allowed=dt(2019, 2, 16),
                initial_visible_month=dt(2019, 2, 16),
                date=dt(2019, 2, 15),
            ),
                dcc.Graph(
                    id='graph-tab2',
                )
        ]),
        dcc.Tab(label='Date Range', children=[
            dcc.DatePickerRange(
                id='cal-tab3',
                min_date_allowed=dt(2019, 1, 15),
                max_date_allowed=dt(2019, 2, 17),
                initial_visible_month=dt(2019, 2, 1),
                end_date=dt(2019, 8, 25),
            ),
                dcc.Graph(
                    id='graph-tab3',
                )
        ]),
        dcc.Tab(label='Compare 2 Ranges', children=[
            dcc.DatePickerRange(
                id='cal-tab4A',
                min_date_allowed=dt(2019, 1, 15),
                max_date_allowed=dt(2019, 2, 17),
                initial_visible_month=dt(2019, 2, 1),
                end_date=dt(2019, 8, 25),
            ),
            dcc.DatePickerRange(
                id='cal-tab4B',
                min_date_allowed=dt(2019, 1, 15),
                max_date_allowed=dt(2019, 2, 17),
                initial_visible_month=dt(2019, 2, 1),
                end_date=dt(2019, 8, 25),
            ),
                dcc.Graph(
                    id='graph-tab4',
                )
        ])
    ])
])



# callback for tab 1
@app.callback(
    dash.dependencies.Output('graph-tab1', 'figure'),
    [dash.dependencies.Input('cal-tab1', 'date')]
    )
def update_tab1(date):

    if date is not None:
        thedate = dt.strptime(date, '%Y-%m-%d')
        date_string = str(thedate)
        date_string = re.sub(' 00:00:00', '', date_string)
        f = open((date_string + '.csv'))
        csvfile = csv.reader(f)
        tdata = list(csvfile)
        figure = {
            'data': [
                      {'x': tdata[0], 'y': tdata[13], 'type': 'line', 'name': 'Total L1', 'marker': {'color': 'rgb(0, 89, 234)'}},
                      {'x': tdata[0], 'y': tdata[17], 'type': 'bar', 'name': 'Diff L1', 'marker': {'color': 'rgb(0, 89, 234)'}},
                      ],
            'layout': {
                      'title': 'Ticket Stats',
                      'plot_bgcolor': colors['background'],
                      }
                  }
    return figure



# callback for tab 2
@app.callback(
    dash.dependencies.Output('graph-tab2', 'figure'),
    [dash.dependencies.Input('cal-tab2A', 'date'),
     ]
    )
def update_tab2a(date):

    if date is not None:
        thedate = dt.strptime(date, '%Y-%m-%d')
        date_string = str(thedate)
        date_string = re.sub(' 00:00:00', '', date_string)
        f = open((date_string + '.csv'))
        csvfile = csv.reader(f)
        tdata = list(csvfile)
        figure = {
            'data': [
                      {'x': tdata[0], 'y': tdata[13], 'type': 'line', 'name': 'Total L1', 'marker': {'color': 'rgb(0, 89, 234)'}},
                      {'x': tdata[0], 'y': tdata[17], 'type': 'bar', 'name': 'Diff L1', 'marker': {'color': 'rgb(0, 89, 234)'}},
                      ],
            'layout': {
                      'title': 'Ticket Stats',
                      'plot_bgcolor': colors['background'],
                      }
                  }
    return figure



# callback for tab 3
@app.callback(
    dash.dependencies.Output('graph-tab3', 'figure'),
    [dash.dependencies.Input('cal-tab3', 'start_date'),
     dash.dependencies.Input('cal-tab3', 'end_date')]
    )
def update_tab3(start_date, end_date):

    if end_date is not None and start_date is not None:
        thedate = dt.strptime(end_date, '%Y-%m-%d')
        date_string = str(thedate)
        date_string = re.sub(' 00:00:00', '', date_string)
        f = open((date_string + '.csv'))
        csvfile = csv.reader(f)
        tdata = list(csvfile)
        figure = {
            'data': [
                      {'x': tdata[0], 'y': tdata[13], 'type': 'line', 'name': 'Total L1', 'marker': {'color': 'rgb(0, 89, 234)'}},
                      {'x': tdata[0], 'y': tdata[17], 'type': 'bar', 'name': 'Diff L1', 'marker': {'color': 'rgb(0, 89, 234)'}},
                      ],
            'layout': {
                      'title': 'Ticket Stats',
                      'plot_bgcolor': colors['background'],
                      }
                  }
    return figure



# callback for tab 4
@app.callback(
    dash.dependencies.Output('graph-tab4', 'figure'),
    [dash.dependencies.Input('cal-tab4A', 'end_date'),
     dash.dependencies.Input('cal-tab4B', 'end_date')]
    )
def update_tab4(end_date):

    if end_date is not None:
        thedate = dt.strptime(end_date, '%Y-%m-%d')
        date_string = str(thedate)
        date_string = re.sub(' 00:00:00', '', date_string)
        f = open((date_string + '.csv'))
        csvfile = csv.reader(f)
        tdata = list(csvfile)
        figure = {
            'data': [
                      {'x': tdata[0], 'y': tdata[13], 'type': 'line', 'name': 'Total L1', 'marker': {'color': 'rgb(0, 89, 234)'}},
                      {'x': tdata[0], 'y': tdata[17], 'type': 'bar', 'name': 'Diff L1', 'marker': {'color': 'rgb(0, 89, 234)'}},
                      ],
            'layout': {
                      'title': 'Ticket Stats',
                      'plot_bgcolor': colors['background'],
                      }
                  }
    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
