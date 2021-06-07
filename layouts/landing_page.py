import dash_html_components as html
import dash
app = dash.Dash(__name__)

style_div = {'display': 'flex','flex-wrap': 'wrap', 'padding':'20px'}
style_text = {'width': '500px', 'padding':'20px'}

div_octo = html.Div([
    html.Div([html.Img(src=app.get_asset_url('planet1.jpg'), width="500px")]),
    html.Div([
        html.Span("There are some ", style={'color':'white'}),
        html.Span("4 million different kinds of animals and plants ", style={'color':'#fb2056'}),
        html.Span("in the world.", style={'color':'white'}),
        html.P("Discover the richness of the creatures that surrounds us, where to find them, and why each of them is unique.", style={'color':'white'})
        ], style=style_text)
    ], style=style_div)

div_tukan = html.Div([
    html.Div([
        html.P('"It seems to me that the natural world is the greatest source of excitement; the greatest source of visual beauty; the greatest source of intellectual interest. It is the greatest source of so much in life that makes life worth living."', style={'color':'white', 'text-align':'right'}),
        html.P("- Sir David Attenborough", style={'color':'#fb2056', 'text-align':'right'})
        ], style=style_text),
    html.Div([html.Img(src=app.get_asset_url('planet2.jfif'), width="500px")])
], style=style_div)

div_whale = html.Div([
    html.Div([html.Img(src=app.get_asset_url('planet3.jpg'), width="500px")]),
    html.Div([
        html.Span("Platform created in collaboration between ", style={'color':'white'}),
        html.Span("Data For Good ",style={'color':'#fb2056'}),
        html.Span("and ",style={'color':'white'}),
        html.Span("Ceebios",style={'color':'#fb2056'}),
        html.Span(".",style={'color':'white'}),
        html.Div([
        html.Span("Species data from ",style={'color':'white'}),
        html.Span("GBIF",style={'color':'#fb2056'}),
        html.Span(", scientific publications from ",style={'color':'white'}),
        html.Span("Semantic Scholar Open Corpus",style={'color':'#fb2056'})], style={'display': "inline-block"})
        ], style=style_text)
], style=style_div)

intro_layout = html.Div([
    html.Div([
        div_octo,
        div_tukan,
        div_whale
    ], style={'margin':'auto', 'width':'1040px'})
], style={"background": 'linear-gradient(180deg, rgba(7,10,32,1) 0%, rgba(23,36,113,1) 100%)','height':'100%', "width":"100%"})

