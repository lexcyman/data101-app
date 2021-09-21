from application import app
from flask import render_template, url_for
import pandas as pd
import numpy as mp
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go

# homepage
@app.route('/')
def get_global_plastics_production():
  # import data from data folder
  df = pd.read_csv('data/global-plastics-production.csv')

  # create line graph
  fig = px.line(df, x="Year", y="Global Plastics Production", 
      title='Global Plastics Production (in Million Tonnes) from 1950 to 2015')

  # translate as JSON
  graph1JSON = json.dumps(fig, cls = plotly.utils.PlotlyJSONEncoder)

  # return data
  return render_template('index.html', title='Home', graph1JSON=graph1JSON)

# mismanaged wastes page
@app.route('/mismanaged-wastes')
def get_mismanaged_wastes():
  # import data from data folder
  mismanaged_countries_2010_df = pd.read_csv('data/mismanaged-wastes-2010.csv')
  mismanaged_countries_2019_df = pd.read_csv('data/share-of-global-mismanaged-plastic-waste.csv')

  emitted_countries_2010_df = pd.read_csv('data/plastic-waste-per-capita.csv')
  emitted_countries_2019_df = pd.read_csv('data/share-of-global-plastic-waste-emitted-to-the-ocean.csv')
  
  mismanaged_continents_df = pd.read_csv('data/continents-mismanaged.csv')
  mismanaged_continents_df = mismanaged_continents_df.sort_values('Share of global mismanaged plastic waste', ascending=True)
  
  emitted_continents_df = pd.read_csv('data/continents-emitted.csv')
  emitted_continents_df = emitted_continents_df.sort_values('Share of global plastics emitted to ocean', ascending=True)

  # blue colorscale for the maps
  colorscale = ["#6baed6", "#57a0ce", "#4292c6", "#3082be", "#2171b5", "#1361a9", "#08519c", "#0b4083", "#08306b"]

  # create chloropleth maps
  mismanaged_map_2010_fig = go.Figure(data=go.Choropleth(locations=mismanaged_countries_2010_df['Code'],
                      z=mismanaged_countries_2010_df['Mismanaged wastes'],
                      text=mismanaged_countries_2010_df['Entity'],
                      colorscale=colorscale,
                      autocolorscale=False,
                      reversescale=False,
                      marker_line_color='#313131',
                      marker_line_width=0.5,
                      colorbar_title='Contribution (%)'))
  mismanaged_map_2010_fig.update_layout(title_text='Global Mismanaged Wastes per Country in 2010',
                      title={ 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top' },
                      geo=dict(showframe=False, showcoastlines=False, projection_type='equirectangular'),
                      width=1200,
                      height=600)

  mismanaged_map_2019_fig = go.Figure(data=go.Choropleth(locations=mismanaged_countries_2019_df['Code'],
                      z=mismanaged_countries_2019_df['Share of global mismanaged plastic waste'],
                      text=mismanaged_countries_2019_df['Entity'],
                      colorscale=colorscale,
                      autocolorscale=False,
                      reversescale=False,
                      marker_line_color='#313131',
                      marker_line_width=0.5,
                      colorbar_title='Contribution (%)'))
  mismanaged_map_2019_fig.update_layout(title_text='Global Mismanaged Wastes per Country in 2019',
                      title={ 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top' },
                      geo=dict(showframe=False, showcoastlines=False, projection_type='equirectangular'),
                      width=1200,
                      height=600)

  emitted_map_2010_fig = go.Figure(data=go.Choropleth(locations=emitted_countries_2010_df['Code'],
                      z=emitted_countries_2010_df['Per capita plastic waste'],
                      text=emitted_countries_2010_df['Entity'],
                      colorscale=colorscale,
                      autocolorscale=False,
                      reversescale=False,
                      marker_line_color='#313131',
                      marker_line_width=0.5,
                      colorbar_title='Contribution (%)'))
  emitted_map_2010_fig.update_layout(title_text='Global Plastic Wastes Emitted to the Ocean in 2010',
                      title={ 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top' },
                      geo=dict(showframe=False, showcoastlines=False, projection_type='equirectangular'),
                      width=1200,
                      height=600)

  emitted_map_2019_fig = go.Figure(data=go.Choropleth(locations=emitted_countries_2019_df['Code'],
                      z=emitted_countries_2019_df['Share of global plastics emitted to ocean'],
                      text=emitted_countries_2019_df['Entity'],
                      colorscale=colorscale,
                      autocolorscale=False,
                      reversescale=False,
                      marker_line_color='#313131',
                      marker_line_width=0.5,
                      colorbar_title='Contribution (%)'))
  emitted_map_2019_fig.update_layout(title_text='Global Plastic Wastes Emitted to the Ocean in 2019',
                      title={ 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top' },
                      geo=dict(showframe=False, showcoastlines=False, projection_type='equirectangular'),
                      width=1200,
                      height=600)
  
  # create horizontal bar graphs
  mismanaged_bar_fig = px.bar(mismanaged_continents_df, x='Share of global mismanaged plastic waste', y='Continent', orientation='h',
            title='Global Mismanaged Plastic Wastes per Continent in 2019',
            text='Share of global mismanaged plastic waste')
  mismanaged_bar_fig.update_layout(title={ 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top' })

  emitted_bar_fig = px.bar(emitted_continents_df, x='Share of global plastics emitted to ocean', y='Continent', orientation='h',
            title='Global Plastic Wastes Emitted to the Ocean per Continent in 2019',
            text='Share of global plastics emitted to ocean')
  emitted_bar_fig.update_layout(title={ 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top' })

  # translate as JSON
  continents1JSON = json.dumps(mismanaged_bar_fig, cls = plotly.utils.PlotlyJSONEncoder)
  continents2JSON = json.dumps(emitted_bar_fig, cls = plotly.utils.PlotlyJSONEncoder)
  map1_2010_JSON = json.dumps(mismanaged_map_2010_fig, cls = plotly.utils.PlotlyJSONEncoder)
  map1_2019_JSON = json.dumps(mismanaged_map_2019_fig, cls = plotly.utils.PlotlyJSONEncoder)
  map2_2010_JSON = json.dumps(emitted_map_2010_fig, cls = plotly.utils.PlotlyJSONEncoder)
  map2_2019_JSON = json.dumps(emitted_map_2019_fig, cls=plotly.utils.PlotlyJSONEncoder)

  # return data
  return render_template('mismanaged.html', title='Mismanaged Wastes', 
                      continents1JSON=continents1JSON,
                      continents2JSON=continents2JSON,
                      map1_2010_JSON=map1_2010_JSON,
                      map1_2019_JSON=map1_2019_JSON,
                      map2_2010_JSON=map2_2010_JSON,
                      map2_2019_JSON=map2_2019_JSON)

# marine plastic wastes page
@app.route('/marine-plastic-wastes')
def get_marine_plastic_wastes():
  plastic_marine_df = pd.read_csv('data/plastic-marine-pollution-global-dataset.csv')

  plastic_particles_df = plastic_marine_df[["Latitude","Longitude","CD1","CD2","CD3","CD4"]]
  plastic_particles_df["CD1"]=plastic_particles_df["CD1"].str.replace(',','')
  plastic_particles_df["CD2"]=plastic_particles_df["CD2"].str.replace(',','')
  plastic_particles_df["CD3"]=plastic_particles_df["CD3"].str.replace(',','')
  plastic_particles_df["CD4"]=plastic_particles_df["CD4"].str.replace(',','')
  #plastic_particles_df = pd.to_numeric(plastic_particles_df,errors="coerce")
  #plastic_particles_df(np.nan,0,regex=True)
  plastic_particles_df = plastic_particles_df.astype(float)

  plastic_waste_grams_df = plastic_marine_df[["Latitude","Longitude","WD1","WD2","WD3","WD4"]]
  plastic_waste_grams_df = plastic_waste_grams_df.astype(str)
  plastic_waste_grams_df["WD1"]=plastic_waste_grams_df["WD1"].str.replace(',','')
  plastic_waste_grams_df["WD2"]=plastic_waste_grams_df["WD2"].str.replace(',','')
  plastic_waste_grams_df["WD3"]=plastic_waste_grams_df["WD3"].str.replace(',','')
  plastic_waste_grams_df["WD4"]=plastic_waste_grams_df["WD4"].str.replace(',','')
  #plastic_waste_grams_df = pd.to_numeric(plastic_waste_grams_df,errors="coerce")
  #plastic_waste_grams_df(np.nan,0,regex=True)
  plastic_waste_grams_df = plastic_waste_grams_df.astype(float)

  #plastic_particles_fig = px.scatter(plastic_particles_df)
  plastic_particles_fig = px.scatter_mapbox(plastic_particles_df,lat="Latitude",lon="Longitude")

  plastic_waste_grams_fig = px.scatter_mapbox(plastic_waste_grams_df,lat="Latitude",lon="Longitude")

  plastic_particles_JSON = json.dumps(plastic_particles_fig, cls = plotly.utils.PlotlyJSONEncoder)
  plastic_waste_grams_JSON = json.dumps(plastic_waste_grams_fig, cls = plotly.utils.PlotlyJSONEncoder)
  return render_template('marine.html', title = 'Marine Plastic Wastes',
                      plastic_particles_JSON=plastic_particles_JSON,
                      plastic_waste_grams_JSON=plastic_waste_grams_JSON)

# synthesis of data page
@app.route('/synthesis-of-data')
def get_synthesis_of_data():
  return render_template('synthesis.html', title='Synthesis of Data')