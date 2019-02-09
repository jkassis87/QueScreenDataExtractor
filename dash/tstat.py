import dash
import dash_core_components as dcc
import dash_html_components as html
import csv

f = open('2019-2-5.csv', 'r')
csvfile = csv.reader(f)
tdata = list(csvfile)

app = dash.Dash()

colors = {
    'background': '#FFFFFF',
    'text': '#111111'
}

app.layout = html.Div(children=[
    html.H1(children='Dash Tutorials'),
    dcc.Graph(id = 'L1 Total',
              figure = {
                  'data': [
                      {'x': tdata[0], 'y': tdata[13], 'type': 'line', 'name': 'Total L1', 'marker': {'color': 'rgb(0, 89, 234)'}},
                      {'x': tdata[0], 'y': tdata[17], 'type': 'bar', 'name': 'Diff L1', 'marker': {'color': 'rgb(0, 89, 234)'}},
                      {'x': tdata[0], 'y': tdata[14], 'type': 'line', 'name': 'Total L2', 'marker': {'color': 'rgb(234, 0, 0)'}},
                      {'x': tdata[0], 'y': tdata[18], 'type': 'bar', 'name': 'Diff L2', 'marker': {'color': 'rgb(234, 0, 0)'}},
                      {'x': tdata[0], 'y': tdata[15], 'type': 'line', 'name': 'Total L3', 'marker': {'color': 'rgb(0, 234, 15)'}},
                      {'x': tdata[0], 'y': tdata[19], 'type': 'bar', 'name': 'Diff L3', 'marker': {'color': 'rgb(0, 234, 15)'}},
                      {'x': tdata[0], 'y': tdata[16], 'type': 'line', 'name': 'Total Bil', 'marker': {'color': 'rgb(246, 0, 255)'}},
                      {'x': tdata[0], 'y': tdata[20], 'type': 'bar', 'name': 'Diff Bil', 'marker': {'color': 'rgb(246, 0, 255)'}},
                      ],
                  'layout': {
                      'title': 'Hostopia Ticket Stats',
                      'plot_bgcolor': colors['background'],
                      }
                  }
              )
])


if __name__ == '__main__':
    app.run_server(debug=True)
