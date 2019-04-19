#!/home/tstatsdp/public_html/live/bin/python3

import dash, dash_auth, re, csv, sqlite3
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from datetime import datetime as dt
from datetime import timedelta
from datetime import date as dtm
import pandas as pd
from dateutil import parser

now = dt.now() - timedelta(1)
app = dash.Dash(__name__)

colors = {
    'background': '#FFFFFF',
}

def gettdata(date):

    tteams = ["L1", "L2", "L3", "Bil"]
    ss = ':00:00'
    stats = [
            [date + ' 00' + ss, date + ' 01' + ss, date + ' 02' + ss, date + ' 03' + ss, date + ' 04' + ss,
            date + ' 05' + ss, date + ' 06' + ss, date + ' 07' + ss, date + ' 08' + ss, date + ' 09' + ss,
            date + ' 10' + ss, date + ' 11' + ss, date + ' 12' + ss, date + ' 13' + ss, date + ' 14' + ss,
            date + ' 15' + ss, date + ' 16' + ss, date + ' 17' + ss, date + ' 18' + ss, date + ' 19' + ss,
            date + ' 20' + ss, date + ' 21' + ss, date + ' 22' + ss, date + ' 23' + ss],
        ]

    for t in tteams:
        stats_add = []
        for x in stats[0]:
            conn = sqlite3.connect("tdatadb.sqlite")
            curs = conn.cursor()
            query = "SELECT Stat FROM AllData WHERE Brand = '" + t + "' AND Date = '" + str(x) + "';"
            curs.execute(query)
            stat = curs.fetchone()
            stats_add.extend(stat)

        stats.append(stats_add)

    stats_add_lists = [[], [], [], []]
    stats = stats + stats_add_lists
    for thour in range(len(stats[0])):
        if thour == 0:
            stats[5].append(0)
            stats[6].append(0)
            stats[7].append(0)
            stats[8].append(0)
        else:
            stats[5].append(stats[1][thour] - stats[1][(thour - 1)])
            stats[6].append(stats[2][thour] - stats[2][(thour - 1)])
            stats[7].append(stats[3][thour] - stats[3][(thour - 1)])
            stats[8].append(stats[4][thour] - stats[4][(thour - 1)])

    for x in stats:
        print(x)
        print(str(len(x)))
    return (stats)

