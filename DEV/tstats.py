import dash, dash_auth, re, csv, sqlite3
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from datetime import datetime as dt
from datetime import timedelta
import pandas as pd


now = dt.now() - timedelta(1)

app = dash.Dash(__name__)

colors = {
    'background': '#FFFFFF',
}


def getrange(start_date, end_date):
    sdate = []
    while start_date <= end_date:
        ss = ':00:00'
        start_date += timedelta(days=1)
        date = start_date.strftime('%Y-%m-%d')
        sdate1 = [
            date + ' 00' + ss, date + ' 01' + ss, date + ' 02' + ss, date + ' 03' + ss, date + ' 04' + ss,
            date + ' 05' + ss, date + ' 06' + ss, date + ' 07' + ss, date + ' 08' + ss, date + ' 09' + ss,
            date + ' 10' + ss, date + ' 11' + ss, date + ' 12' + ss, date + ' 13' + ss, date + ' 14' + ss,
            date + ' 15' + ss, date + ' 06' + ss, date + ' 07' + ss, date + ' 18' + ss, date + ' 19' + ss,
            date + ' 20' + ss, date + ' 21' + ss, date + ' 22' + ss, date + ' 23' + ss
        ]

        sdate.extend(sdate1)

    return pd.Series(sdate)

def gettdata(date):
    conn = sqlite3.connect("tdatadb.sqlite")
    tlist1 = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]]
    tteams = ["L1", "L2", "L3", "Bil"]
    for y in tteams:
        tstatadd = []
        for x in range(len(tlist1[0])):
            rr = "SELECT Stat FROM AllData WHERE Team = '" + y + "' AND Hour = " + str(x) + " AND Date = '" + date + "';"
            df = pd.read_sql_query(rr, conn)
            tlistdata = list(df["Stat"])
            tcount = sum(tlistdata)
            tstatadd.append(tcount)

        tlist1.append(tstatadd)
        tstatadd = []

    tlist1d = [[], [], [], []]
    tlist1 = tlist1 + tlist1d
    for thour in range(len(tlist1[0])):
        if thour == 0:
            tlist1[5].append(0)
            tlist1[6].append(0)
            tlist1[7].append(0)
            tlist1[8].append(0)
        else:
            tlist1[5].append(tlist1[1][thour] - tlist1[1][(thour - 1)])
            tlist1[6].append(tlist1[2][thour] - tlist1[2][(thour - 1)])
            tlist1[7].append(tlist1[3][thour] - tlist1[3][(thour - 1)])
            tlist1[8].append(tlist1[4][thour] - tlist1[4][(thour - 1)])

    return (tlist1)


def format_date(datest):
    thedate = dt.strptime(datest, '%Y-%m-%d')
    date_string = str(thedate)
    date_string = re.sub(' 00:00:00', '', date_string)
    return(date_string)


