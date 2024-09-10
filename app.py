import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import plotly.express as px 
from util_app import get_aggregate_each, plot_agg_each, plot_agg

#https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config
st.set_page_config(
    page_title="EEIO-Indonesia",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Dashboard title
st.title('Indonesia Carbon Footprint Calculator')
st.subheader('Environment Sustainability Project')

# Create tabs
tab1, tab2, tab3 = st.tabs(["Emission", "Data Center", "About"])

with tab1:
    # SIDEBAR
    #st.sidebar.header("This is my sidebar")

    col1, col2 = st.columns([1,2])

    with col1:
        st.subheader('Header column 1')

        fpath = "data/list_agg_sectors.xlsx"
        df_lagg = pd.read_excel(fpath)
        lst = df_lagg['Aggregated sectors'].tolist()
        lst.insert(0, "--All Sectors--")

        opt_sector = st.selectbox("Category of Aggregated Sectors",lst)
        #print(type(opt_sector)) #str
    
    with col2:
        st.subheader('Header column 2')
        # Show static DataFrame
        #st.write(opt_sector)

        #opt_sector="Energy"
        if (opt_sector != "--All Sectors--"):
            df_agg_sectors_each = pd.read_excel("buf/result_agg_sectors_each.xlsx")
            df_selected=df_agg_sectors_each[df_agg_sectors_each["Aggregated sectors"] == opt_sector]
            
            plot_agg_each(df_selected, opt_sector)
            
        else:
            saved_file_path = "buf/result_agg_sectors.xlsx"
            df_agg_sectors = pd.read_excel(saved_file_path)
            df_agg_sectors.set_index('Aggregated sectors', inplace=True)
            #st.dataframe(df_agg_sectors)
            plot_agg(df_agg_sectors)

with tab2:
    uploaded_file = st.file_uploader("Choose a file", type = 'xlsx')

    if uploaded_file is not None:
        df1 = pd.read_excel(uploaded_file)
        st.dataframe(df1)
        #print(df1)

with tab3:
    st.write("Indonesia Carbon Footprint Calculator")
    st.write("Version 0.0.1")
    st.write("September 2024")