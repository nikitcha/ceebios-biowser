import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

taxon_tab = html.Div([
    html.Div(id='graph_display'),
    dbc.Row(children = [
        dbc.ButtonGroup([
            dbc.Button("Get Children", id='children'),
            dbc.Button("Reset", id='reset')],
            size='sm',
            style={'padding-left':'50px'}),
        ]),
    dbc.Col(dcc.Slider(id='nchildren', min=1, max=50, step=1, value=10, marks={1:'1',50:'50'}), 
    style={'width':'200px'})])

paper_tab = html.Div([html.P('Paper Graph')])

graph_layout = html.Div([
    dbc.Tabs([
        dbc.Tab(taxon_tab, label='Taxon Graph'),
        dbc.Tab(paper_tab, label='Paper Graph')
        ])
    ], style={'width':'50%', 'padding-left':'15px'})    