def get_date_range(start_date, end_date):
    tdata = [[], [], [], [], [], [], [], [], []]

    start_datex = dt(int(start_date[0:4]), int(start_date[5:7]), int(start_date[8:10]))
    end_datex = dt(int(end_date[0:4]), int(end_date[5:7]), int(end_date[8:10]))

    while start_datex <= end_datex:
        date_str = str(start_datex)
        date_str = date_str[:10]
        tdatax = gettdata(date_str)
        tdata[0].extend(tdatax[0])
        tdata[1].extend(tdatax[1])
        tdata[2].extend(tdatax[2])
        tdata[3].extend(tdatax[3])
        tdata[4].extend(tdatax[4])
        tdata[5].extend(tdatax[5])
        tdata[6].extend(tdatax[6])
        tdata[7].extend(tdatax[7])
        tdata[8].extend(tdatax[8])
        for x in tdatax:
            print(x)

        start_datex += timedelta(days=1)

    tdata = tdata[1:]
    for x in tdata:
        print(x)

    df = pd.DataFrame(tdata)
    df = df.transpose()
    df.columns = ['L1Total', 'L2Total', 'L3Total', 'BilTotal', 'L1Diff', 'L2Diff', 'L3Diff', 'BilDiff']
    print(df)
    return(df)


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
        ]),
        dcc.Tab(label='Date Range', children=[
            dcc.DatePickerRange(
                id='cal-tab3',
                min_date_allowed=dt(2019, 1, 15),
                max_date_allowed=dt(now.year, now.month, now.day),
                initial_visible_month=dt(now.year, now.month, now.day),
                start_date= dt(now.year, now.month, now.day),
                end_date=dt(now.year, now.month, now.day),
            ),
                dcc.Graph(
                    id='graph-tab3',
                )
        ]),
        dcc.Tab(label='Compare 2 Ranges', children=[
            dcc.DatePickerRange(
                id='cal-tab4A',
                min_date_allowed=dt(2019, 1, 15),
                max_date_allowed=dt(now.year, now.month, now.day),
                initial_visible_month=dt(now.year, now.month, now.day),
                start_date=dt(now.year, now.month, now.day),
                end_date=dt(now.year, now.month, now.day),
            ),
            dcc.DatePickerRange(
                id='cal-tab4B',
                min_date_allowed=dt(2019, 1, 15),
                max_date_allowed=dt(now.year, now.month, now.day),
                initial_visible_month=dt(now.year, now.month, now.day),
                start_date=dt(now.year, now.month, now.day),
                end_date=dt(now.year, now.month, now.day),
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
        tdata = gettdata(format_date(date))
        figure = {
            'data': [
                      {'x': tdata[0], 'y': tdata[1], 'type': 'line', 'name': 'Total L1',
                       'legendgroup': 'Level 1', 'marker': {'color': 'rgb(0, 0, 255)'}},
                {'x': tdata[0], 'y': tdata[5], 'type': 'bar', 'name': 'Diff L1',
                 'legendgroup': 'Level 1', 'marker': {'color': 'rgb(0, 0, 255)'}},
                {'x': tdata[0], 'y': tdata[2], 'type': 'line', 'name': 'Total L2',
                 'legendgroup': 'Level 2', 'marker': {'color': 'rgb(255, 0, 0)'}},
                {'x': tdata[0], 'y': tdata[6], 'type': 'bar', 'name': 'Diff L2',
                 'legendgroup': 'Level 2', 'marker': {'color': 'rgb(255, 0, 0'}},
                {'x': tdata[0], 'y': tdata[3], 'type': 'line', 'name': 'Total L3',
                 'legendgroup': 'Level 3', 'marker': {'color': 'rgb(0, 255, 0)'}},
                {'x': tdata[0], 'y': tdata[7], 'type': 'bar', 'name': 'Diff L3',
                 'legendgroup': 'Level 3', 'marker': {'color': 'rgb(0, 255, 0)'}},
                {'x': tdata[0], 'y': tdata[4], 'type': 'line', 'name': 'Total Bil',
                 'legendgroup': 'Billing', 'marker': {'color': 'rgb(51, 51, 51)'}},
                {'x': tdata[0], 'y': tdata[8], 'type': 'bar', 'name': 'Diff Bil',
                 'legendgroup': 'Billing', 'marker': {'color': 'rgb(51, 51, 51)'}},
            ],
            'layout': {
                      'title': 'Ticket Stats For ' + format_date(date),
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
        tdata_start = gettdata(format_date(start_date))
        tdata_end = gettdata(format_date(end_date))
        figure = {
            'data': [
                      {'x': tdata_start[0], 'y': tdata_start[1], 'type': 'line', 'name': 'Total L1 - A',
                       'legendgroup': 'Level 1', 'marker': {'color': 'rgb(0, 0, 255)'}},
                {'x': tdata_start[0], 'y': tdata_start[5], 'type': 'bar', 'name': 'Diff L1 - A',
                 'legendgroup': 'Level 1', 'marker': {'color': 'rgb(0, 0, 255)'}},
                {'x': tdata_end[0], 'y': tdata_end[1], 'type': 'line', 'name': 'Total L1 - B',
                 'legendgroup': 'Level 1', 'marker': {'color': 'rgb(255, 123, 0)'}},
                {'x': tdata_end[0], 'y': tdata_end[5], 'type': 'bar', 'name': 'Diff L1 - B',
                 'legendgroup': 'Level 1', 'marker': {'color': 'rgb(255, 123, 0)'}},
                {'x': tdata_start[0], 'y': tdata_start[2], 'type': 'line', 'name': 'Total L2 - A',
                 'legendgroup': 'Level 2', 'marker': {'color': 'rgb(255, 0, 0)'}},
                {'x': tdata_start[0], 'y': tdata_start[6], 'type': 'bar', 'name': 'Diff L2 - A',
                 'legendgroup': 'Level 2', 'marker': {'color': 'rgb(255, 0, 0)'}},
                {'x': tdata_end[0], 'y': tdata_end[2], 'type': 'line', 'name': 'Total L2 - B',
                 'legendgroup': 'Level 2', 'marker': {'color': 'rgb(0, 255, 255)'}},
                {'x': tdata_end[0], 'y': tdata_end[6], 'type': 'bar', 'name': 'Diff L2 - B',
                 'legendgroup': 'Level 2', 'marker': {'color': 'rgb(0, 255, 255)'}},
                {'x': tdata_start[0], 'y': tdata_start[3], 'type': 'line', 'name': 'Total L3 - A',
                 'legendgroup': 'Level 3', 'marker': {'color': 'rgb(0, 0, 0)'}},
                {'x': tdata_start[0], 'y': tdata_start[7], 'type': 'bar', 'name': 'Diff L3 - A',
                 'legendgroup': 'Level 3', 'marker': {'color': 'rgb(0, 0, 0)'}},
                {'x': tdata_end[0], 'y': tdata_end[3], 'type': 'line', 'name': 'Total L3 - B',
                 'legendgroup': 'Level 3', 'marker': {'color': 'rgba(120, 120, 120)'}},
                {'x': tdata_end[0], 'y': tdata_end[7], 'type': 'bar', 'name': 'Diff L3 - B',
                 'legendgroup': 'Level 3', 'marker': {'color': 'rgb(120, 120, 120)'}},
                {'x': tdata_start[0], 'y': tdata_start[4], 'type': 'line', 'name': 'Total Bil - A',
                 'legendgroup': 'Billing', 'marker': {'color': 'rgb(0, 255, 0)'}},
                {'x': tdata_start[0], 'y': tdata_start[8], 'type': 'bar', 'name': 'Diff Bil - A',
                 'legendgroup': 'Billing', 'marker': {'color': 'rgb(0, 255, 0)'}},
                {'x': tdata_end[0], 'y': tdata_end[4], 'type': 'line', 'name': 'Total Bil - B',
                 'legendgroup': 'Billing', 'marker': {'color': 'rgb(255, 0, 255)'}},
                {'x': tdata_end[0], 'y': tdata_end[8], 'type': 'bar', 'name': 'Diff Bil - B',
                 'legendgroup': 'Billing', 'marker': {'color': 'rgb(255, 0, 255)'}},
            ],
            'layout': {
                      'title': 'Ticket Stats for A - ' + format_date(start_date) + ' and B - ' + format_date(end_date),
                      'plot_bgcolor': colors['background'],
                'xaxis': {'title': 'Hour Of The Day', 'tickmode': 'linear', 'dtick': 1},
                'yaxis': {'title': 'Ticket Count', 'tickmode': 'linear', 'dtick': 10},
                'legend': {'orientation': 'h', 'x': 0, 'y': -0.2, 'yanchor': 'top'},
                'barmode': 'overlay'
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
        start_dt = dt.strptime(start_date, '%Y-%m-%d')
        start_str = start_dt.strftime('%Y-%m-%d')
        end_dt = dt.strptime(end_date, '%Y-%m-%d')
        end_str = end_dt.strftime('%Y-%m-%d')
        x0 = getrange(start_dt, end_dt)
        tdata = get_date_range(start_date, end_date)
        figure = {
            'data': [
                {'x': x0, 'y': tdata['L1Total'], 'type': 'line', 'name': 'Total L1',
                 'legendgroup': 'Level 1', 'marker': {'color': 'rgb(0, 0, 255)'}},
                {'x': x0, 'y': tdata['L1Diff'], 'type': 'bar', 'name': 'Diff L1',
                 'legendgroup': 'Level 1', 'marker': {'color': 'rgb(0, 0, 255)'}},
                {'x': x0, 'y': tdata['L2Total'], 'type': 'line', 'name': 'Total L2',
                 'legendgroup': 'Level 2', 'marker': {'color': 'rgb(255, 0, 0)'}},
                {'x': x0, 'y': tdata['L2Diff'], 'type': 'bar', 'name': 'Diff L2',
                 'legendgroup': 'Level 2', 'marker': {'color': 'rgb(255, 0, 0'}},
                {'x': x0, 'y': tdata['L3Total'], 'type': 'line', 'name': 'Total L3',
                 'legendgroup': 'Level 3', 'marker': {'color': 'rgb(0, 255, 0)'}},
                {'x': x0, 'y': tdata['L3Diff'], 'type': 'bar', 'name': 'Diff L3',
                 'legendgroup': 'Level 3', 'marker': {'color': 'rgb(0, 255, 0)'}},
                {'x': x0, 'y': tdata['BilTotal'], 'type': 'line', 'name': 'Total Bil',
                 'legendgroup': 'Billing', 'marker': {'color': 'rgb(51, 51, 51)'}},
                {'x': x0, 'y': tdata['BilDiff'], 'type': 'bar', 'name': 'Diff Bil',
                 'legendgroup': 'Billing', 'marker': {'color': 'rgb(51, 51, 51)'}},
                      ],
            'layout': {
                      'title': 'Ticket Stats For Dates Between ' + format_date(start_date) + ' and ' + format_date(end_date),
                      'plot_bgcolor': colors['background'],
                'xaxis': {'title': 'Hour Of The Day', 'tickmode': 'array', 'type': 'category',},
                'yaxis': {'title': 'Ticket Count', 'tickmode': 'linear', 'dtick': 10},
                'legend': {'orientation': 'h', 'x': 0, 'y': -0.2, 'yanchor': 'top'},
                'barmode': 'overlay'
                      }
                  }
    return figure



# callback for tab 4
@app.callback(
    dash.dependencies.Output('graph-tab4', 'figure'),
    [dash.dependencies.Input('cal-tab4A', 'start_date'),
     dash.dependencies.Input('cal-tab4B', 'end_date')]
    )
def update_tab4(start_date, end_date):

    if end_date is not None:
        tdata_start = gettdata(format_date(start_date))
        tdata_end = gettdata(format_date(end_date))
        figure = {
            'data': [
                      {'x': tdata[0], 'y': tdata[13], 'type': 'line', 'name': 'Total L1', 'marker': {'color': 'rgb(0, 89, 234)'}},
                      {'x': tdata[0], 'y': tdata[17], 'type': 'bar', 'name': 'Diff L1', 'marker': {'color': 'rgb(0, 89, 234)'}},
                      ],
            'layout': {
                      'title': 'Ticket Stats',
                      'plot_bgcolor': colors['background'],
                'xaxis': {'title': 'Hour Of The Day', 'tickmode': 'linear', 'dtick': 1},
                'yaxis': {'title': 'Ticket Count', 'tickmode': 'linear', 'dtick': 10},
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
        app.run_server(debug=True)
