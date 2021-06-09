import dash_html_components as html
import dash_leaflet as dl
from dash import Dash

# Cool, dark tiles by Stadia Maps.
url = 'https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png'
attribution = '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a> '
url_ = "https://api.gbif.org/v2/map/occurrence/density/{z}/{x}/{y}@2x.png?srs=EPSG:3857&bin=hex&hexPerTile=64&style=purpleYellow-noborder.poly&taxonKey=120"
# Create app.
app = Dash()
app.layout = html.Div([
    dl.Map([
        dl.TileLayer(url=url, maxZoom=10, attribution=attribution),
        dl.TileLayer(url=url_, maxZoom=10)
        ], zoom=2)
], style={'width': '100%', 'height': '600px', 'margin': "auto", "display": "block", "position": "relative"})

if __name__ == '__main__':
    app.run_server()