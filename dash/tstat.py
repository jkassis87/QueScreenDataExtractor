import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import csv
from datetime import datetime as dt
from datetime import timedelta

now = dt.now() - timedelta(1)
date = (str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '.csv')

def get_csv(date):
    f = open(date, 'r')
    csvfile = csv.reader(f)
    tdata = list(csvfile)
    return(tdata)

app = dash.Dash(__name__)

colors = {
    'background': '#FFFFFF',
    'text': '#111111'
}

app.layout = html.Div(children=[
    dcc.DatePickerSingle(
        id = 'date picker single',
        min_date_allowed = dt(2019, 1, 11),
        max_date_allowed = now,
        initial_visible_month = now,
        date = dt(2019, 1, 12)),
    html.Div(id='output-container-date-picker-single'),
    dcc.Graph(id = 'L1 Total',
              figure = {
                  'data': [
                      {'x': get_csv(date)[0], 'y': get_csv(date)[13], 'type': 'line', 'name': 'Total L1', 'marker': {'color': 'rgb(0, 89, 234)'}},
                      {'x': get_csv(date)[0], 'y': get_csv(date)[17], 'type': 'bar', 'name': 'Diff L1', 'marker': {'color': 'rgb(0, 89, 234)'}},
                      {'x': get_csv(date)[0], 'y': get_csv(date)[14], 'type': 'line', 'name': 'Total L2', 'marker': {'color': 'rgb(234, 0, 0)'}},
                      {'x': get_csv(date)[0], 'y': get_csv(date)[18], 'type': 'bar', 'name': 'Diff L2', 'marker': {'color': 'rgb(234, 0, 0)'}},
                      {'x': get_csv(date)[0], 'y': get_csv(date)[15], 'type': 'line', 'name': 'Total L3', 'marker': {'color': 'rgb(0, 234, 15)'}},
                      {'x': get_csv(date)[0], 'y': get_csv(date)[19], 'type': 'bar', 'name': 'Diff L3', 'marker': {'color': 'rgb(0, 234, 15)'}},
                      {'x': get_csv(date)[0], 'y': get_csv(date)[16], 'type': 'line', 'name': 'Total Bil', 'marker': {'color': 'rgb(246, 0, 255)'}},
                      {'x': get_csv(date)[0], 'y': get_csv(date)[20], 'type': 'bar', 'name': 'Diff Bil', 'marker': {'color': 'rgb(246, 0, 255)'}},
                      ],
                  'layout': {
                      'title': 'Hostopia Ticket Stats',
                      'plot_bgcolor': colors['background'],
                      }
                  }
              )
])

@app.callback(
    dash.dependencies.Output('output-container-date-picker-single', 'children'),
    [dash.dependencies.Input('date picker single', 'date')])

def update_output(date):
    if date is not None:
        now = dt.now()
        date = (str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '.csv')
    return date

if __name__ == '__main__':
    app.run_server(debug=True)
