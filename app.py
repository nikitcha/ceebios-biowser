import json
import dash
import dash_cytoscape as cyto
import dash_html_components as html
import dash_core_components as dcc
import dash_trich_components as dtc
from dash.dependencies import Output, Input, State
import phylo_tree
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import loaders
import layout
import urllib
import dash_leaflet as dl

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

@app.callback(Output('taxon-graph', 'children'), Input('session_graph', 'data'))
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
        return html.P('No Node Selected')

    
@app.callback(Output('session_selected', 'data'), Input('cytoscape', 'tapNodeData'), State('session_selected', 'data'))
def update_selected(selected, data):
    print(selected)
    if selected:
        return {'selected':selected}

@app.callback(Output('wiki-body', 'children'), Input('session_selected', 'data'))
def display_wiki(data):
    if not data or not data['selected']:
        return html.P('No Node Selected')
    else:
        taxon = int(data['selected']['id'])
        try:
            wiki = loaders.get_wiki_info(taxon)
            element = html.Div([
                html.H4(wiki['label'].capitalize()),
                html.H6(wiki['description'].capitalize()),
                dbc.Row([
                    html.Img(src=wiki['image'], height='300px', style={'margin':'5px'}),
                    html.Img(src=wiki['range'], height='300px', style={'margin':'5px'})],
                        no_gutters=True,
                        style={'margin':'auto'}),
                html.P(wiki['page'].summary, style={'margin':'5px', 'fontSize':14}),
                dbc.Row([
                    html.P('Source:', style={'margin':'5px', 'fontSize':12}),
                    dcc.Link('Wikipedia', href=wiki['page'].url, target='_blank', style={'margin':'5px', 'fontSize':12}),
                    dcc.Link('Wikidata', href=wiki['wikidata'], target='_blank', style={'margin':'5px', 'fontSize':12}),
                    ],
                    no_gutters=True,
                    style={'margin':'auto'})
            ])
        except:
            wiki = loaders.get_wiki(taxon)
            element = html.Div([
                html.P('No Wikidata element found. Result from Wikipedia instead.', style={'margin':'5px', 'fontSize':12}),
                html.H4(wiki[0].title),
                html.Img(src=wiki[1], height='300px', style={'margin':'5px'}),
                html.P(wiki[0].summary, style={'margin':'5px', 'fontSize':14}),
                dbc.Row([
                    html.P('Source:', style={'margin':'5px', 'fontSize':12}),
                    dcc.Link('Wikipedia', href=wiki[0].url, target='_blank', style={'margin':'5px', 'fontSize':12})
                ],
                    no_gutters=True,
                    style={'margin':'auto'})
            ])            
        return element

@app.callback(Output('images-body', 'children'), Input('session_selected', 'data'))
def display_images(data):
    if not data or not data['selected']:
        return html.P('No Node Selected')
    else:
        images = loaders.get_images(int(data['selected']['id']),limit=8)
        divs = [html.Div(html.Img(src=im, height='300px'), style={'margin':'5px'}) for im in images]
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
            html.P('Source: GBIF', style={'margin':'5px', 'fontSize':14}),
        ])
        return element

@app.callback(Output('links-body', 'children'), Input('session_selected', 'data'))
def display_links(data):
    if not data or not data['selected']:
        return html.P('No Node Selected')
    else:
        taxon = data['selected']['id']
        name = data['selected']['label']
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

@app.callback(Output('maps-body', 'children'), Input('session_selected', 'data'))
def display_map(data):
    if not data or not data['selected']:
        return html.P('No Node Selected')
    else:
        taxon = data['selected']['id']        
        url = 'https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png'
        attribution = '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a> '
        url_ = "https://api.gbif.org/v2/map/occurrence/density/{z}/{x}/{y}@2x.png?srs=EPSG:3857&bin=hex&hexPerTile=64&style=purpleYellow-noborder.poly&taxonKey="+taxon
        element = html.Div([
            dl.Map([
                dl.TileLayer(url=url, maxZoom=10, attribution=attribution),
                dl.TileLayer(url=url_, maxZoom=10),
                ], zoom=2)
        ], style={'height': '800px'})   
        return element

@app.callback(Output('session_paper', 'data'), Input('session_selected', 'data'))
def get_papers(data):
    if not data or not data['selected']:
        return {}
    else:
        elements, papers = loaders.get_neo_papers(int(data['selected']['id']),limit=100, offset=0)
        return {'paper_graph':elements, 'papers':papers}


def format_paper(key, paper):
    url = dcc.Link('DOI', href=paper.get('url'), target='_blank', style={'margin-left':'15px','fontSize':10}) if paper.get('url') is not None else None
    element = html.Div(id=key,children=[
        html.Span(paper.get('node_id'),style={'fontSize':12}),
        html.H6(paper['title'], style={'fontSize':14, 'margin-bottom':'0px'}),
        dbc.Row([            
            html.Span(paper.get('field'),style={'fontSize':12, 'margin-left':'15px'}),
            html.Span(paper.get('year'),style={'fontSize':12, 'margin-left':'5px'}),
        ]),
        html.P(paper.get('abstract'),style={'fontSize':10, 'margin-bottom':'2px'}),
        dbc.Row([
            url,
            dcc.Link('Semantic Scholar', href=paper.get('s2url'), target='_blank', style={'margin-left':'15px','fontSize':10}),
        ]),
    ], style={'margin-top':'5px', 'margin-left':'0px', 'border':'1px dashed #aaaaaa'})
    return element


@app.callback(Output('papers-body', 'children'), Input('session_paper', 'data'))
def display_papers(data):
    if not data or 'papers' not in data:
        return html.P('No Node Selected')
    else:       
        paper_divs = [format_paper(k,paper) for k,paper in data['papers'].items()]
        element = html.Div(paper_divs, 
            style={        
                'height': '800px',
                'overflow': 'auto',
                'text-align': 'justify',
                })
        return element

@app.callback(Output('paper-graph-container', 'children'), Input('session_paper', 'data'))
def display_paper_graph(data):
    if not data or 'paper_graph' not in data:
        return html.P('No Node Selected')
    else:  
        #return html.P(str(data['paper_graph']))
        return cyto.Cytoscape(
                id='cyto-paper',        
                layout = {'name': 'cose'},
                elements = data['paper_graph'],
                stylesheet= phylo_tree.default_stylesheet,
                style={'width': '100%', 'height': '800px'}
            )   


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
    app.run_server(debug=False)