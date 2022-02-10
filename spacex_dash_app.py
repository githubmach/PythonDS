#!pip3 install pandas dash
#!pip3 install wget
#wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
#wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/spacex_dash_app.py"
#python3 spacex_dash_app.py

# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
#import wget
# Read the airline data into pandas dataframe
#fn = wget.download("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
#spacex_df = pd.read_csv(fn)
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()+1000
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', 
                                             options=[{'label': 'All Sites', 'value':'ALL'}, 
                                                      {'label':'CCAFS LC-40', 'value':'site1'},
                                                      {'label':'CCAFS SLC-40', 'value':'site2'},
                                                      {'label':'KSC LC-39A', 'value':'site3'},
                                                      {'label':'VAFB SLC-4E', 'value':'site4'},
                                                     ],
                                             value='ALL',
                                             placeholder="Select a Launch Site here",
                                             searchable=True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, 
                                                step=1000,
                                                #marks={0: '0',100: '100'},
                                                value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    #filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site',  
        title='Total Success Launches By Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        launchsite_name = {'site1':'CCAFS LC-40', 'site2':'CCAFS SLC-40', 
                           'site3':'KSC LC-39A', 'site4':'VAFB SLC-4E'}
        filtered_df = spacex_df[spacex_df['Launch Site']==launchsite_name[entered_site]]
        values = filtered_df['class'].apply(lambda x: 1)
        fig = px.pie(filtered_df, values=values, names='class',  
        title='Total Success Launches for site %s' %launchsite_name[entered_site])
        return fig
        
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, entered_payload):
    #filtered_df = spacex_df
    if entered_site == 'ALL':
        filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].
                      apply(lambda x: x>entered_payload[0] and x<entered_payload[1] )]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version',
                         title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        launchsite_name = {'site1':'CCAFS LC-40', 'site2':'CCAFS SLC-40', 
                           'site3':'KSC LC-39A', 'site4':'VAFB SLC-4E'}
        filtered_df = spacex_df[spacex_df['Launch Site']==launchsite_name[entered_site]]
        filtered_df = filtered_df[filtered_df['Payload Mass (kg)'].
                      apply(lambda x: x>entered_payload[0] and x<entered_payload[1] )]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version',  
        title='Correlation between Payload and Success for site %s' %launchsite_name[entered_site])
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()