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
            dcc.DatePickerRange(
                id='cal-tab2A',
                min_date_allowed=dt(2019, 1, 15),
                max_date_allowed=dt(2019, 2, 16),
                initial_visible_month=dt(2019, 2, 16),
                start_date=dt(2019, 1, 15),
                end_date=dt(2019, 8, 25)
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
                start_date= dt(2019, 1, 15),
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
                start_date=dt(2019, 1, 15),
                end_date=dt(2019, 8, 25),
            ),
            dcc.DatePickerRange(
                id='cal-tab4B',
                min_date_allowed=dt(2019, 1, 15),
                max_date_allowed=dt(2019, 2, 17),
                initial_visible_month=dt(2019, 2, 1),
                start_date=dt(2019, 1, 15),
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
                      {'x': tdata[0], 'y': tdata[13], 'type': 'line', 'name': 'Total L1', 'marker': {'color': 'rgb(0, 0, 255)'}},
                      {'x': tdata[0], 'y': tdata[17], 'type': 'bar', 'name': 'Diff L1', 'marker': {'color': 'rgb(0, 0, 255)'}},
                {'x': tdata[0], 'y': tdata[14], 'type': 'line', 'name': 'Total L1', 'marker': {'color': 'rgb(255, 0, 0)'}},
                {'x': tdata[0], 'y': tdata[18], 'type': 'bar', 'name': 'Diff L1', 'marker': {'color': 'rgb(255, 0, 0)'}},
                {'x': tdata[0], 'y': tdata[16], 'type': 'line', 'name': 'Total L1', 'marker': {'color': 'rgb(0, 255, 0)'}},
                {'x': tdata[0], 'y': tdata[20], 'type': 'bar', 'name': 'Diff L1', 'marker': {'color': 'rgb(0, 255, 0)'}},
                {'x': tdata[0], 'y': tdata[15], 'type': 'line', 'name': 'Total L1', 'marker': {'color': 'rgb(51, 51, 51)'}},
                {'x': tdata[0], 'y': tdata[19], 'type': 'bar', 'name': 'Diff L1', 'marker': {'color': 'rgb(51, 51, 51)'}},
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
    [dash.dependencies.Input('cal-tab2A', 'start_date'),
    dash.dependencies.Input('cal-tab2A', 'end_date')
     ]
    )
def update_tab2a(start_date, end_date):

    if start_date is not None and end_date is not None:
        thedate_start = dt.strptime(start_date, '%Y-%m-%d')
        thedate_end = dt.strptime(end_date, '%Y-%m-%d')
        date_string_start = str(thedate_start)
        date_string_end = str(thedate_end)
        date_string_start = re.sub(' 00:00:00', '', date_string_start)
        date_string_end = re.sub(' 00:00:00', '', date_string_end)
        f_start = open((date_string_start + '.csv'))
        f_end = open((date_string_end + '.csv'))
        csvfile_start = csv.reader(f_start)
        csvfile_end = csv.reader(f_end)
        tdata_start = list(csvfile_start)
        tdata_end = list(csvfile_end)
        figure = {
            'data': [
                      {'x': tdata_start[0], 'y': tdata_start[13], 'type': 'line', 'name': 'Total L1 - A', 'marker': {'color': 'rgb(0, 0, 255)'}},
                      {'x': tdata_start[0], 'y': tdata_start[17], 'type': 'bar', 'name': 'Diff L1 - A', 'marker': {'color': 'rgb(0, 0, 255)'}},
                {'x': tdata_end[0], 'y': tdata_end[13], 'type': 'line', 'name': 'Total L1 - B', 'marker': {'color': 'rgba(0, 0, 255, 0.6)'}},
                {'x': tdata_end[0], 'y': tdata_end[17], 'type': 'bar', 'name': 'Diff L1 - B', 'marker': {'color': 'rgba(0, 0, 255, 0.6)'}},
                {'x': tdata_start[0], 'y': tdata_start[14], 'type': 'line', 'name': 'Total L2 - A', 'marker': {'color': 'rgb(255, 0, 0)'}},
                {'x': tdata_start[0], 'y': tdata_start[18], 'type': 'bar', 'name': 'Diff L2 - A', 'marker': {'color': 'rgb(255, 0, 0)'}},
                {'x': tdata_end[0], 'y': tdata_end[14], 'type': 'line', 'name': 'Diff L2 - B', 'marker': {'color': 'rgba(255, 0, 0, 0.6)'}},
                {'x': tdata_end[0], 'y': tdata_end[18], 'type': 'bar', 'name': 'Diff L2 - B', 'marker': {'color': 'rgba(255, 0, 0, 0.6)'}},
                {'x': tdata_end[0], 'y': tdata_end[16], 'type': 'bar', 'name': 'Total BL - A', 'marker': {'color': 'rgb(0, 255, 0)'}},
                {'x': tdata_start[0], 'y': tdata_start[20], 'type': 'line', 'name': 'Diff BL - A', 'marker': {'color': 'rgb(0, 255, 0)'}},
                {'x': tdata_start[0], 'y': tdata_start[16], 'type': 'bar', 'name': 'Total BL - B', 'marker': {'color': 'rgba(0, 255, 0, 0.6)'}},
                {'x': tdata_end[0], 'y': tdata_end[20], 'type': 'line', 'name': 'Diff BL - B', 'marker': {'color': 'rgba(0, 255, 0, 0.6)'}},
                {'x': tdata_start[0], 'y': tdata_start[15], 'type': 'line', 'name': 'Total L3 - A', 'marker': {'color': 'rgb(51, 51, 51)'}},
                {'x': tdata_start[0], 'y': tdata_start[19], 'type': 'bar', 'name': 'Diff L3 - A', 'marker': {'color': 'rgb(51, 51, 51)'}},
                {'x': tdata_end[0], 'y': tdata_end[15], 'type': 'line', 'name': 'Total L3 - B', 'marker': {'color': 'rgba(51, 51, 51, 0.6)'}},
                {'x': tdata_end[0], 'y': tdata_end[19], 'type': 'bar', 'name': 'Diff L3 - B', 'marker': {'color': 'rgba(51, 51, 51, 0.6)'}}
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
        thedate_start = dt.strptime(start_date, '%Y-%m-%d')
        date_string_start = str(thedate_start)
        date_string_start = re.sub(' 00:00:00', '', date_string_start)
        x = dt(int(date_string_start[0:4]), int(date_string_start[5:7]), int(date_string_start[8:10]))
        thedate_end = dt.strptime(end_date, '%Y-%m-%d')
        date_string_end = str(thedate_end)
        date_string_end = re.sub(' 00:00:00', '', date_string_end)
        y = dt(int(date_string_end[0:4]), int(date_string_end[5:7]), int(date_string_end[8:10]))
        tdata = []
        while y >= x:
            thedate_x = str(x)
            thedate_x = re.sub(' 00:00:00', '', thedate_x)
            thedate = dt.strptime(thedate_x, '%Y-%m-%d')
            date_string = str(thedate)
            date_string = re.sub(' 00:00:00', '', date_string)
            f = open((date_string + '.csv'))
            csvfile = csv.reader(f)
            csvlist = list(csvfile)
            tdata.extend(csvlist)
            x = x + timedelta(1)
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
