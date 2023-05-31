from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate


import plotly.express as px

from app import app
from apps import app1, app2


from wordcloud import WordCloud
import cv2 
#-------------------------------------------------------------------------------

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1(['STATS-TUBE'],className='head'),
            
            html.H5(['Analytics of Social Platform'],className='info'),
            
            html.H6(['by: Abhinav R Bharadwaj'],className='pep1'),
            
            html.H6(['Ansul Dasyam'],className='pep2'),
            
            dbc.Button(html.H1(['YouTube'],className='t1'), color="primary",href='/apps/app1', className="b1"),

            dbc.Button(html.H1(['Reddit'],className='t1'), color="primary",href='/apps/app2', className="b2"),
            ],className='button')
        
    ],id='but',className='back'),
    
    dcc.Location(id='url', refresh=False),
    
    html.Div(id='page-content')
],className='index')


@app.callback(Output('page-content', 'children'),
              Output('but', 'hidden'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/app1':
        return app1.layout,True
    
    elif pathname == '/apps/app2':
        return app2.layout,True
    
    elif pathname == '/':
        return '404',False



if __name__ == '__main__':
    app.run_server(debug=True)




