import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import csv
from datetime import datetime as dt
from datetime import timedelta
import re

app = dash.Dash(__name__)

colors = {
    'background': '#FFFFFF',
}

app.layout = html.Div(children=[
    dcc.DatePickerSingle(
        id = 'callendar-1',
        min_date_allowed = dt(2019, 1, 15),
        max_date_allowed = dt(2019, 2, 16),
        initial_visible_month = dt(2019, 2, 16),
        date = dt(2019, 2, 15)),
    html.Div(id = 'callendar-output'),
    dcc.Graph(id = 'Daily-Ticket-Stats',
#              figure = {
#                  'data': [
#                      {'x': get_csv(date)[0], 'y': get_csv(date)[13], 'type': 'line', 'name': 'Total L1', 'marker': {'color': 'rgb(0, 89, 234)'}},
#                      {'x': get_csv(date)[0], 'y': get_csv(date)[17], 'type': 'bar', 'name': 'Diff L1', 'marker': {'color': 'rgb(0, 89, 234)'}},
#                      ],
#                  'layout': {
#                      'title': 'Ticket Stats',
#                      'plot_bgcolor': colors['background'],
#                      }
#                  }
              )
])

@app.callback(
    dash.dependencies.Output('Daily-Ticket-Stats', 'figure'),
    [dash.dependencies.Input('callendar-1', 'date')]
    )
def update_output(date):

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


if __name__ == '__main__':
    app.run_server(debug=True)
