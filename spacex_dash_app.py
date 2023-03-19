# Import required libraries
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

sites = list(pd.unique(spacex_df['Launch Site']))
opts = [{'label': str(st),'value': str(st)} for st in sites]
opts.insert(0, {'label':'All','value':'allsite'})

# Create a dash application
app = Dash(__name__)
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=opts,
                                             value='allsite',
                                             placeholder='Choose Launch Site',
                                             searchable = True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                                                value=[0, 10000]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart',component_property='figure'),
              Input(component_id='site-dropdown',component_property='value'))

def get_pie(site):

    if site=='allsite':
        data = spacex_df[['Launch Site','class']].groupby('Launch Site')['class'].sum().reset_index()
        fig = px.pie(data, values='class', names='Launch Site', title='Total Success Launches by Site')
    else:
        data = spacex_df[spacex_df['Launch Site']==site]
        data = data[['Launch Site','class']].groupby('class')['Launch Site'].count().reset_index()
        fig = px.pie(data, values='Launch Site', names='class', title='Total Success Launches for site {}'.format(site))
    
    return fig
    

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
              [Input(component_id='site-dropdown',component_property='value'),
               Input(component_id='payload-slider',component_property='value')])

def get_scatter(site,mass_range):
    lo, hi = mass_range
    
    if site == 'allsite':
        data = spacex_df[(spacex_df['Payload Mass (kg)'] >= lo) & (spacex_df['Payload Mass (kg)'] <= hi)]
    else:
        data = spacex_df[(spacex_df['Payload Mass (kg)'] >= lo) & (spacex_df['Payload Mass (kg)'] <= hi) & (spacex_df['Launch Site']==site)]
    
    fig = px.scatter(data, x='Payload Mass (kg)', y='class', color='Booster Version Category')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
