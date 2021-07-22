import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_trich_components as dtc
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from pandas.core.groupby.generic import DataFrameGroupBy
import loaders
import urllib
import dash_leaflet as dl
import plotly.graph_objects as go
from plotly.figure_factory import create_distplot

from app import app
from utils import paper_layout, clean_graph, get_connection, get_userdata, add_userdata
import climate
connection = get_connection()

@app.callback([Output('session-graph', 'data'), Output("history-container", "options")], 
              Input('input', 'value'), Input('children', 'n_clicks'), Input('reset', 'n_clicks'), Input('username', 'value'),
              State('session-graph', 'data'), State('nchildren', 'value'), State('cytoscape', 'tapNodeData'))
def populate_graph(value, children, reset, user, graph, slider, selected):
    ctx = dash.callback_context
    username = 'anonymous' if not user else user
    if value:
        add_userdata(connection, username, value['name'])
    history = get_userdata(connection, username=username)
    options = [{'label':v, 'value':v} for v in history['search'].values]
    if ctx.triggered[0]['prop_id']=='input.value':
        search_term = value
        backbone = loaders.get_backbone(value)
        if type(graph)==dict:
            graph.update({'backbone':backbone})
        else:
            graph = {'backbone':backbone}
        cyto = loaders.get_cyto_backbone(backbone)
        if 'graph' in graph:
            graph.update({'graph':clean_graph(graph['graph']+cyto)})
        else:
            graph.update({'graph':cyto})
    if ctx.triggered[0]['prop_id']=='children.n_clicks':
        if selected:
            taxon = selected['id']
            if 'offset' in graph and taxon in graph['offset']:
                offset = graph['offset'][taxon]
                graph['offset'][taxon] += slider                
            else:
                offset = 0
                if 'offset' in graph:
                    graph['offset'].update({taxon:slider})
                else:
                    graph.update({'offset':{taxon:slider}})
            child_nodes = loaders.get_children(selected,limit=slider, offset = offset)
            graph.update({'graph':clean_graph(graph['graph']+child_nodes)})
    if ctx.triggered[0]['prop_id']=='reset.n_clicks':
        if value:
            backbone = loaders.get_backbone(value)
            if type(graph)==dict:
                graph.update({'backbone':backbone})
            else:
                graph = {'backbone':backbone}
        elif 'backbone' in graph:
            backbone = graph['backbone']
        else:
            raise PreventUpdate
        cyto = loaders.get_cyto_backbone(backbone)
        graph.update({'graph':cyto, 'offset':{}})        
    return graph, options

@app.callback(Output('cytoscape', 'elements'), Input('session-graph', 'data'))
def display_graph(data):
    if data and 'graph' in data:
        return data['graph']
    else:
        return []

@app.callback(Output('wiki-body', 'children'), Input('cytoscape', 'tapNodeData'), State('username', 'value'))
def display_wiki(data, user):
    username = 'anonymous' if not user else user
    if not data:
        return html.P('No Node Selected')
    else:
        add_userdata(connection, username, data['label'])
        taxon = int(data['id'])
        wiki = loaders.get_wiki_info(taxon)
        if wiki:
            try:
                summary = wiki['page'].summary
            except:
                summary = ''
            try:
                url = wiki['page'].url
            except:
                url = ''
            label = wiki['label'].capitalize() if wiki['label'] else ''
            desc = wiki['description'].capitalize() if wiki['description'] else ''
            element = html.Div([
                html.H4(label),
                html.H6(desc),
                dbc.Row([
                    html.Img(src=wiki['image'], height='300px', style={'padding':'5px'}),
                    html.Img(src=wiki['range'], height='300px', style={'padding':'5px'})],
                        no_gutters=True,
                        style={'padding':'auto'}),
                html.P(summary, style={'padding':'5px', 'font-size':14}),
                dbc.Row([
                    html.P('Source:', style={'padding':'5px', 'font-size':12}),
                    dcc.Link('Wikipedia', href=url, target='_blank', style={'padding':'5px', 'font-size':12}),
                    dcc.Link('Wikidata', href=wiki['wikidata'], target='_blank', style={'padding':'5px', 'font-size':12}),
                    ],
                    no_gutters=True,
                    style={'padding':'auto'})
            ])
        else:
            element = html.Div('No Wikidata element found')
            '''
            wiki = loaders.get_wiki(taxon)
            element = html.Div([
                html.P('No Wikidata element found. Result from Wikipedia instead.', style={'padding':'5px', 'font-size':12}),
                html.H4(wiki[0].title),
                html.Img(src=wiki[1], height='300px', style={'padding':'5px'}),
                html.P(wiki[0].summary, style={'padding':'5px', 'font-size':14}),
                dbc.Row([
                    html.P('Source:', style={'padding':'5px', 'font-size':12}),
                    dcc.Link('Wikipedia', href=wiki[0].url, target='_blank', style={'padding':'5px', 'font-size':12})
                ],
                    no_gutters=True,
                    style={'padding':'auto'})
            ])            
            '''
        return element

