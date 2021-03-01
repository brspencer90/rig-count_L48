# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 13:51:28 2020

@author: Bryan
"""

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objects as go
import pandas as pd
import numpy as np
import datetime as dt

today = dt.date.today()
this_month = pd.to_datetime(str(today.year)+'-'+str(today.month)+'-01')

data_processed_dir = 'C:\\Users\\Bryan\\OneDrive\\02 GitHub\\rig-count_L48\\data\\processed\\'

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

colors = {
    'paper': '#000000',
    'background': '#4E4E4E',
    'header': '#7F7F7F',
    'text':'#FFFFFF'
    }

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv(data_processed_dir+'processed_weekly_class_full.csv',parse_dates=True)
df.date = pd.to_datetime(df.date)

closest_date = df.dropna().date.max().strftime('%Y-%m-%d')

fig = go.Figure(data=go.Scatter(x=df.date, y=df['Total US RigCount'],mode='lines',name='Rig Count'))

for ser in fig['data']:
    ser['text']=[d.strftime('%Y-%m-%d') for d in df.date]
    ser['hovertemplate']='<br>Date=%{text}<br>''Rig Count''=%{y}<extra></extra>'

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['paper'],
    font_color=colors['text']
    )
        
app.layout = html.Div(
    children=[
        html.H1(
            children='USA Oil Rig Count Predictor',
            style={
                'textAlign':'center',
                'color':colors['header'],
                'backgroundColor':colors['paper']
                }
        ),
    
        html.Div(
            children='Interactive web application for predicting the US Oil Rig Count',
            style={
                'textAlign':'center',
                'color': colors['text']
                }
        ),
        
        html.Hr(),
    
        dcc.Graph(
            id='rig-count-graph',
            figure=fig
        ),
        html.Hr(),
        
        html.H6("Data Input for Model : ",
                style={
                    'color':colors['header']
                    }
                ),
        html.Div(['Select Initial Date (YYYY-MM-DD): ',
                  dcc.Input(id='initial-date',value=closest_date,type='text'),
                  html.Button(id='initial-date-submit',children='Submit'),
                  ],
                 style={
                      'textAlign':'left',
                      'color':colors['text']}
                 ),
        html.Br(),
        html.Div([html.Label('Rig Count : '),
                  dcc.Input(id='rig-count',value=df['Total US RigCount'][df.date==closest_date].values[0],
                            type='number'),
                  html.Label('WTI Price ($/bbl): '),
                  dcc.Input(id='oil-price',value=round(df['wti_spot'][df.date==closest_date].values[0],2),
                            type='number'),
                  html.Label('US Net Imports of Oil (Mbpd): '),
                  dcc.Input(id='usa-net-import',value=round(df['usa_net_import_smooth'][df.date==closest_date].values[0],3),
                            type='number'),
                  html.Label('US L48 Production (Mbpd) : '),
                  dcc.Input(id='usa-l48-prod',value=round(df['usa_l48_prod_smooth'][df.date==closest_date].values[0],3),
                            type='number'),
                  html.Label('US SPR Stocks of Crude Oil (Mbpd): '),
                  dcc.Input(id='usa-stocks-spr',value=round(df['usa_stocks_spr'][df.date==closest_date].values[0],3),
                            type='number'),                  
                  html.Label('OPEC Total Production (Mbpd): '),
                  dcc.Input(id='opec-tot-prod',value=round(df['opec_tot_prod'][df.date==closest_date].values[0],3),
                            type='number'),
                  html.Label('OPEC Crude Capacity (Mbpd): '),
                  dcc.Input(id='opec-crud-capac',value=round(df['opec_crud_capac'][df.date==closest_date].values[0],3),
                            type='number'),
                  html.Label('OPEC Surplus Capacity (Mbpd): '),
                  dcc.Input(id='opec-surp-capac',value=round(df['opec_surp_capac'][df.date==closest_date].values[0],3),
                            type='number'),
                  html.Label('Non-OPEC Total Production (Mbpd): '),
                  dcc.Input(id='non-opec-tot-prod',value=round(df['non-opec_tot_prod'][df.date==closest_date].values[0],3),
                            type='number'),
                  html.Label('OECD Consumption (Mbpd): '),
                  dcc.Input(id='oecd-cons',value=round(df['oecd_cons_smooth'][df.date==closest_date].values[0],3),
                            type='number')
                  ],
                 style={
                      'textAlign':'left',
                      'color':colors['text']}
                 ),        
        
    ],
    
    style={
        'backgroundColor':colors['paper']
        }
)

@app.callback(
    Output('rig-count-graph','figure'),
    Input('initial-date-submit','n_clicks'),
    State('initial-date','value'),
    prevent_initial_call=True)
def update_graph_initial_date(n_clicks,initial_date):
    closest_date = df.date[df.date <= initial_date][df.date[df.date <= initial_date].index[0]].strftime('%Y-%m-%d') 
   
    predict_date = dt.datetime.strptime(closest_date,'%Y-%m-%d') + dt.timedelta(weeks=8)
   
    fig_up = go.Figure(go.Scatter(x=df.date, 
                                y=df['Total US RigCount'],mode='lines',name='Rig Count'))
    fig_up.add_trace(go.Scatter(x=pd.Series(closest_date),
                                y=df['Total US RigCount'][df.date == closest_date],
                                mode='markers',name='Initial Date')
                     )

    fig_up.add_trace(go.Scatter(x=[predict_date,predict_date],y=[0,df['Total US RigCount'].max()],
                                mode='lines',name='Predicted Date',
                                line = dict(color='green', width=2, dash='dash')))
    

    for ser in fig_up['data']:
        ser['text']=[d.strftime('%Y-%m-%d') for d in df.date]
        ser['hovertemplate']='<br>Date=%{text}<br>''Rig Count''=%{y}<extra></extra>'

    fig_up.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['paper'],
        font_color=colors['text'],
        )
    
    return fig_up

@app.callback(
    Output('initial-date','value'),
    Input('initial-date-submit','n_clicks'),
    State('initial-date','value'),
    prevent_initial_call=True)
def update_date_initial_date(n_clicks,initial_date):
    closest_date = df.date[df.date <= initial_date][df.date[df.date <= initial_date].index[0]].strftime('%Y-%m-%d') 

    return closest_date    

@app.callback(
    Output('rig-count','value'),
    Input('initial-date-submit','n_clicks'),
    State('initial-date','value'),
    prevent_initial_call=True)
def update_rig_count_initial_date(n_clicks,initial_date):
    closest_date = df.date[df.date <= initial_date][df.date[df.date <= initial_date].index[0]].strftime('%Y-%m-%d') 

    return df['Total US RigCount'][df.date==closest_date].values[0]

@app.callback(
    Output('oil-price','value'),
    Input('initial-date-submit','n_clicks'),
    State('initial-date','value'),
    prevent_initial_call=True)
def update_oil_price_initial_date(n_clicks,initial_date):
    closest_date = df.date[df.date <= initial_date][df.date[df.date <= initial_date].index[0]].strftime('%Y-%m-%d') 

    return round(df['wti_spot'][df.date==closest_date].values[0],2)

@app.callback(
    Output('usa-net-import','value'),
    Input('initial-date-submit','n_clicks'),
    State('initial-date','value'),
    prevent_initial_call=True)
def update_usa_net_import_initial_date(n_clicks,initial_date):
    closest_date = df.date[df.date <= initial_date][df.date[df.date <= initial_date].index[0]].strftime('%Y-%m-%d') 

    return round(df['usa_net_import_smooth'][df.date==closest_date].values[0],3)

@app.callback(
    Output('usa-l48-prod','value'),
    Input('initial-date-submit','n_clicks'),
    State('initial-date','value'),
    prevent_initial_call=True)
def update_usa_l48_prod_initial_date(n_clicks,initial_date):
    closest_date = df.date[df.date <= initial_date][df.date[df.date <= initial_date].index[0]].strftime('%Y-%m-%d') 

    return round(df['usa_l48_prod_smooth'][df.date==closest_date].values[0],3)

@app.callback(
    Output('usa-stocks-spr','value'),
    Input('initial-date-submit','n_clicks'),
    State('initial-date','value'),
    prevent_initial_call=True)
def update_usa_stocks_spr_initial_date(n_clicks,initial_date):
    closest_date = df.date[df.date <= initial_date][df.date[df.date <= initial_date].index[0]].strftime('%Y-%m-%d') 

    return round(df['usa_stocks_spr'][df.date==closest_date].values[0],3)

@app.callback(
    Output('opec-tot-prod','value'),
    Input('initial-date-submit','n_clicks'),
    State('initial-date','value'),
    prevent_initial_call=True)
def update_opec_tot_prod_initial_date(n_clicks,initial_date):
    closest_date = df.date[df.date <= initial_date][df.date[df.date <= initial_date].index[0]].strftime('%Y-%m-%d') 

    return round(df['opec_tot_prod'][df.date==closest_date].values[0],3)

@app.callback(
    Output('opec-crud-capac','value'),
    Input('initial-date-submit','n_clicks'),
    State('initial-date','value'),
    prevent_initial_call=True)
def update_opec_crud_capac_initial_date(n_clicks,initial_date):
    closest_date = df.date[df.date <= initial_date][df.date[df.date <= initial_date].index[0]].strftime('%Y-%m-%d') 

    return round(df['opec_crud_capac'][df.date==closest_date].values[0],3)

@app.callback(
    Output('opec-surp-capac','value'),
    Input('initial-date-submit','n_clicks'),
    State('initial-date','value'),
    prevent_initial_call=True)
def update_opec_surp_capac_initial_date(n_clicks,initial_date):
    closest_date = df.date[df.date <= initial_date][df.date[df.date <= initial_date].index[0]].strftime('%Y-%m-%d') 

    return round(df['opec_surp_capac'][df.date==closest_date].values[0],3)

@app.callback(
    Output('non-opec-tot-prod','value'),
    Input('initial-date-submit','n_clicks'),
    State('initial-date','value'),
    prevent_initial_call=True)
def update_non_opec_tot_prod_initial_date(n_clicks,initial_date):
    closest_date = df.date[df.date <= initial_date][df.date[df.date <= initial_date].index[0]].strftime('%Y-%m-%d') 

    return round(df['non-opec_tot_prod'][df.date==closest_date].values[0],3)

@app.callback(
    Output('oecd-cons','value'),
    Input('initial-date-submit','n_clicks'),
    State('initial-date','value'),
    prevent_initial_call=True)
def update_oecd_cons_initial_date(n_clicks,initial_date):
    closest_date = df.date[df.date <= initial_date][df.date[df.date <= initial_date].index[0]].strftime('%Y-%m-%d') 

    return round(df['oecd_cons_smooth'][df.date==closest_date].values[0],3)


if __name__ == '__main__':
    app.run_server(debug=True)