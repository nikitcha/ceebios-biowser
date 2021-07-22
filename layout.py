import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import sys

from pandas.io.formats import style
sys.path.append('gbif_autosuggest')
import gbif_autosuggest
import os
import dash
app = dash.Dash(__name__)
from layouts.landing_page import intro_layout
from layouts.graph_tab import graph_layout
import climate
import phylo_tree

logo = html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    html.Div(html.Img(src=app.get_asset_url('ceebios-logo.png'), height="30px")),
                    html.Div("CEEBIOS", className='logo__ceebios', style={'font-size':20}),
                    html.Div("Biowser", className ='logo__biowser', style={'font-size':20}),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://ceebios.com",
            style={"text-decoration": "none"}
        )

search_bar_landing = dbc.Row(
    [
        dbc.Col(
            dbc.Button("Start Exploration", id='search', color="primary", className="explore", href='/explore', size='md'),
        style={'margin-left':'100px'}),
    ],
    no_gutters=True,
    className="search-bar-landing",
)

navbar_landing = dbc.Navbar(
    [
        logo,
        dbc.Col(dbc.Button("Start Exploration", id='search', color="primary", className="explore", href='/explore', size='md'),style={'margin-left':'100px'}),
    ],
    color="light", dark=False, className="navbar-landing"
)

navbar = dbc.Navbar(
    [
        logo,
        dbc.Col(gbif_autosuggest.GbifAutosuggest(id='input', value='', label='my-label')),
        dbc.Input(id="username", placeholder="User Name", type="text",debounce=True, className='username'),
        dbc.Col(dcc.Dropdown(id='history-container',placeholder='Search History', className='history'))
    ],
    color="light", dark=False)


#tab_papers = html.Div([html.Div(id='papers-body'), dbc.Button("Next", id='papers-next-2')])
tab_papers = html.Div(id='papers-body')
tab_images = html.Div(id='images-body')
tab_maps = html.Div(id='maps-body')
keys = list(climate.climate_dict.keys())
tab_climate = html.Div([
            dbc.Row([
                html.Div('Climate data statistics for species geographical range. Source: GBIF & WorlClim.org', style={'font-size':14}, className='climate-note')
            ]),
            dbc.Row(dcc.RadioItems(
                id='climate-radio', 
                options=[{'value': x, 'label': x} 
                        for x in keys],
                value=keys[0], 
                inputStyle = {'display':'inline-block', 'padding':'10px'},
                labelStyle = {'font-size':14, 'padding':'5px'}
            )),            
            dbc.Row(dcc.Graph(id="climate-box-plot")),
        ])

tab_links = html.Div(id='links-body')
tab_wiki = html.Div(id='wiki-body')
tab_resources = html.Div(id='resources-body')

tabs_layout = html.Div(
    dbc.Tabs(
        [
            dbc.Tab(tab_images, label="Images", className='single-tab'),
            dbc.Tab(tab_wiki, label="Wikipedia", className='single-tab'),
            dbc.Tab(tab_papers, label="Publications", className='single-tab'),
            dbc.Tab(tab_maps, label="Maps", className='single-tab'),
            dbc.Tab(tab_climate, label="Climate", className='single-tab'),
            dbc.Tab(tab_links, label="Smart Links", className='single-tab'),
            dbc.Tab(tab_resources, label="Other Resources", className='single-tab'),
        ]),
        className='tabs-data')

index_page = html.Div([
    navbar_landing,
    intro_layout])

legend = html.Div(
   [html.Div('● '+k,style={'fontSize':9,'color':v}) for k,v in phylo_tree.COLORS.items()], 
   style={'position':'absolute','margin-top':'50px', 'margin-left':'10px'})

explore_page = html.Div([
    navbar,
    legend,
    dbc.Row([
        graph_layout,
        tabs_layout,
    ], className = 'explore-page')
    ])





