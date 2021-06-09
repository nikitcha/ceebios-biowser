from numpy.lib.function_base import gradient


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

def  add_graph(graph1, graph2):
    graph_ = graph1.copy()
    for g in graph2:
        if 'source' in g['data']:
            ig = {'data':{'source':g['data']['target'], 'target':g['data']['source']}}
            if g not in graph1 and ig not in graph1:
                graph_ += [g]
    return graph_