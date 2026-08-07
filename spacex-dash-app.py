# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

unique_launch_sites = spacex_df['Launch Site'].unique().tolist()

launch_sites = [
    {'label': 'All Sites', 'value': 'All Sites'}
]

for site in unique_launch_sites:
    launch_sites.append({'label': site, 'value': site})

# Create slider marks
marks_dict = {}

for i in range(0, 11000, 1000):
    marks_dict[i] = {'label': str(i) + ' Kg'}

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=launch_sites,
                                    value='All Sites',
                                    placeholder='Select a Launch Site',
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
                                dcc.RangeSlider(
                                    id='payload_slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    marks=marks_dict,
                                    value=[min_payload, max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def get_pie_chart(entered_site):

    if entered_site == 'All Sites':

        data = spacex_df[
            spacex_df['class'] == 1
        ]

        fig = px.pie(
            data,
            names='Launch Site',
            title='Total Success Launches by Site'
        )

    else:

        data = spacex_df[
            spacex_df['Launch Site'] == entered_site
        ]

        fig = px.pie(
            data,
            names='class',
            title='Success vs Failure for site ' + entered_site
        )

    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [
        Input('site-dropdown', 'value'),
        Input('payload_slider', 'value')
    ]
)
def get_scatter_chart(entered_site, payload_slider):

    low, high = payload_slider

    data = spacex_df[
        spacex_df['Payload Mass (kg)'].between(low, high)
    ]

    if entered_site != 'All Sites':

        data = data[
            data['Launch Site'] == entered_site
        ]

        title_text = (
            'Correlation between Payload and Success for site '
            + entered_site
        )

    else:

        title_text = (
            'Correlation between Payload and Success for all Sites'
        )

    # Scatter plot
    fig = px.scatter(
        data,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title=title_text
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run()
