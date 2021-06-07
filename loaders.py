from pygbif import species, occurrences, maps
import phylo_tree
import pandas
from wikidata.client import Client
from qwikidata.sparql import return_sparql_query_results
client = Client() 
from utils import safe_get, deep_get
import requests
import urllib
import wikipedia

sci_name = client.get('P225')
im_prop = client.get('P18')

def get_backbone(suggest):
    backbone = species.name_backbone(name=suggest['name'], rank=suggest['rank'])
    return backbone

def get_cyto_backbone(backbone):
    nodes,edges = [],[]
    last_id = ''
    for o in phylo_tree.ORDER:
        fld = o.lower()
        if fld in backbone:
            label = backbone[fld].lower().capitalize()
            id = str(backbone[fld+'Key'])
            nodes += [{'data': { 'id': id, 'label': label, 'rank':o.upper() }}]
            if last_id:
                edges += [{'data': { 'source': id, 'target': last_id}}]
            last_id = id
    return nodes+edges    

def get_children(data, limit = 5):
    selected_id = data['selected']['id']
    children = species.name_usage(key=int(selected_id), data='children', limit=limit,offset=0)['results']
    children = pandas.DataFrame(children)
    if 'canonicalName' in children.columns:
        children = children[['canonicalName','rank','taxonID']].dropna()
    nodes,edges = [],[]
    for _,row in children.iterrows():
        taxon = str(row['taxonID'].replace('gbif:',''))
        name = row['canonicalName'].lower().capitalize()
        nodes += [{'data': { 'id': taxon, 'label': name, 'rank':row['rank'].upper()}}]
        edges += [{'data': { 'source': taxon, 'target': selected_id}}]
    return nodes+edges    


def get_wiki_info(taxon):
    query = """SELECT ?item ?itemLabel ?itemDescription ?article ?image ?range
    WHERE 
    {
    ?item wdt:P846 "$gbif$"
    optional {?item wdt:P18 ?image.}
    optional {?item wdt:P181 ?range.}
    OPTIONAL {
        ?article schema:about ?item ;
        schema:isPartOf <https://en.wikipedia.org/> ; 
        schema:name ?sitelink .
    }
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }""".replace('$gbif$',str(taxon))
    res = return_sparql_query_results(query)['results']['bindings']
    out = {}
    if len(res)>0:
        out['image'] = safe_get(res[0], ['image','value'])
        out['wikipedia'] = safe_get(res[0], ['article','value'])
        out['wikidata'] = safe_get(res[0], ['item','value'])
        out['range'] = safe_get(res[0], ['range','value'])
        out['description'] = safe_get(res[0], ['itemDescription','value'])
        out['label'] = safe_get(res[0], ['itemLabel','value'])
        if out['wikipedia']:
            url = urllib.parse.unquote(out['wikipedia'])
            out['page'] = wikipedia.WikipediaPage(url.split('/')[-1])
        else:
            out['page'] = ''
    return out

def get_wiki(name):
    try:
        page = wikipedia.WikipediaPage(wikipedia.search(name, results=1))
        url = f"https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&titles={page.title}&format=json"
        result = requests.get(url).json()
        entity = client.get(deep_get(result,'wikibase_item'), load=True)
        image_url = '' if im_prop not in entity else entity[im_prop].image_url
        return page, image_url
    except:
        return None,None

