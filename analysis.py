#dataset located here: https://www.kaggle.com/datasets/asaniczka/mountain-climbing-accidents-dataset
import pandas as pd

df = pd.read_csv('deaths_on_eight-thousanders.csv', parse_dates=['Date'])

df['year'] = df['Date'].dt.year

print(df.head())

print(len(df))

print(type(df))

print(df.filter(items=['Mountain']))

print(df.Mountain.unique())

print(df.describe())

from arrow import now
from geocoder import arcgis

mountain_df = pd.DataFrame.from_dict(orient='index', data={mountain: arcgis(location=mountain).latlng for mountain in df['Mountain'].unique().tolist()}, ).reset_index().merge(right=df['Mountain'].value_counts().to_frame().reset_index(), left_on='index', right_on='Mountain', how='inner').drop(columns=['Mountain'])
mountain_df.columns = ['Mountain', 'latitude', 'longitude', 'count']

from warnings import filterwarnings
filterwarnings(action='ignore', category=FutureWarning)

from plotly.express import scatter_mapbox
scatter_mapbox(data_frame=mountain_df, lat='latitude', lon='longitude', size='count', hover_name='Mountain', mapbox_style='open-street-map', zoom=3, height=900).show()

from plotly.express import histogram
histogram(data_frame=df.sort_values(by='Mountain'), x='Date', color='Mountain').show()
#This plot demonstrates how Everest dominates the overall totals.
histogram(data_frame=df, x='Mountain').show()

#The breakdown by nationality shows how unevenly the fatalities are distributed; the cause of death data is too noisy to be useful for a volumetric breakdown.
for column in ['Nationality', 'Cause of death']:
    histogram(data_frame=df, y=column, height=1500).show()

#We can combine the nationality and mountain data and add name and year data and we get as complete a view as we can for this many dimensions of data; unfortunately because the strip plot treats years as categorical our colors are not especially helpful.
from plotly.express import strip
strip(data_frame=df, y='Nationality', x='Mountain', hover_name='Name', hover_data=['Date'], height=1500, stripmode='overlay', color='year').show()

#This view is so sparse it may not be a useful way to understand the data other than realizing most of the fatalities are from Nepal and most of them have died on Everest.
from plotly.express import scatter
scatter(data_frame=df[['Nationality', 'Mountain']].groupby(by=['Nationality', 'Mountain']).size().reset_index().rename(columns={0: 'count'}),
        x='Mountain', y='Nationality', size='count', height=1500).show()