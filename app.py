import dash
import dash_bootstrap_components as dbc
import flask

app = dash.Dash(__name__, 
                title='Ceebios Biowser', 
                suppress_callback_exceptions=True, 
                #external_stylesheets=[dbc.themes.BOOTSTRAP]
                )
server = app.server

