import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app import app

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys
import re
from bs4 import BeautifulSoup
import bs4
import requests
#------------------------------------------------------------------------------
d = {'name':['a','b','c','d','e','f','g','h','i','j'],'views':[0,0,0,0,0,0,0,0,0,0],'year':[0,1,2,3,4,5,6,7,8,9],'tick':[0,1,2,3,4,5,6,7,8,9]}
df=pd.DataFrame(d)
d1 = {'tv':[0,0,0,0,0],'tick':[1,2,3,4,5]}
df1=pd.DataFrame(d)
d2 = {'top_viw':[0,0,0,0,0],'top_name':['a','b','c','d','e']}
df2=pd.DataFrame(d2)



def scraper(url):
    # chrome_path = "C:/Users/bhara/py/ct/ch/chromedriver.exe"
    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get(url)
    time.sleep(3)


    i = 0

    while True:
        i=i+1 
        html_from_page1 = driver.page_source
        cmd='window.scrollTo('+str(i*100000)+','+str((i+1)*100000)+');'
        driver.execute_script(cmd)
        html_from_page2 = driver.page_source
        if html_from_page2 == html_from_page1:
            time.sleep(2)
            driver.close()
            driver.quit()
            break
        html_from_page2 = html_from_page1



    html_text = html_from_page2
    soup = bs4.BeautifulSoup(html_text, "html.parser")
    soup = BeautifulSoup(html_text, 'html.parser')

    # title=soup.find_all('a',class_="yt-simple-endpoint style-scope ytd-grid-video-renderer")
    title=soup.find_all('a',class_="yt-simple-endpoint focus-on-expand style-scope ytd-rich-grid-media")




    for i in range(len(title)):
        title[i]=str(title[i]).replace(',','')

    cmd1 = '(.*)(\s)(\d+)(\s)(.*)ago(\s)(\d+)(\s)(\w+)(\s)(\d*)(\s*)(.*)(\s*)(\d*)(\s*)(.*)(\s)(.*)'
    cmd2 = '(.*)aria-label=\"(.*)(\s)by(\s)(.*)ago(.*)(\s)(\d+)(\s)views'
    # cmd2 = '(.*)aria-label=\"(.*)(\s)by(\s)(.*)(\s)ago(\s)(\d+)(\s)(\w+)(\s)(\d+)(\s)views'


    ago = []
    for i in title:
        m1 = re.match(cmd1,i,re.M)
        if m1:
            if (m1.group(5)).find('year') != -1:
                ago.append(int(m1.group(3)))
            else:
                ago.append(0)
        
    

    vid=[]
    viw=[]
    tick=[]
    n=1
    for i in title:
        m2 = re.match(cmd2,i,re.M)
        if m2:
            vid.append(m2.group(2))
            viw.append(int(m2.group(8)))
            tick.append(n)
            n=n+1
        else:
            print(i)

    global df
    d = {'name':vid,'views':viw,'year':ago,'tick':tick}
    print(len(vid),len(viw),len(ago),len(tick))
    time.sleep(5)
    df=pd.DataFrame(d)
    print("===========================================")
    return df

def hist_plot():
    ma=df['year'].max()
    mi=df['year'].min()

    s=0
    l=[]
    for i in range(mi,ma+1):
        a = df[df.year == i]
        # print(a)
        s=sum(a['views'])
        l.append(s)
        # print(s)

    d1={'tv':l}
    df1=pd.DataFrame(d1)
    return df1

    
def tops():
    top_viw=[]
    top_name=[]
    ma=df['year'].max()
    mi=df['year'].min()
    
    for i in range(mi,ma+1):
        a = df[df.year == i]
        a = a.sort_values('views',ascending=False)
        b=list(a['views'])
        top_viw.append(b[0])
        b=list(a['name'])
        top_name.append(b[0])
    

    d2={'top_viw':top_viw,'top_name':top_name}
    df2=pd.DataFrame(d2)
    return df2
#-------------------------------------------------------------------------------
#app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
#-------------------------------------------------------------------------------
PLOTLY_LOGO = 'https://images.plot.ly/logo/new-branding/plotly-logomark.png'

search_bar = dbc.Row(
    [
        dbc.Col(
            dbc.Button(
                "Home", color="primary", className="ms-2",href='/', n_clicks=0
            ),
            width="auto",
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("YouTube Stats", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                search_bar,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
)
#-------------------------------------------------------------------------------
form = dbc.Form(
    dbc.Row(
        [
            dbc.Col(
                [
                dbc.Input(
                    type="url",
                    id='in',
                    placeholder="Enter url",
                    value=''
                ),
            ],
                width=3,
                className="me-3",
            ),
            dbc.Col(dbc.Button("Submit", color="primary",id='submit'), width="auto"),
        ],
        className="g-2",
    )
)

#-------------------------------------------------------------------------------
layout = html.Div([
    dbc.Container(navbar, fluid=True),
    html.Br(),
    dbc.Container(form, fluid=True),
    
    #html.Button(id='sub',n_clicks=0,children=['submit']),
    html.Br(),
    html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): '{} year(s) ago'.format(str(year)) for year in df['year'].unique()},
        disabled=True,
        step=None
    )
    ],className='g10'),
    dcc.Graph(id='complete_plot',className='g11'),
    dcc.Graph(id='hist',className='g12'),
    dcc.Graph(id='y_tops',className='g13'),
    dcc.Graph(id='t_tops',className='g14'),
    dcc.Graph(id='t_bots',className='g15')
],className='app1')


