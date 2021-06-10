import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import phylo_tree

taxon_tab = html.Div([
    html.Div([
        dcc.Store(id='session-graph', storage_type='session'),        
        cyto.Cytoscape(
                id='cytoscape',        
                layout = {'name': 'cose'},
                elements = [],
                stylesheet= phylo_tree.default_stylesheet,
                style={'width': '100%', 'height': '800px'}
            )         
    ],id='taxon-graph'),
    dbc.Row(children = [
        dbc.ButtonGroup([
            dbc.Button("Get Children", id='children'),
            dbc.Button("Reset", id='reset')],
            size='sm',
            style={'padding-left':'50px'}),
        ]),
    dbc.Col(dcc.Slider(id='nchildren', min=1, max=50, step=1, value=10, marks={1:'1',50:'50'}), 
    style={'width':'200px'})])

paper_tab = html.Div([
    dcc.Store(id='session-paper', storage_type='session'),    
    html.Div(id='paper-graph-container'),
    dbc.Row(children = [
        dbc.ButtonGroup([
            dbc.Button("Next", id='papers-next'),
            dbc.Button("Reset", id='papers-reset')],
            size='sm',
            style={'padding-left':'50px'}),
        ]),
    dbc.Col(dcc.Slider(id='graph-size', min=1, max=200, step=1, value=100, marks={1:'1',200:'200'}), 
    style={'width':'200px'})])

graph_layout = html.Div([
    dbc.Tabs([
        dbc.Tab(taxon_tab, label='Taxon Graph'),
        dbc.Tab(paper_tab, label='Paper Graph')
        ])
    ], style={'width':'50%', 'padding-left':'15px'})    