import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import sys
sys.path.append('gbif_autosuggest')
import gbif_autosuggest
import os
import dash
app = dash.Dash(__name__)
from layouts.landing_page import intro_layout
from layouts.graph_tab import graph_layout

search_bar_landing = dbc.Row(
    [
        dbc.Col(
            dbc.Button("Start Exploration", id='search', color="primary", className="explore", href='/explore', size='md'),
        style={'margin-left':'100px'}),
    ],
    no_gutters=True,
    className="search-bar-landing",
    style={'margin-left':'10px'}
)

search_bar = dbc.Row(
    [
        dbc.Col(gbif_autosuggest.GbifAutosuggest(id='input', value='', label='my-label'))
    ],
    no_gutters=True,
    className="search-bar",
    style={'margin-left':'10px'}
)

navbar_landing = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=app.get_asset_url('ceebios-logo.png'), height="30px")),
                    dbc.Col(dbc.NavbarBrand("CEEBIOS", style={'color':'#3D5170', 'margin-right':'10px'})),
                    dbc.Col(dbc.NavbarBrand("Biowser", style={'color':'#fb2056', 'margin-left':'10px'})),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://ceebios.com",
        ),
        search_bar_landing
    ],
    color="light", dark=False, className="navbar"
)

navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=app.get_asset_url('ceebios-logo.png'), height="30px")),
                    dbc.Col(dbc.NavbarBrand("CEEBIOS", style={'color':'#3D5170', 'margin-right':'10px'})),
                    dbc.Col(dbc.NavbarBrand("Biowser", style={'color':'#fb2056', 'margin-left':'10px'})),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://ceebios.com",
        ),
        search_bar,
        dbc.Input(id="username", placeholder="User Name", type="text",debounce=True, style={'width':'200px', 'margin-right':'10px', 'margin-left':'50px'}),
        dcc.Dropdown(id='history-container',placeholder='Search History',  style={'width':'300px', 'margin-right':'10px'})
    ],
    color="light", dark=False, className="navbar"
)


tab_papers = html.Div(id='papers-body')
tab_images = html.Div(id='images-body')
tab_maps = html.Div(id='maps-body')
tab_links = html.Div(id='links-body')
tab_wiki = html.Div(id='wiki-body')
tab_resources = html.Div(id='resources-body')

tab_style = {'margin':'0','padding':'0','border':'0'}
tabs_layout = html.Div(
    dbc.Tabs(
        [
            dbc.Tab(tab_maps, label="Maps", style=tab_style),
            dbc.Tab(tab_wiki, label="Wikipedia", style=tab_style),
            dbc.Tab(tab_images, label="Images", style=tab_style),
            dbc.Tab(tab_papers, label="Publications", style=tab_style),
            dbc.Tab(tab_links, label="Smart Links", style=tab_style),
            dbc.Tab(tab_resources, label="Other Resources", style=tab_style),
        ]),
        style={'width':'50%', 'height':'900px'})

index_page = html.Div([
    navbar_landing,
    intro_layout])

paper_pop = html.Div([
    html.P('Hello There')
    ],
    style={'position':'absolute', 'width':'500px', 'height':'500px'}
)

explore_page = html.Div([
    navbar,
    dbc.Row([
        graph_layout,
        tabs_layout,
        #paper_pop,
    ], style = {'border':'0', 'margin':'0','padding':'0'})
    ])





