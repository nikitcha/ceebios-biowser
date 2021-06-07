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

search_bar = dbc.Row(
    [
        dcc.Store(id='session_graph', storage_type='session'),
        dcc.Store(id='session_selected', storage_type='session'),
        dbc.Col(gbif_autosuggest.GbifAutosuggest(id='input', value='', label='my-label')),
        dbc.Col(
            dbc.Button("Search", color="primary", className="explore", href='/explore', size='md'),
        ),
    ],
    no_gutters=True,
    className="search-bar",
    style={'margin':'auto'}
)

navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=app.get_asset_url('ico-ceebios.png'), height="30px")),
                    dbc.Col(dbc.NavbarBrand("CEEBIOS", className="ml-1", style={'color':'#3D5170', 'margin':'0px'})),
                    dbc.Col(dbc.NavbarBrand("Biowser", className="ml-1", style={'color':'#fb2056', 'margin':'0px'})),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://ceebios.com",
        ),
        search_bar
    ],
    color="light", dark=False, className="navbar"
)

tab_papers = dbc.Card(dbc.CardBody(html.P("Publications")))
tab_images = dbc.Card(dbc.CardBody(html.P("Images")))
tab_maps = dbc.Card(dbc.CardBody(html.P("Maps")))
tab_links = dbc.Card(dbc.CardBody(html.P("Smart Links")))
tab_wiki = dbc.Card(dbc.CardBody(html.P("Wikipedia")))

tabs_layout = html.Div(
    dbc.Tabs(
        [
            dbc.Tab(tab_wiki, label="Wikipedia"),
            dbc.Tab(tab_images, label="Images"),
            dbc.Tab(tab_papers, label="Publications"),
            dbc.Tab(tab_maps, label="Maps"),
            dbc.Tab(tab_links, label="Smart Links"),
        ]),
        style={'width':'50%', 'height':'800px'})

index_page = html.Div([
    navbar,
    intro_layout])

explore_page = html.Div([
    navbar,
    dbc.Row([
        graph_layout,
        tabs_layout    
    ])
    ])






