import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from sqlite3 import Connection
import sqlite3
import pandas

def get_connection(dbname='data.db'):
    return sqlite3.connect(dbname, check_same_thread=False)

def init_db(conn: Connection):
    conn.execute(
        """CREATE TABLE IF NOT EXISTS userdata
            (
                username TEXT,
                search TEXT,
                UNIQUE(username, search)
            );"""
    )
    conn.commit()

def add_userdata(conn: Connection, username:str, search:str):
    try:
        conn.execute(f"INSERT or IGNORE INTO userdata (username, search) VALUES ('{username}', '{search}')")
        conn.commit()
    except:
        print('Entry present')

def get_userdata(conn: Connection, username:str):
    if username=='admin':
        df = pandas.read_sql(f"SELECT DISTINCT search FROM userdata", con=conn)
    else:
        df = pandas.read_sql(f"SELECT DISTINCT search FROM userdata where username='{username}'", con=conn)
    return df


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

def clean_graph(graph):
    _g = []
    for g in graph:
        if g not in _g:
            if 'source' in g['data']:
                ig = {'data':{'source':g['data']['target'], 'target':g['data']['source']}}
                if ig not in _g:
                    _g.append(g)
            else:
                _g.append(g)
    return _g

    
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
