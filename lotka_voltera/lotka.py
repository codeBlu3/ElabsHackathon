import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
#plotly graph objects to create the plot itself
import plotly.graph_objs as go

app= dash.Dash()
#Our dash will be very simple, just the graph
app.layout = html.Div([dcc.Graph(id='graph'),
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
                                     value=.05)])])

#Telling Dash that the sliders are inputs into the graph
@app.callback(Output('graph','figure'),
             [Input('alpha','value'),
             Input('beta','value'),
             Input('gamma','value'),
             Input('delta','value')])
#And this function takes the inputs, runs the model and plots the output
def update_figure(alpha,beta,gamma,delta):
    xs = [50]
    ys = [20]
    

    for n in range(1000):
        new_x = xs[-1] + ((alpha - beta*ys[-1])*xs[-1])*.01
        new_y = ys[-1] + ((delta*xs[-1] - gamma)*ys[-1])*.01
        xs.append(new_x)
        ys.append(new_y)
    
    data = [go.Scatter(x=list(range(0,1001)), y=xs, mode='lines', name='Prey'),
            go.Scatter(x=list(range(0,1001)), y=ys, mode='lines', name='Predator')]
    layout = go.Layout(title = f'Lotka-Volterra')
    return {'data':data,'layout':layout}



app.run_server(host='0.0.0.0')
#server = app.server
