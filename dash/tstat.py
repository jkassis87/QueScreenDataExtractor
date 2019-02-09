import dash
import dash_core_components as dcc
import dash_html_components as html
import csv

f = open('2019-2-5.csv', 'r')
csvfile = csv.reader(f)
tdata = list(csvfile)

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Dash Tutorials'),
    dcc.Graph(id = 'L1 Total',
              figure = {
                  'data': [
                      {'x': tdata[0], 'y': tdata[13], 'type': 'line', 'name': 'Total'},
                      {'x': tdata[0], 'y': tdata[17], 'type': 'bar', 'name': 'Total'},
                      ],
                  'layout': {
                      'title': 'DP L1 Ticket Stats'
                      }
                  }
              )
])

dcc.Graph(
    id = 'L1 Total',
    figure = {
        'data': [
            {'x': tdata[0], 'y': tdata[13], 'type': 'line', 'name': 'Total'},
            {'x': tdata[0], 'y': tdata[17], 'type': 'line', 'name': 'Total'},
            ],
        'layout': {
            'title': 'DP L1 Ticket Stats'
            }
        }
    )

if __name__ == '__main__':
    app.run_server(debug=True)
