import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

def deep_get(_dict, prop, default=None):
    if prop in _dict:
        return _dict.get(prop, default)
    else:
        for key in _dict:
            if isinstance(_dict.get(key), dict):
                return deep_get(_dict.get(key), prop, default)  

def safe_get(dic,fs):
    if len(fs)==0:
        return dic
    if fs[0] in dic:
        return safe_get(dic[fs[0]], fs[1:])
    else:
        return None                

def add_graph(graph1, graph2):
    graph_ = graph1.copy()
    for g in graph2:
        if 'source' in g['data']:
            ig = {'data':{'source':g['data']['target'], 'target':g['data']['source']}}
            if g not in graph1 and ig not in graph1:
                graph_ += [g]
    return graph_

    
def paper_layout(key, paper):
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
