import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout='wide')
st.header("Uber Data Analysis")

df=pd.read_csv('Uber Request Data.csv')
df['Request timestamp']=df['Request timestamp'].apply(lambda x:x.replace('-','/'))
df['Drop timestamp'].fillna('-',inplace=True)
df['Drop timestamp']=df['Drop timestamp'].apply(lambda x:x.replace('-','/'))

df['Request timestamp']=pd.to_datetime(df['Request timestamp'],errors='coerce')
df['Drop timestamp']=pd.to_datetime(df['Drop timestamp'],errors='coerce')

df['OrderTime']=df['Request timestamp'].dt.hour
df['OrderWeekDay']=df['Request timestamp'].dt.day_name()
df['OrderMonth']=df['Request timestamp'].dt.month

df["OrderTime"].fillna(0,inplace=True)
df['OrderTime']=df["OrderTime"].astype('int32')

df['DropTime']=df['Drop timestamp'].dt.hour
df['Duration']=df['Drop timestamp']-df['Request timestamp']
df['total_minutes'] = df['Duration'].dt.total_seconds() / 60


def time_definitation(x):
    if x<5:
        return "Early Morning"
    elif x<10:
        return "Morning"
    elif x<14:
        return "Noon"
    elif x<16:
        return "After Noon"
    elif x<21:
        return "Evening"
    else:
        return "Night"


df["Time Range"]=df['OrderTime'].apply(time_definitation)


st.sidebar.header("Filter Data")
status = ["All"] + sorted(df["Status"].unique().tolist())
selected_status = st.sidebar.selectbox("Select Status", status)

timerange = ["All"] + sorted(df["Time Range"].unique().tolist())
selected_timerange = st.sidebar.selectbox("Select Time Range", timerange)


if selected_status != 'All':
    df=df[df['Status']==selected_status]
if selected_timerange != 'All':
    df=df[df['Time Range']==selected_timerange]



st.subheader("📊 Key Metrics")

col1,col2,col3=st.columns(3)

import numpy as np
complete_percent=np.round(len(df[df['Status']=='Trip Completed'])/len(df),2)

col1.metric("Total TripCompleted Percentage ",complete_percent,'%')
col2.metric("Highest demanded pickup point ",'City')
col3.metric("Highest demanded Week Day",' Monday ')

st.subheader("Peak Week Day")
col1,col2=st.columns(2)

with col1:
    filter_value=df.groupby("OrderWeekDay").size().reset_index(name='Count')
    fig=px.bar(filter_value,x='OrderWeekDay',y='Count')
    st.plotly_chart(fig)

with col2:
    filter_value=df.groupby(["OrderWeekDay","Status"]).size().reset_index(name='Count')
    fig=px.bar(filter_value,x='OrderWeekDay',y='Count',color='Status')
    st.plotly_chart(fig)



with st.expander("View Data"):
    st.table(df)