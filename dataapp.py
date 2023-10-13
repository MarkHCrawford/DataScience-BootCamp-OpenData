import plotly.express as px
from dash import Dash, html, dcc, callback, Output, Input
from dash import dcc 
from dash import html
import numpy as np
import pandas as pd
import requests as r

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
#importing data

urlemis = "https://data.cityofnewyork.us/resource/k3e2-emsq.json"
remis = r.get(urlemis)
dfemis = pd.read_json(remis.text)

url = "https://data.cityofnewyork.us/resource/wcm8-aq5w.json?$limit=15000"
response = r.get(url)
df = pd.read_json(response.text)
dfyearby_energy = df.groupby(['largest_property_use_type', 'year_built'], as_index=False)['source_eui_kbtu_ft'].sum()
#energyproperty = px.line(x=dfyearby_energy[dfyearby_energy['year_built'] == xaxis_column_name]['Value'],
#                     y=dfyearby_energy[dfyearby_energy['source_eui_kbtu_ft'] == yaxis_name]['Value'],
#                     hover_name=yearby_energy[yearby_energy['Indicator Name'] == yaxis_column_name]['Country Name'])


sourcetype = dfemis.groupby(['sector', 'source_type'], as_index=False)['cy_2016_tco2e'].sum()
emissource = px.bar(sourcetype, x='source_type', y='cy_2016_tco2e', labels = dict(source_type='Emissions Source', cy_2016_tco2e="Total Emissions"))

emissource.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)



#)

#duplicates

df.duplicated()
df.dropna(axis=0,
          how='any',
          inplace=True)

#data type conversion

df['source_eui_kbtu_ft'] = pd.to_numeric(df['source_eui_kbtu_ft'], errors='coerce')
df['net_emissions_metric_tons'] = pd.to_numeric(df['net_emissions_metric_tons'], errors='coerce')
df['site_energy_use_kbtu'] = pd.to_numeric(df['site_energy_use_kbtu'], errors='coerce')
df['energy_star_score'] = pd.to_numeric(df['energy_star_score'], errors='coerce')
df['avoided_emissions_onsite_1'] = pd.to_numeric(df['avoided_emissions_onsite_1'], errors='coerce')

df['total_ghg_emissions_metric'] = pd.to_numeric(df['total_ghg_emissions_metric'], errors='coerce')
df.dropna(axis=0,
          how='any',
          inplace=True)


dfoccupancy = df.groupby('occupancy', as_index=False)['energy_star_score'].mean()
starscore = px.line(dfoccupancy, x='occupancy', y='energy_star_score')
starscore.update_layout(template='plotly_dark')

heatmap1 = px.density_mapbox(df, lat='latitude', lon='longitude', z='total_ghg_emissions_metric', radius = 50,
                        center = dict(lat=40.77, lon=-73.94), zoom= 10,
                        mapbox_style="stamen-terrain")
heatmap1.update_layout(template='plotly_dark')

heatmap2 = px.density_mapbox(df, lat='latitude', lon='longitude', z='site_energy_use_kbtu', radius = 40,
                        center = dict(lat=40.77, lon=-73.94), zoom= 10,
                        mapbox_style="stamen-terrain")
heatmap2.update_layout(template='plotly_dark')
app = Dash(__name__)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(children='NYC Energy and Emissions', style={'textAlign':'center',
                                                        'color':colors['text']}),

    
    html.H2(children='NYC Emissions by type, note the size of residential.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph',
        figure=emissource
    ),
    html.H2(children="We can see that buildings with higher occupancy have a significantly lower energy score.",
    
    style={
        'textAlign':'center',
        'color':colors['text']
   }),
  dcc.Graph(
       id='occupancy',
       figure=starscore
   ),
#         dcc.Dropdown(
#                dfyearby_energy['largest_property_use_type'].unique(),
#                'Adult Education',
#                id='dropdown',
#                style = {
#                    'backgroundColor':colors['background'],
#                    'color':colors['text']
#
 #               }
  #          ),
 #       dcc.Graph(
  #          id='propertyusetype',
  #          figure=energyproperty
   #               ),

    html.H2(children="Here we have two heatmaps. One shows the concentration of energy use in lower Manhattan, and the other shows how that corresponds to emissions.",
    style={
        'textAlign':'center',
        'color':colors['text']
   }),
    dcc.Graph(id='map1',
              figure=heatmap1),
    dcc.Graph(id='map2',
            figure=heatmap2),
])

#@callback(
#    Output('propertyusetype', 'largest_property_use_type'),
#    Input('dropdown', 'value')
#)
#def update_graph(value):
#    dff = df[df.country==value]
#    return px.line(dff, x='year', y='pop')
#
if __name__ == '__main__':
    app.run_server(debug=True)