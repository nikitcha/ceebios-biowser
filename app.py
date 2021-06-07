import json
import dash
import dash_cytoscape as cyto
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
import phylo_tree
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import loaders
import layout

#external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.LITERA])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('session_graph', 'data'), Input('input', 'value'), Input('nchildren', 'value'), Input('children', 'n_clicks'), Input('reset', 'n_clicks'), State('session_selected', 'data'), State('session_graph', 'data'))
def populate_graph(value, slider, children, reset, selected, graph):
    ctx = dash.callback_context
    if ctx.triggered[0]['prop_id']=='nchildren.value':
        raise PreventUpdate
    if ctx.triggered[0]['prop_id']=='input.value':
        value = ctx.triggered[0]['value']
        backbone = loaders.get_backbone(value)
        if type(graph)==dict:
            graph.update({'backbone':backbone})
        else:
            graph = {'backbone':backbone}
        cyto = loaders.get_cyto_backbone(backbone)
        graph.update({'graph':cyto})
    if ctx.triggered[0]['prop_id']=='children.n_clicks':
        child_nodes = loaders.get_children(selected,limit=slider)
        graph.update({'graph':graph['graph']+child_nodes})
    return graph

@app.callback(Output('graph_display', 'children'), Input('session_graph', 'data'))
def display_graph(data):
    if data and 'graph' in data:
        return cyto.Cytoscape(
                id='cytoscape',        
                layout = {'name': 'cose'},
                elements = data['graph'],
                stylesheet= phylo_tree.default_stylesheet,
                style={'width': '100%', 'height': '800px'}
            )        
    else:
        return html.Div(id='cytoscape', style={'width': '100%', 'height': '800px'})

    
@app.callback(Output('session_selected', 'data'), Input('cytoscape', 'tapNodeData'), State('session_selected', 'data'))
def update_selected(selected, data):
    if not data:
        data = {'selected':selected}
    else:
        data.update({'selected':selected})
    print(data)
    return data


# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/explore':
        return layout.explore_page
    else:
        return  layout.index_page
    # You could also return a 404 "URL not found" page here



if __name__ == '__main__':
    app.run_server(debug=True)