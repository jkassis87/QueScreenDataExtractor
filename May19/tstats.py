import dash, re, csv, sqlite3
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from datetime import datetime as dt
from datetime import timedelta
from datetime import date as dtm
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
            date + ' 20' + ss, date + ' 21' + ss, date + ' 22' + ss, date + ' 23' + ss]
        ]

    for t in tteams:
        stats_add = []
        for x in stats[0]:
            conn = sqlite3.connect("tdatadb.sqlite")
            curs = conn.cursor()
            query = "SELECT Stat FROM AllData WHERE Brand = ? AND Date = ?;"
            curs.execute(query, (t,x))
            y = curs.fetchone()
            #print(y)
            stats_add.extend(y)

        stats.append(stats_add)

    #for x in stats:
    #    print(x)
    #    print(str(len(x)))
    return (stats)


app.layout = html.Div([
    dcc.Tabs(id="tabs", children=[

        # START Tab 1 - Single Day Stats
        dcc.Tab(label='Single Day', children=[
            html.Div([
                dcc.DatePickerSingle(
                    id='cal-tab1',
                    min_date_allowed=dt(2019, 1, 15),
                    max_date_allowed=dt(now.year, now.month, now.day),
                    initial_visible_month=dt(now.year, now.month, now.day),
                    date=dt(now.year, now.month, now.day),
                    display_format='MMMM Y, DD'
                ),
                dcc.Graph(
                    id='graph-tab1',
                )
            ])
        ]),
        # END Tab 1

        # START Tab 2 - Compare 2 Days
        dcc.Tab(label='Compare 2 Days', children=[
            dcc.DatePickerRange(
                id='cal-tab2',
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
        # END Tab 2

        # START Tab 3 - Single Date Range
        dcc.Tab(label='Date Range', children=[
            dcc.DatePickerRange(
                id='cal-tab3',
                min_date_allowed=dt(2019, 1, 15),
                max_date_allowed=dt(now.year, now.month, now.day),
                initial_visible_month=dt(now.year, now.month, now.day),
                start_date=dt(now.year, now.month, now.day),
                end_date=dt(now.year, now.month, now.day)
            ),
            dcc.Graph(
                id='graph-tab3',
            )
        ])
        # END Tab 3

    ])
])



# START callback for tab 1
@app.callback(
    dash.dependencies.Output('graph-tab1', 'figure'),
    [dash.dependencies.Input('cal-tab1', 'date')]
    )
def update_tab1(date):

    if date is not None:
        tdata = gettdata(date)
        for x in tdata:
            print(x)
        # data for Tab 1
        figure = {
            'data': [
                {'x': tdata[0], 'y': tdata[1], 'name': 'Total L1', 'legendgroup': 'Level 1', 'marker': {'color': 'rgb(0, 0, 255)'}},
                {'x': tdata[0], 'y': tdata[2], 'name': 'Total L2', 'legendgroup': 'Level 2', 'marker': {'color': 'rgb(255, 0, 0)'}},
                {'x': tdata[0], 'y': tdata[3], 'name': 'Total L3', 'legendgroup': 'Level 3', 'marker': {'color': 'rgb(0, 255, 0)'}},
                {'x': tdata[0], 'y': tdata[4], 'name': 'Total Bil', 'legendgroup': 'Billing', 'marker': {'color': 'rgb(51, 51, 51)'}},
        ],

            # Layout for tab 1
            'layout': {
                      'title': 'Ticket Stats For ' + parser.parse(date).strftime("%A") + ' ' + date,
                      'plot_bgcolor': colors['background'],
                'xaxis': {'title': 'Hour Of The Day', 'tickmode': 'array', 'dtick': 1, 'tickformat': '%H'},
                'yaxis': {'title': 'Ticket Count', 'tickmode': 'linear', 'dtick': 10},
                'legend': {'orientation': 'h', 'x': 0, 'y': -0.2, 'yanchor': 'top'}
                      }
                  }
    return figure
# END callback for Tab 1


# START callback for tab 2
@app.callback(
    dash.dependencies.Output('graph-tab2', 'figure'),
    [dash.dependencies.Input('cal-tab2', 'start_date'),
    dash.dependencies.Input('cal-tab2', 'end_date')
     ]
    )
def update_tab2(start_date, end_date):

    if start_date is not None and end_date is not None:
        tdata_start = gettdata(start_date)
        tdata_end = gettdata(end_date)
        hr_list = list(range(0, 25))

        # Data for tab 2
        figure = {
            'data': [
                {'x': hr_list, 'y': tdata_start[1],'name': 'Total L1 - A', 'legendgroup': 'Level 1', 'marker': {'color': 'rgb(0, 0, 255)'}},
                {'x': hr_list, 'y': tdata_end[1], 'name': 'Total L1 - B', 'legendgroup': 'Level 1', 'marker': {'color': 'rgb(255, 123, 0)'}},

                {'x': hr_list, 'y': tdata_start[2], 'name': 'Total L2 - A', 'legendgroup': 'Level 2', 'marker': {'color': 'rgb(255, 0, 0)'}},
                {'x': hr_list, 'y': tdata_end[2], 'type': 'line', 'name': 'Total L2 - B', 'legendgroup': 'Level 2', 'marker': {'color': 'rgb(0, 255, 255)'}},

                {'x': hr_list, 'y': tdata_start[3],'name': 'Total L3 - A', 'legendgroup': 'Level 3', 'marker': {'color': 'rgb(0, 0, 0)'}},
                {'x': hr_list, 'y': tdata_end[3], 'name': 'Total L3 - B', 'legendgroup': 'Level 3', 'marker': {'color': 'rgba(120, 120, 120)'}},

                {'x': hr_list, 'y': tdata_start[4], 'name': 'Total Bil - A', 'legendgroup': 'Billing', 'marker': {'color': 'rgb(0, 255, 0)'}},
                {'x': hr_list, 'y': tdata_end[4], 'name': 'Total Bil - B', 'legendgroup': 'Billing', 'marker': {'color': 'rgb(255, 0, 255)'}},
            ],

            # Layout of Tab 2
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
# END Callback for Tab 2

# START callback for tab 3
@app.callback(
    dash.dependencies.Output('graph-tab3', 'figure'),
    [dash.dependencies.Input('cal-tab3', 'start_date'),
    dash.dependencies.Input('cal-tab3', 'end_date')
     ]
    )
def update_tab3(start_date, end_date):

    if start_date is not None and end_date is not None:

        # start_date and end_date as a datetime function
        start_dt = dt.strptime(start_date, '%Y-%m-%d')
        end_dt = dt.strptime(end_date, '%Y-%m-%d')

        # gets data of first date
        tdata = gettdata(start_date)

        while start_dt < end_dt:
            start_dt += timedelta(days=1)
            date_string = start_dt.strftime('%Y-%m-%d')
            date_data = gettdata(date_string)
            for a, b in zip(tdata, date_data):
                a.extend(b)
        for x in tdata:
            print(x)
        # data for Tab 3
        figure = {
            'data': [
                {'x': tdata[0], 'y': tdata[1], 'name': 'Total L1', 'legendgroup': 'Level 1', 'marker': {'color': 'rgb(0, 0, 255)'}},
                {'x': tdata[0], 'y': tdata[2], 'name': 'Total L2', 'legendgroup': 'Level 2', 'marker': {'color': 'rgb(255, 0, 0)'}},
                {'x': tdata[0], 'y': tdata[3], 'name': 'Total L3', 'legendgroup': 'Level 3', 'marker': {'color': 'rgb(0, 255, 0)'}},
                {'x': tdata[0], 'y': tdata[4], 'name': 'Total Bil', 'legendgroup': 'Billing', 'marker': {'color': 'rgb(51, 51, 51)'}},
        ],

            # Layout for tab 3
            'layout': {
                      'title': 'Ticket Stats For ' + parser.parse(start_date).strftime("%A") + ' ' + start_date,
                      'plot_bgcolor': colors['background'],
                'xaxis': {'title': 'Hour Of The Day', 'tickmode': 'array', 'dtick': 1, 'tickformat': '%Y-%m-%d %H'},
                'yaxis': {'title': 'Ticket Count', 'tickmode': 'linear', 'dtick': 10},
                'legend': {'orientation': 'h', 'x': 0, 'y': -0.2, 'yanchor': 'top'}
                      }
                  }
    return figure
# END callback for tab 3


if __name__ == '__main__':
    app.run_server(debug=True)