@app.callback(
    dash.dependencies.Output('year-slider', 'min'),
    dash.dependencies.Output('year-slider', 'max'),
    dash.dependencies.Output('year-slider', 'marks'),
    dash.dependencies.Output('year-slider', 'disabled'),
    Input('submit','n_clicks'),
    State(component_id='in', component_property='value'))
def slider_setting(clicks,input_url):
    cmd='https://www.youtube.com/(.*)/videos'
    m3 = re.match(cmd,input_url,re.M)
    if m3:
        df=scraper(input_url)
        print(df['year'])
        #df1=hist_plot()
        min1=df['year'].min()
        max1=df['year'].max()
        mar1={str(year): '{} year(s) ago'.format(str(year)) for year in df['year'].unique()}
        return min1,max1,mar1,False
    else:
        df=pd.DataFrame(d)
        min1=df['year'].min()
        max1=df['year'].max()
        mar1={str(year): '{} year(s) ago'.format(str(year)) for year in df['year'].unique()}
        return min1,max1,mar1,True



@app.callback(
    Output('graph-with-slider', 'figure'),
    Output('hist', 'figure'),
    Output('complete_plot', 'figure'),
    Output('y_tops', 'figure'),
    Output('t_tops', 'figure'),
    Output('t_bots', 'figure'),
    Input('year-slider', 'value'))
def graph_gen(slider_val):
    filtered_df = df[df.year == slider_val]
    fig = px.line(filtered_df, x='tick',y="views",markers=True,
                  labels={
                     "tick": "videos",
                     "views": "views (year wise)"
                  },
                  hover_data={"name":True,"views":True,"tick":False})
    fig.update_xaxes(
    ticktext=filtered_df['name'])
    
    fig.update_layout(
    title={
        'text': "Yearly Views",
        'y':1,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    font_size=15,
    title_font_family="Times New Roman",
    title_font_color="black",
    title_font_size=24,
    font_color="blue",
    transition_duration=500)

    df1=hist_plot()
    fig1=px.bar(df1,y='tv',
                labels={
                     "tv": "views",
                     "index": "year"
                  },
                text_auto=True)
    fig1.update_layout(
        title={
        'text': "View Summary",
        'y':1,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        font_size=15,
    title_font_family="Times New Roman",
    title_font_color="black",
    title_font_size=24,
        font_color="blue",
        transition_duration=500)
    
    fig2=px.line(df,x='tick',y='views',markers=True,
                 labels={
                     "views": "views",
                     "tick": "videos"
                  },
                 hover_data={"name":True,"views":True,"tick":False})
    fig2.update_layout(
        title={
        'text': "Cumulative Yearly Views",
        'y':1,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        font_size=15,
    title_font_family="Times New Roman",
    title_font_color="black",
    title_font_size=24,
        font_color="blue",
        transition_duration=500)
    
    df3=tops()
    fig3=px.bar(df3,y='top_viw',
                labels={
                     "top_viw": "views",
                     "index": "year"
                  },
                hover_data={"top_name":True,"top_viw":True})
    fig3.update_layout(
        title={
        'text': "Top Rated Video By Year",
        'y':1,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        font_size=15,
    title_font_family="Times New Roman",
    title_font_color="black",
    title_font_size=24,
        font_color="blue",
        transition_duration=500)

    top=df.sort_values(['views'],ascending=False).head(n=10)
    top['tick']=[0,1,2,3,4,5,6,7,8,9]
    fig4=px.bar(top,x='tick',y='views',
                labels={
                     "views": "views",
                     "tick": "video"
                  },
                hover_data={"name":True,"views":True,'tick':False})
    fig4.update_layout(
        title={
        'text': "Top 10 Videos Of All Time",
        'y':1,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        font_size=15,
    title_font_family="Times New Roman",
    title_font_color="black",
    title_font_size=24,
        font_color="blue",
        transition_duration=500)

    bot=df.sort_values(['views'],ascending=False).tail(n=10)
    bot['tick']=[0,1,2,3,4,5,6,7,8,9]
    fig5=px.bar(bot,x='tick',y='views',
                labels={
                     "views": "views",
                     "tick": "video"
                  },
                hover_data={"name":True,"views":True,'tick':False})
    fig5.update_layout(
        title={
        'text': "Least Viewed",
        'y':1,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        font_size=15,
    title_font_family="Times New Roman",
    title_font_color="black",
    title_font_size=24,
        font_color="blue",
        transition_duration=500)

    return fig,fig1,fig2,fig3,fig4,fig5


if __name__ == '__main__':
    app.run_server(debug=True)
