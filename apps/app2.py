import praw
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app import app

from wordcloud import WordCloud,STOPWORDS
from dash.exceptions import PreventUpdate
import re
import cv2 

reddit = praw.Reddit(
    client_id="wBlYlJ7XtNtL0d1fEAj-vg",
    client_secret="muW07OSaCr5I4Dj23Sn7HeFeoifSLg",
    user_agent="a12487")
#------------------------------------------------------------------------------
s = ''
l=[]
l_dec=[]

def scatt(subs,n=4):
    data = []
    for x in subs:
        for y in reddit.subreddit(x).top('day',limit=n):
            data.append([y.subreddit.display_name,y.score,y.num_comments,str(y.author.name),y.total_awards_received,y.url])
    df = pd.DataFrame(data, columns =['Subreddit', 'Upvotes', 'Total Comments','Username','Total Awards','url'])
    return df
#-------------------------------------------------------------------------------
def pie():
    flairs = {}
    for x in reddit.subreddit('science').top('month',limit=999):
        f = x.link_flair_text 
        if f not in flairs.keys():
            flairs[f] = 1
        else :
            flairs[f] +=1
    df = pd.DataFrame(flairs.items(),columns=['Topic','Count'])
    return df
#-------------------------------------------------------------------------------
def wordcld(sub,n):
        subreddit = reddit.subreddit(sub)
        sub_title = []
        for submission in subreddit.new(limit = n):
            sub_title.append(submission.title)
        y = []
        for x in sub_title:
            x = x.lower()
            y.append(x)
        s = set(STOPWORDS)
        my_file = open("verbsList.txt", "r")
        content = my_file.read()
        ar = content.split("\n")
        my_file.close()
        s.update(ar)
        my_file = open("verbs-all.txt", "r")
        content = my_file.read()
        ar =re.split('\t|\n', content)
        my_file.close()
        s.update(ar)
        wordcloud = WordCloud(width = 1200, height = 600, stopwords= s, max_font_size = 200,background_color = 'white', colormap = 'viridis')
        wordcloud = wordcloud.generate(' '.join(y))
        img = wordcloud.to_file('work.png')
        df3 = cv2.imread('work.png')
        return df3

#-------------------------------------------------------------------------------
#app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
#-------------------------------------------------------------------------------
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

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
                        dbc.Col(dbc.NavbarBrand("Reddit Stats", className="ms-2")),
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
#--------------------------------------------------
form = dbc.Row(
    [
        dbc.Col(
            [
                #dbc.Label("Email", html_for="example-email-grid"),
                dbc.Input(
                    type="text",
                    id="subreddit",
                    value='',
                    placeholder="Enter subreddit",
                ),
            ],
            width=3,
        ),
        dbc.Col(
            [
                #dbc.Label("Password", html_for="example-password-grid"),
                dbc.Input(
                    type="number",
                    id="num",
                    value=1,
                    min=1,
                    max=10,
                    step=1
                ),
            ],
            width=3,
        ),
        dbc.Col(dbc.Button("Submit", color="primary",id='submit'), width="auto"),
    ],
    className="g-3",
)
#-------------------------------------------------------------------------------
form1 = dbc.Row(
    [
        dbc.Col(
            [
                #dbc.Label("Email", html_for="example-email-grid"),
                dbc.Input(
                    type="text",
                    id="subreddit1",
                    value=None,
                    placeholder="Enter subreddit",
                ),
            ],
            width=3,
        ),
        dbc.Col(
            [
                #dbc.Label("Password", html_for="example-password-grid"),
                dbc.Input(
                    type="number",
                    id="num1",
                    value=100,
                    min=100,
                    max=200,
                    step=1
                ),
            ],
            width=3,
        ),
        dbc.Col(dbc.Button("Submit", color="primary",id='submit1'), width="auto"),
    ],
    className="g-3",
)
#-------------------------------------------------------------------------------
table_header = [
    html.Thead(html.Tr([html.Th("Subreddits")]))
]

table_body = [html.Tbody(id='tab')]

table = dbc.Table(table_header + table_body,
                  bordered=True,
                  dark=True,
                  hover=True,
                  responsive=True,
                  striped=True,)
#-------------------------------------------------------------------------------
layout = html.Div([
    dbc.Container(navbar, fluid=True),
    html.Br(),
    dbc.Container(form, fluid=True),
    html.Br(),
    dbc.Container(table, fluid=True),
    #html.Div(id='my-output'),
    html.Br(),
    dbc.Button("Generate graph", color="success", size="lg", id='load', className="me-1"),
    dcc.Graph(id='award_upvotes',className='g20'),
    dcc.Graph(id='pie',className='g21'),
    html.Br(),
    dbc.Container(form1, fluid=True),
    html.Br(),
    dcc.Graph(id='wordel',className='g22')
],className='app2')

@app.callback(
    #Output(component_id='my-output', component_property='children'),
    Output(component_id='tab', component_property='children'),
    Input('submit','n_clicks'),
    State(component_id='subreddit', component_property='value'))
def input_collector(clicks,subred):
    global s
    global l
    global l_dec
    l.append(str(subred))
    l_dec.append(html.Tr([html.Td(subred)]))
    s=s+subred+'\n'
    #return s
    return l_dec
    
@app.callback(
    Output(component_id='wordel', component_property='figure'),
    Input('submit1','n_clicks'),
    State(component_id='subreddit1', component_property='value'),
    State(component_id='num1', component_property='value'))
def word(click,sub,num):
    if sub is None :
        raise PreventUpdate
    else:
        df3 = wordcld(sub,num)
        fig = px.imshow(df3)        
        fig.update_layout(title_text='Commonly used words',title_x=0.5)
        fig.update_xaxes(visible=False)    
        fig.update_yaxes(visible=False)
        return fig




@app.callback(
    Output(component_id='award_upvotes', component_property='figure'),
    Output(component_id='pie', component_property='figure'),
    Input('load','n_clicks'),
    State(component_id='num', component_property='value'))
def graph_gen(click,num):
    if l[0] == '':
        l.remove('')
    df=scatt(l,num)
    fig = px.scatter(df, x="Upvotes", y="Total Awards", color="Subreddit",
                 size='Total Comments',hover_data=['Username'],size_max= 50)
    fig.update_layout(transition_duration=500)
    fig.update_layout(title_text='Top posts of particular subreddits (Bubbles denote posts)', title_x=0.43,title=dict(
        font=dict(
            family="roborto",
            size=20,
            color="Green"
        )))
    fig.update_layout(
    legend=dict(
        font=dict(
            family="Courier",
            size=12,
            color="Red"
        ),
        bgcolor="LightYellow",
        bordercolor="LightBlue",
        borderwidth=2
        )
    )
    fig.update_xaxes(title_font=dict(size=18, family='Courier', color='crimson'))
    fig.update_yaxes(title_font=dict(size=18, family='Courier', color='crimson'))

    df1 = pie()
    fig1 = go.Figure(data=[go.Pie(labels=df1.Topic,values=df1.Count,hole=0.3)])
    fig1.update_layout(title_text='Most talked about topics in r/science', title_x=0.43,title=dict(
        font=dict(
            family="roborto",
            size=20,
            color="Green"
        )))
    fig1.update_layout(
    legend=dict(
        font=dict(
            family="Courier",
            size=12,
            color="Red"
        ),
        bgcolor="LightYellow",
        bordercolor="LightBlue",
        borderwidth=2
        )
    )
    return fig,fig1






if __name__ == '__main__':
    app.run_server(debug=True)

print(l)
