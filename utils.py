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