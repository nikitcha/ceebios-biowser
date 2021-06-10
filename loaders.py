from pygbif import species, occurrences
import pandas
from wikidata.client import Client
from qwikidata.sparql import return_sparql_query_results
import requests
import urllib
import wikipedia
from py2neo import Graph

from utils import safe_get, deep_get
import phylo_tree
import neo4j_credentials as nc

graph = Graph("bolt://localhost:7687", auth=(nc.user, nc.password))
client = Client() 
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

def get_children(data, limit = 5, offset=0):
    selected_id = data['id']
    children = species.name_usage(key=int(selected_id), data='children', limit=limit,offset=offset)['results']
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

def get_images(taxon, limit=6):
    res = occurrences.search(taxonKey=taxon,mediatype='stillimage',limit=limit)['results']
    images = [r['media'][0]['identifier'] for r in res]
    return images


def parse_node(start_node, papers):
    if str(start_node.labels)==':Taxon':
        node = { 'id': str(start_node['id']), 'label': start_node['name'], 'rank':start_node['rank'].upper()}
    elif str(start_node.labels)==':Paper':
        if start_node['id'] not in papers:
            paper_dict = dict(start_node)
            paper_dict.update({'node_id':'Paper '+str(len(papers))})
            newpaper = {start_node['id']:paper_dict}
            papers.update(newpaper)
        node = {'id': start_node['id'], 'label':papers[start_node['id']]['node_id'], 'rank':'PAPER'}
    else:
        node = {'id': start_node['name'], 'label': start_node['name'], 'rank':'FUNCTION'}
    return node


def cypher_to_cytoscape(results):
    nodes, edges = [],[]
    papers = {}
    for res in results:
        res = res['p']
        for node in res.nodes:
            tnode = parse_node(node, papers)
            nodes += [{'data':tnode}]
        for rel in res.relationships:
            snode = parse_node(rel.nodes[0], papers)
            enode = parse_node(rel.nodes[1], papers)
            edge = {'data': { 'source': snode['id'], 'target': enode['id']}}
            iedge = {'data': { 'source': enode['id'], 'target': snode['id']}}
            if (edge not in edges) and (iedge not in edges):
                edges += [edge]
    return nodes+edges, papers


def get_neo_papers(taxon, limit=50, offset=0):
    sq = """
    match (p:Taxon {{id:{}}})-[:IS_SYNONYM*1..2]-(q:Taxon) return p,q;
    """.format(taxon)
    synonyms = graph.run(sq).data()
    alltax = [taxon]
    for syn in synonyms:
        for f in ['q','p']:
            tax = syn[f]['id']
            if tax not in alltax:
                alltax.append(tax)

    query = """
    match p=(t:Taxon)-[:MENTIONS*1..2]-()
    where t.id in [{}]
    return p
    skip {}
    limit {};
    """.format(','.join([str(s) for s in alltax]), offset, limit)

    elements, papers = cypher_to_cytoscape(graph.run(query).data())
    return elements, papers    