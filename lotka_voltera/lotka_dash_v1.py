#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
#plotly graph objects to create the plot itself
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
import pandas as pd
from scipy import integrate
# Definition of parameters


# In[2]:


# Add additional tunable parameters

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app= dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app.config.suppress_callback_exceptions = True
#Our dash will be very simple, just the graph
app.layout = html.Div([html.H1(children = "staySape's Lotka-Voltera Model Simulation ",
                style = {
                    'font-size':'320%',
                    'text-align': 'center'
                    }
                ),
                    dcc.Graph(id='popvpop'),
                    dcc.Graph(id='linetimepop'),
                       #and four sliders for the paramaters
                      html.Div([html.Div(children='Alpha'),dcc.Slider(id='alpha',
                                     min=1,max=4,step=.05,marks = {1:'1',2:'2',3:'3',4:'4'},
                                     value=3)]),
                      html.Div([html.Div(children='Beta'),dcc.Slider(id='beta',
                                     min=0,max=2,step=.05,marks = {0:'0',1:'1',2:'2'},
                                     value=.1)]),
                      html.Div([html.Div(children='Gamma'),dcc.Slider(id='gamma',
                                     min=0,max=2,step=.05,marks = {0:'0',1:'1',2:'2'},
                                     value=.8)]),
                      html.Div([html.Div(children='Delta'),dcc.Slider(id='delta',
                                     min=0,max=1,step=.01,marks = {0:'0',.25:'.25',.5:'.5',.75:'.75',1:'1'},
                                     value=.05)]),
                      html.Div([html.Div(children='Prey0'),dcc.Input(id="Prey0", type="number", placeholder="input with range",
                                    min=5, max=100, step=5, value = 50
                                    )]),
                       html.Div([html.Div(children='Predator0'),dcc.Input(id="Predator0", type="number", placeholder="input with range",
                                    min=5, max=100, step=5, value = 50
                                    )]),
                    html.Div(id='intermediate-value', style={'display': 'none'})
                      ])


# In[3]:


def lotka_sim(X, t, a, b, c, d):
    """ Return the growth rate of
    prey and predator populations. """
    preydx =  a*X[0] -   b*X[0]*X[1]
    predatordx = -c*X[1] + d*b*X[0]*X[1] 
    return np.array([preydx,predatordx])


# In[4]:


#Telling Dash that the sliders are inputs into the graph
@app.callback(Output('intermediate-value','children'),
             [Input('alpha','value'),
             Input('beta','value'),
             Input('gamma','value'),
             Input('delta','value'),
             Input('Prey0','value'),
             Input('Predator0','value')])
def datasimulate(alpha,beta,gamma,delta,Prey0, Predator0):
    
    t = np.linspace(0, 15,  1000)
    X0 = np.array([Prey0, Predator0]) 
    X = integrate.odeint(lotka_sim, X0, t, args = (alpha,beta,gamma,delta))
    ppPop = pd.DataFrame()
    ppPop['Time'] = t
    ppPop['Prey'] = X[:,0]
    ppPop['Predator'] = X[:,1]
    return ppPop.to_json()

@app.callback(Output('linetimepop', 'figure'), [Input('intermediate-value', 'children')])
def update_graph_1(jsonified_data):

    # more generally, this line would be
    # json.loads(jsonified_cleaned_data)
    ppPop = pd.read_json(jsonified_data)
    figScat = px.scatter(ppPop, x='Prey', y='Predator')
    figScat.update_layout(title={'text': "Predator-Prey Scatterplot" })
    return figScat

@app.callback(Output('popvpop', 'figure'), [Input('intermediate-value', 'children')])
def update_graph_2(jsonified_data):

    # more generally, this line would be
    # json.loads(jsonified_cleaned_data)
    ppPop = pd.read_json(jsonified_data)
    melted = ppPop.melt(id_vars = 'Time',  var_name='Species', value_name='Population' )
    figLine = px.line(melted, x ='Time', y= 'Population', color = 'Species')
    figLine.update_layout(title={'text': "Population Comparison of Prey and Predator through time"}) 
    return figLine


# In[ ]:


app.run_server(host='0.0.0.0')
#server = app.server


# In[ ]:




