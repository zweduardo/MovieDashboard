from turtle import title
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

#Get the data from the database
loc1 = r"C:\Users\eduar\Documents\Selenium\themoviedb.db"
themoviedb = sqlite3.connect(loc1)
themoviedf = pd.read_sql_query("SELECT genre_ids,id as movie_id,original_language,title,popularity,release_date,vote_average,vote_count FROM TopRated",themoviedb)
castdf = pd.read_sql_query("SELECT id as CastId,known_for_department,original_name,character,movie_id FROM Cast WHERE known_for_department = 'Acting'",themoviedb)

#Cleaning and Merging the data
themoviedf['vote_average'] = pd.to_numeric(themoviedf['vote_average'])
themoviedf['popularity'] = pd.to_numeric(themoviedf['popularity'])
themoviedf['vote_count'] = pd.to_numeric(themoviedf['vote_count'])
themoviedf['release_date'] = pd.to_datetime(themoviedf['release_date'])
themoviedf['year'] = themoviedf['release_date'].apply(lambda x:str(x.year))
castdf['movie_id'] = pd.to_numeric(castdf['movie_id'])
themoviedf['movie_id'] = pd.to_numeric(themoviedf['movie_id'])
moviesdf = pd.merge(castdf,themoviedf,on='movie_id')

#Setting the page layout
st.set_page_config(layout='wide')
col1,col2,col3,col4,col5 = st.columns(5)
col6 = st.columns(1)
col7,col8 = st.columns(2)
col9,col10,col11 = st.columns(3)
sdbar = st.sidebar

#Creating the sidebar and selection options
name = sdbar.multiselect("Pick a Name",moviesdf['original_name'].unique(),default='Tom Cruise')
number = sdbar.slider("Pick a Minimun Rating",moviesdf['vote_average'].min(),moviesdf['vote_average'].max())

#Creating the dataframes and metrics
graf1df = moviesdf[moviesdf['vote_average'] > number]
graf2df = graf1df[graf1df['vote_count'] > 0]
graf3df = graf2df[graf2df['original_name'].isin(name)]
showdf = graf3df[['original_name','title','character','vote_average','popularity','year','original_language']]


#Creating the dashboard metrics
col1.metric("Total Movies",showdf['title'].count())
col2.metric("Average Rating ",round(showdf['vote_average'].mean(),2),(round(showdf['vote_average'].mean()-moviesdf['vote_average'].mean(),2)))
col3.metric("Average Movie Popularity",round(showdf['popularity'].mean(),2),(round(showdf['popularity'].mean()-moviesdf['popularity'].mean(),2)))
col4.metric("Movies per Year",round(showdf['year'].value_counts().mean(),2))
col5.metric("Main Movie Language",showdf['original_language'].mode()[0])

#Creating the charts
col7.scatter_chart(graf3df,x='vote_average',y='popularity',color='original_language',size='vote_count',use_container_width=True)
col8.bar_chart(graf3df,y='vote_average',x='year',color='original_language',use_container_width=True)
col9.bar_chart(graf3df,y='popularity', x='character',use_container_width=True)
col10.bar_chart(graf3df,y='popularity', x='year',use_container_width=True)

#Creating a popover with the credits
with col11.popover("Credits"):
    st.write("Created by Eduardo Zantut Wittmann: https://www.linkedin.com/in/eduardozw/")
    st.write("Data Provided by The Movie Database: https://www.themoviedb.org/")
    st.write("Dashboard Created with Streamlit: https://www.streamlit.io/ based on a sqlite3 database")

#Creating the expander to show the dataframe
with st.expander("Click this expander to see more information"):
    st.write(showdf.sort_values('vote_average',ascending=False),use_container_width=True)