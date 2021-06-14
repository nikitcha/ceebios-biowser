import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from layout import explore_page, index_page
from layouts.graph_tab import paper_tab, taxon_tab
from utils import init_db, get_connection
import callbacks

def serve_layout():
    return html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])

app.layout = serve_layout
app.validation_layout = html.Div([
    explore_page,
    index_page,
    paper_tab,
    taxon_tab
])


# Update the index
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])              
def display_page(pathname):
    if pathname == '/explore':
        return explore_page
    else:
        return  index_page
        # You could also return a 404 "URL not found" page here

if __name__ == '__main__':
    init_db(get_connection())
    app.run_server(debug=False, host='3.19.223.69')