COLORS = {
  'SPECIES':"#fb2056",
  'GENUS':"#fc8f5b",
  'FAMILY':"#ffd055",
  'ORDER':"#8dd58c",
  'CLASS':"#38c9b1",
  'PHYLUM':"#1798c3",
  'KINGDOM':"#182573",
}
ORDER = {
  'KINGDOM':1,
  'PHYLUM':2,
  'CLASS':3,
  'ORDER':4,
  'FAMILY':5,
  'GENUS':6,
  'SPECIES':7,
  'SUBSPECIES':8,
  'VARIETY':9,
}

small_stylesheet = [
          {
            'selector': 'node',
            'style': {'width': 10,'height': 10, 'shape': 'ellipse', "label": "data(label)", 'font-size':8}
          },
          {
            'selector': 'node[img]',
            'style': {'background-image':'data(img)','background-fit': 'cover',"border-width":3}
          },  
          {
            'selector': 'node[rank="SPECIES"]',
            'style': {'background-color': '#fb2056',"border-color":'#fb2056'}
          },  
          {
            'selector': 'node[rank="GENUS"]',
            'style': {'background-color': '#fc8f5b','border-color': '#fc8f5b'}
          },  
          {
            'selector': 'node[rank="FAMILY"]',
            'style': {'background-color': '#ffd055','border-color': '#ffd055'}
          },  
          {
            'selector': 'node[rank="ORDER"]',
            'style': {'background-color': '#8dd58c','border-color': '#8dd58c'}
          },  
          {
            'selector': 'node[rank="CLASS"]',
            'style': {'background-color': '#38c9b1'}
          },  
          {
            'selector': 'node[rank="PHYLUM"]',
            'style': {'background-color': '#1798c3'}
          },  
          {
            'selector': 'node[rank="KINGDOM"]',
            'style': {'shape': 'rectangle','background-color': '#182573'}
          }, 
          {
            'selector': 'node[rank="FUNCTION"]',
            'style': {'shape': 'triangle','background-color': '#F7E7CE'}
          }, 
          {
            'selector': 'node[rank="PAPER"]',
            'style': {'shape': 'rectangle','background-color': '#AFDCEC'}
          }, 
          {
            'selector': 'edge',
            'style': {
                "curve-style": "bezier",
                "opacity": 0.45,
                'z-index': 5000,
                'width':1
            }  
        },
        {
        'selector': ':selected',
            "style": {
                "border-width": 1,
                "border-color": "black",
                "border-opacity": 1,
                "opacity": 1,
                "color": "black",
                "font-size": 10,
                'z-index': 9999
            }
        }    
]

default_stylesheet = [
          {
            'selector': 'node',
            'style': {'width': 20,'height': 20, 'shape': 'ellipse', "label": "data(label)", 'font-size':8}
          },
          {
            'selector': 'node[img]',
            'style': {'background-image':'data(img)','background-fit': 'cover',"border-width":3}
          },  
          {
            'selector': 'node[rank="SPECIES"]',
            'style': {'background-color': '#fb2056',"border-color":'#fb2056'}
          },  
          {
            'selector': 'node[rank="GENUS"]',
            'style': {'background-color': '#fc8f5b','border-color': '#fc8f5b'}
          },  
          {
            'selector': 'node[rank="FAMILY"]',
            'style': {'background-color': '#ffd055','border-color': '#ffd055'}
          },  
          {
            'selector': 'node[rank="ORDER"]',
            'style': {'background-color': '#8dd58c','border-color': '#8dd58c'}
          },  
          {
            'selector': 'node[rank="CLASS"]',
            'style': {'background-color': '#38c9b1'}
          },  
          {
            'selector': 'node[rank="PHYLUM"]',
            'style': {'background-color': '#1798c3'}
          },  
          {
            'selector': 'node[rank="KINGDOM"]',
            'style': {'shape': 'rectangle','background-color': '#182573'}
          }, 
          {
            'selector': 'node[rank="FUNCTION"]',
            'style': {'shape': 'triangle','background-color': '#F7E7CE'}
          }, 
          {
            'selector': 'node[rank="PAPER"]',
            'style': {'shape': 'rectangle','background-color': '#AFDCEC'}
          }, 
          {
            'selector': 'edge',
            'style': {
                "curve-style": "bezier",
                "opacity": 0.45,
                'z-index': 5000,
                'width':1
            }  
        },
        {
        'selector': ':selected',
            "style": {
                "border-width": 1,
                "border-color": "black",
                "border-opacity": 1,
                "opacity": 1,
                "color": "black",
                "font-size": 10,
                'z-index': 9999
            }
        }    
]