app.layout = html.Div([
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='Single Day', children=[
            html.Div([
                dcc.DatePickerSingle(
                    id='cal-tab1',
                    min_date_allowed=dt(2019, 1, 15),
                    max_date_allowed=dt(now.year, now.month, now.day),
                    initial_visible_month=dt(now.year, now.month, now.day),
                    date=dt(now.year, now.month, now.day)),
                dcc.Graph(
                    id='graph-tab1',
                )
            ])
        ]),
        dcc.Tab(label='Compare 2 Days', children=[
            dcc.DatePickerRange(
                id='cal-tab2A',
                min_date_allowed=dt(2019, 1, 15),
                max_date_allowed=dt(now.year, now.month, now.day),
                initial_visible_month=dt(now.year, now.month, now.day),
                start_date=dt(now.year, now.month, now.day),
                end_date=dt(now.year, now.month, now.day)
            ),
                dcc.Graph(
                    id='graph-tab2',
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
        tdata = gettdata(date)
        hr_list = list(range(0, 25))
        figure = {
            'data': [
                      {'x': hr_list, 'y': tdata[1], 'type': 'line', 'name': 'Total L1',
                       'legendgroup': 'Level 1', 'marker': {'color': 'rgb(0, 0, 255)'}},
                {'x': hr_list, 'y': tdata[5], 'type': 'bar', 'name': 'Diff L1',
                 'legendgroup': 'Level 1', 'marker': {'color': 'rgb(0, 0, 255)'}},
                {'x': hr_list, 'y': tdata[2], 'type': 'line', 'name': 'Total L2',
                 'legendgroup': 'Level 2', 'marker': {'color': 'rgb(255, 0, 0)'}},
                {'x': hr_list, 'y': tdata[6], 'type': 'bar', 'name': 'Diff L2',
                 'legendgroup': 'Level 2', 'marker': {'color': 'rgb(255, 0, 0'}},
                {'x': hr_list, 'y': tdata[3], 'type': 'line', 'name': 'Total L3',
                 'legendgroup': 'Level 3', 'marker': {'color': 'rgb(0, 255, 0)'}},
                {'x': hr_list, 'y': tdata[7], 'type': 'bar', 'name': 'Diff L3',
                 'legendgroup': 'Level 3', 'marker': {'color': 'rgb(0, 255, 0)'}},
                {'x': hr_list, 'y': tdata[4], 'type': 'line', 'name': 'Total Bil',
                 'legendgroup': 'Billing', 'marker': {'color': 'rgb(51, 51, 51)'}},
                {'x': hr_list, 'y': tdata[8], 'type': 'bar', 'name': 'Diff Bil',
                 'legendgroup': 'Billing', 'marker': {'color': 'rgb(51, 51, 51)'}},
            ],
            'layout': {
                      'title': 'Ticket Stats For ' + parser.parse(date).strftime("%A") + ' ' + date,
                      'plot_bgcolor': colors['background'],
                'xaxis': {'title': 'Hour Of The Day', 'tickmode': 'linear', 'dtick': 1},
                'yaxis': {'title': 'Ticket Count', 'tickmode': 'linear', 'dtick': 10},
                'legend': {'orientation': 'h', 'x': 0, 'y': -0.2, 'yanchor': 'top'}
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
        tdata_start = gettdata(start_date)
        tdata_end = gettdata(end_date)
        hr_list = list(range(0, 25))
        figure = {
            'data': [
                      {'x': hr_list, 'y': tdata_start[1], 'type': 'line', 'name': 'Total L1 - A',
                       'legendgroup': 'Level 1', 'marker': {'color': 'rgb(0, 0, 255)'}},
                {'x': hr_list, 'y': tdata_start[5], 'type': 'bar', 'name': 'Diff L1 - A',
                 'legendgroup': 'Level 1', 'marker': {'color': 'rgb(0, 0, 255)'}},
                {'x': hr_list, 'y': tdata_end[1], 'type': 'line', 'name': 'Total L1 - B',
                 'legendgroup': 'Level 1', 'marker': {'color': 'rgb(255, 123, 0)'}},
                {'x': hr_list, 'y': tdata_end[5], 'type': 'bar', 'name': 'Diff L1 - B',
                 'legendgroup': 'Level 1', 'marker': {'color': 'rgb(255, 123, 0)'}},
                {'x': hr_list, 'y': tdata_start[2], 'type': 'line', 'name': 'Total L2 - A',
                 'legendgroup': 'Level 2', 'marker': {'color': 'rgb(255, 0, 0)'}},
                {'x': hr_list, 'y': tdata_start[6], 'type': 'bar', 'name': 'Diff L2 - A',
                 'legendgroup': 'Level 2', 'marker': {'color': 'rgb(255, 0, 0)'}},
                {'x': hr_list, 'y': tdata_end[2], 'type': 'line', 'name': 'Total L2 - B',
                 'legendgroup': 'Level 2', 'marker': {'color': 'rgb(0, 255, 255)'}},
                {'x': hr_list, 'y': tdata_end[6], 'type': 'bar', 'name': 'Diff L2 - B',
                 'legendgroup': 'Level 2', 'marker': {'color': 'rgb(0, 255, 255)'}},
                {'x': hr_list, 'y': tdata_start[3], 'type': 'line', 'name': 'Total L3 - A',
                 'legendgroup': 'Level 3', 'marker': {'color': 'rgb(0, 0, 0)'}},
                {'x': hr_list, 'y': tdata_start[7], 'type': 'bar', 'name': 'Diff L3 - A',
                 'legendgroup': 'Level 3', 'marker': {'color': 'rgb(0, 0, 0)'}},
                {'x': hr_list, 'y': tdata_end[3], 'type': 'line', 'name': 'Total L3 - B',
                 'legendgroup': 'Level 3', 'marker': {'color': 'rgba(120, 120, 120)'}},
                {'x': hr_list, 'y': tdata_end[7], 'type': 'bar', 'name': 'Diff L3 - B',
                 'legendgroup': 'Level 3', 'marker': {'color': 'rgb(120, 120, 120)'}},
                {'x': hr_list, 'y': tdata_start[4], 'type': 'line', 'name': 'Total Bil - A',
                 'legendgroup': 'Billing', 'marker': {'color': 'rgb(0, 255, 0)'}},
                {'x': hr_list, 'y': tdata_start[8], 'type': 'bar', 'name': 'Diff Bil - A',
                 'legendgroup': 'Billing', 'marker': {'color': 'rgb(0, 255, 0)'}},
                {'x': hr_list, 'y': tdata_end[4], 'type': 'line', 'name': 'Total Bil - B',
                 'legendgroup': 'Billing', 'marker': {'color': 'rgb(255, 0, 255)'}},
                {'x': hr_list, 'y': tdata_end[8], 'type': 'bar', 'name': 'Diff Bil - B',
                 'legendgroup': 'Billing', 'marker': {'color': 'rgb(255, 0, 255)'}},
            ],
            'layout': {
                      'title': 'Ticket Stats for A - ' + parser.parse(start_date).strftime("%A") + ' '
                               + start_date + ' and B - ' + parser.parse(end_date).strftime("%A") + ' ' + end_date,
                      'plot_bgcolor': colors['background'],
                'xaxis': {'title': 'Hour Of The Day', 'tickmode': 'linear', 'dtick': 1},
                'yaxis': {'title': 'Ticket Count', 'tickmode': 'linear', 'dtick': 10},
                'legend': {'orientation': 'h', 'x': 0, 'y': -0.2, 'yanchor': 'top'},
                'barmode': 'overlay'
                      }
                  }
    return figure


def run_server(self,
               port=80,
               debug=True,
               threaded=True,
               **flask_run_options):
    self.server.run(port=port, debug=debug, **flask_run_options)


if __name__ == '__main__':
        app.run_server(host='tstats.digitalpacific.com.au', debug=True)