@app.callback(Output('images-body', 'children'), Input('cytoscape', 'tapNodeData'))
def display_images(data):
    if not data:
        return html.P('No Node Selected')
    else:
        images = loaders.get_images(int(data['id']),limit=12)
        divs = [html.Div(html.Img(src=im, height='300px'), style={'padding':'5px'}) for im in images]
        carousel = dtc.Carousel(divs,
                    slides_to_scroll=1,
                    swipe_to_slide=True,
                    autoplay=True,
                    speed=0,
                    variable_width=True,
                    center_mode=True,
                    arrows=False,
                    dots=True
                )
        element = html.Div([
            carousel,
            html.P('Source: GBIF', style={'padding':'5px', 'font-size':14}),
        ])
        return element

@app.callback(Output('links-body', 'children'), Input('cytoscape', 'tapNodeData'))
def display_links(data):
    if not data:
        return html.P('No Node Selected')
    else:
        taxon = data['id']
        name = data['label']
        url = "https://www.gbif.org/species/"+taxon
        links = {'GBIF':url}

        url = "https://search.crossref.org/?q={}&from_ui=yes".format(name.replace(' ','+'))
        links.update({'CrossRef':url})

        url = 'https://academic.microsoft.com/search?q={}&f=&orderBy=0&skip=0&take=10'.format(urllib.parse.quote(name))
        links.update({'Microsoft Academic':url})

        val = name.replace(' ','%20')
        url = "https://www.semanticscholar.org/search?q={}&sort=relevance".format(val)
        links.update({'Semantic Scholar':url})

        val = name.replace(' ','%20')
        url = "https://www.lens.org/lens/search/scholar/list?q={}".format(val)
        links.update({'Lens':url})

        val = name.replace(' ','+')
        url = "https://scholar.google.com/scholar?as_vis=0&q={}&hl=en&as_sdt=0,5".format(val)
        links.update({'Google Scholar':url})

        url = "https://www.base-search.net/Search/Results?lookfor={}&name=&oaboost=1&newsearch=1&refid=dcbasen".format(name.replace(' ','+'))
        links.update({'BASE':url})

        url = "https://app.dimensions.ai/discover/publication?search_mode=content&search_text={}&search_type=kws&search_field=full_search".format(urllib.parse.quote(name))
        links.update({'Dimensions':url})

        divs = [html.Li(dcc.Link(k, href=v, target='_blank')) for k,v in links.items()]
        element = html.Div(divs)
        return element

@app.callback(Output('resources-body', 'children'), Input('cytoscape', 'tapNodeData'))
def display_resources(data):
    if not data:
        return html.P('No Node Selected')
    else:
        name = data['label']
        return html.Div([dbc.Tabs(
        [
            dbc.Tab(html.Embed(src="https://tree.opentreeoflife.org/", className='resources-container'), label="Tree of Life"),
            dbc.Tab(html.Embed(src="https://eol.org/search?q={}".format(name.replace(' ','+')),className='resources-container'), label="EOL"),
            dbc.Tab(html.Embed(src="https://www.onezoom.org/AT/@biota=93302?img=best_any&anim=jump#x775,y1113,w1.4450", className='resources-container'), label="OneZoom"),
            dbc.Tab(html.Embed(src="https://openknowledgemaps.org/",className='resources-container'), label="Open Knowledge Map")
        ])])


