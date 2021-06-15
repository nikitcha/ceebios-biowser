import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import phylo_tree

taxon_tab = html.Div([
    dcc.Store(id='session-graph', storage_type='session'),   
    dbc.Row([
        cyto.Cytoscape(
                id='cytoscape',        
                layout = {'name': 'cose'},
                elements = [],
                stylesheet= phylo_tree.default_stylesheet,
                style={'width': '100%', 'height': '800px'},
                zoomingEnabled=True,
                maxZoom=4,
                minZoom=1,
                zoom=2,
                userZoomingEnabled=False
            )         
    ],id='taxon-graph'),
    dbc.Row(children = [
        dbc.ButtonGroup([
            dbc.Button("Get Children", id='children'),
            dbc.Button("Reset", id='reset'),
            dbc.Button("PNG", id='graph-png')],
            size='sm',
            style={'padding-left':'40px'}),
        ]),
    dbc.Row([
        dbc.Col(html.Div('Children:',style={'padding-left':'30px' ,'fontSize':14})),
        dbc.Col(dcc.Slider(id='nchildren', min=1, max=50, step=1, value=10, marks={1:'1',50:'50'}))
        ], style={'width':'260px'}),
    dbc.Row([
        dbc.Col(html.Div('Zoom:', style={'padding-left':'30px' ,'fontSize':14})),
        dbc.Col(dcc.Slider(id='graph-zoom', min=1, max=4, step=1, value=2, marks={i:str(i) for i in range(1,5)})),
        ], style={'width':'260px'}),    
    ])

paper_tab = html.Div([
    dcc.Store(id='session-paper', storage_type='session'),   
    dbc.Row([
        cyto.Cytoscape(
                id='cyto-paper',        
                layout = {'name': 'cose'},
                elements = [],
                stylesheet= phylo_tree.default_stylesheet,
                style={'width': '100%', 'height': '800px'},
                zoomingEnabled=True,
                maxZoom=4,
                minZoom=1,
                zoom=2,
                userZoomingEnabled=False
            )            
    ],id='paper-graph-container'),
    dbc.Row(children = [
        dbc.ButtonGroup([
            dbc.Button("Next", id='papers-next'),
            dbc.Button("Reset", id='papers-reset'),
            dbc.Button("PNG", id='papers-png')],
            size='sm',
            style={'padding-left':'50px'}),
        dbc.Col(html.Div('Graph Size:',style={'padding-left':'30px' ,'fontSize':14})),
        dbc.Col(dcc.Slider(id='graph-size', min=10, max=200, step=1, value=100, marks={10:'10',200:'200'})),
        dbc.Col(html.Div('Zoom Level:', style={'padding-left':'30px' ,'fontSize':14})),
        dbc.Col(dcc.Slider(id='paper-zoom', min=1, max=4, step=1, value=2, marks={i:str(i) for i in range(1,5)})),
        ], justify='start')
    ])

graph_layout = html.Div([
    dbc.Tabs([
        dbc.Tab(taxon_tab, label='Taxon Graph'),
        dbc.Tab(paper_tab, label='Paper Graph')
        ])
    ], style={'width':'50%', 'padding-left':'15px'})    