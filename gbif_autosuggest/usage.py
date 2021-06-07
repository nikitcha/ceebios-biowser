import gbif_autosuggest
import dash
from dash.dependencies import Input, Output
import dash_html_components as html

app = dash.Dash(__name__)

app.layout = html.Div([
    gbif_autosuggest.GbifAutosuggest(
        id='input',
        value='initial value',
        label='my-label'
    ),
    html.Div(id='output')
])


@app.callback(Output('output', 'children'), [Input('input', 'value')])
def display_output(value):
    if type(value)==dict:
        value = '; '.join([k+':'+str(v) for k,v in value.items()])
    return value


if __name__ == '__main__':
    app.run_server(debug=True)