@app.callback(Output('maps-body', 'children'), Input('cytoscape', 'tapNodeData'))
def display_map(data):
    if not data:
        return html.P('No Node Selected')
    else:
        taxon = data['id']        
        url_ = "https://api.gbif.org/v2/map/occurrence/density/{z}/{x}/{y}@2x.png?srs=EPSG:3857&bin=hex&hexPerTile=64&style=purpleYellow-noborder.poly&taxonKey="+taxon
        element = html.Div([
            dl.Map([
                #dl.TileLayer(url=url, maxZoom=10, attribution=attribution),
                dl.TileLayer(),
                dl.TileLayer(url=url_, maxZoom=10),
                dl.EasyButton(icon='fa-home', n_clicks=0, id="btn")
                ], zoom=2, animate=False, className='map', id='map')
        ], className='map-div')   
        return element

@app.callback(Output("map", "center"),
              Output("map", "zoom"),
              [Input("btn", "n_clicks")])
def easy_btn(click):
    center = [-6.7, 0]
    zoom = 2
    return center, zoom

 
@app.callback(Output('session-paper', 'data'), Input('cytoscape', 'tapNodeData'), Input('papers-next', 'n_clicks'), Input('papers-reset', 'n_clicks'),  State('session-paper', 'data'), State('graph-size','value'))
def get_papers(selected, next, reset, data, value):
    ctx = dash.callback_context
    if not selected:
        return {}
    else:
        if ctx.triggered[0]['prop_id']=='papers-next.n_clicks':      
            offset = 0 if 'offset' not in data else data['offset']        
        #elif ctx.triggered[0]['prop_id']=='papers-next-2.n_clicks':      
        #    offset = 0 if 'offset' not in data else data['offset']
        elif ctx.triggered[0]['prop_id']=='papers-reset.n_clicks':
            offset = 0
        elif ctx.triggered[0]['prop_id']=='cytoscape.tapNodeData':
            offset = 0 if 'offset' not in data else data['offset']
        else:
            raise PreventUpdate
        elements, papers = loaders.get_neo_papers(int(selected['id']),limit=value, offset=offset)
        data.update({'paper_graph':elements, 'papers':papers, 'offset':offset+value})        
        return data

@app.callback(Output('papers-body', 'children'), Input('session-paper', 'data'))
def display_papers(data):
    if not data or 'papers' not in data:
        return html.P('No Node Selected')
    else:
        if len(data['papers'])==0:
            return 'No (more) Papers Found'
        paper_divs = [paper_layout(k,paper) for k,paper in data['papers'].items()]
        element = html.Div(paper_divs, className='paper-tab')
        return element

@app.callback(Output('cyto-paper', 'elements'), Input('session-paper', 'data'))
def display_paper_graph(data):
    if data and'paper_graph' in data:
        return data['paper_graph']
    else:
        return []

@app.callback(
    Output("cyto-paper", "generateImage"),
    Input("papers-png", "n_clicks"),
    prevent_initial_call=True)
def paper_png(n_clicks):
    return {
        'type': 'png',
        'action': 'download'
        }

@app.callback(
    Output("cytoscape", "generateImage"),
    Input("graph-png", "n_clicks"),
    prevent_initial_call=True)
def paper_png(n_clicks):
    return {
        'type': 'png',
        'action': 'download'
        }        

@app.callback(Output('cytoscape','zoom'), Input('graph-zoom', 'value'))
def graph_zoom(zoom):
    return zoom

@app.callback(Output('cyto-paper','zoom'), Input('paper-zoom', 'value'))
def paper_zoom(zoom):
    return zoom    

@app.callback(Output('climate-box-plot', 'figure'), Input('cytoscape', 'tapNodeData'), Input('climate-radio', 'value'))
def display_climate(data, value):
    fig = go.Figure()
    if data:
        taxon = int(data['id'])
        distribution = climate.get_taxon_distribution(taxon)
        df, vstat = climate.calc_stat(value, distribution)
        if value=='Elevation':
            fig = create_distplot([vstat], ['Altitude Distribution (meters)'])
        else:
            for col in df:
                fig.add_trace(go.Box(y=df[col].values, name=df[col].name))
    return fig