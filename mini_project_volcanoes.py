import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt
import io
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy

# Load csv
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

volcano_df_raw = load_data(path = "./data/raw/volcano_ds_pop.csv")
df = deepcopy(volcano_df_raw)

# Title + headers
st.title("Volcanoes")
st.text("")

selected2 = option_menu(None, ["Home", "Map", "Warning", 'Contact'], 
    icons=['house', 'map', 'fire', 'person-circle'], 
    menu_icon="cast", default_index=0, orientation="horizontal")

if selected2 == "Home":
    st.title("Home")


if selected2 == "Map":
    st.header("Volcanoes all over the world")
    mapping = {
        'Unknown': 'unknown/uncertain',
        'D1': 'active',
        'D2': 'active',
        'D3': 'active',
        'D4': 'active',
        'D5': 'active',
        'D6': 'active',
        'D7': 'active',
        'U': 'unknown/uncertain',
        'Q': 'quiescent',
        'P': 'potentially active',
        'U1': 'unknown/uncertain',
        'U7': 'unknown/uncertain'
    }

    df['Active State'] = df['Last Known'].map(mapping)

    left_column, middle_column, right_column = st.columns([1,1,2])

    # Hide non-active volcanoes
    if left_column.checkbox("Show only active volcanoes"):
        filtered_df = df[df['Active State'] == 'active']
        filtered_df['Active State'] = filtered_df['Last Known']
        color_mapping = {
            'D1': '#8f787d',
            'D2': '#a8656e',
            'D3': '#b35a64',
            'D4': '#bc4e57',
            'D5': '#c44149',
            'D6': '#ca3338',
            'D7': '#FF0000',
            }
        filtered_df['Active State Color'] = df['Last Known'].map(color_mapping)
        if not middle_column.checkbox("Show all active volcanoes",value=False):
            slider = right_column.select_slider('Slide to select (D1 = Least Active, D7 = Most Active)', options=pd.unique(filtered_df['Last Known'].sort_values()))
            filtered_df = filtered_df[filtered_df['Active State']==slider]
    else:
        filtered_df = df
        color_mapping = {
            'active':'red',
            'unknown/uncertain':'grey',
            'quiescent':'blue',
            'potentially active':'black'
            }
        filtered_df['Active State Color'] = df['Active State'].map(color_mapping)
        multi = right_column.multiselect('Multiselect', ["All"]+sorted(pd.unique(filtered_df['Active State'])))
        if not multi or 'All' in multi:
            pass
        else:
            filtered_df = filtered_df[filtered_df['Active State'].isin(multi)]
        st.toast('CONGRATULATIONS. Now you see all volcanoes!')

    fig = px.scatter_mapbox(
        filtered_df.sort_values(by='Last Known'),
        lat='Latitude',
        lon='Longitude',
        color='Active State',
        color_discrete_map=color_mapping,
        size_max=15,
        hover_name='Volcano Name',
        zoom=0,
        hover_data={'Latitude':False,
                    'Longitude':False,
                    'Active State':True}
    )

    fig.update_traces(
        marker=dict(opacity=1)
    )
    try:
        if 'quiescent' in multi or 'potentially active' in multi:
            fig.update_layout(
                mapbox_style="carto-positron",
                mapbox_zoom=1, 
                mapbox_center={"lat": filtered_df[filtered_df['Active State']==multi[len(multi)-1]]['Latitude'].iloc[0], "lon": filtered_df[filtered_df['Active State']==multi[len(multi)-1]]['Longitude'].iloc[0]},
            )
        else:
            fig.update_layout(
            mapbox_style="carto-positron",
            mapbox_zoom=1, 
            mapbox_center={"lat": 20, "lon": 0},
            )
    except:
        fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=1, 
        mapbox_center={"lat": 20, "lon": 0},
        )

    fig.update_layout(
        width=1000,
        height=600,
    )

    st.plotly_chart(fig)
    
    if st.button('PARTY TIME'):
        st.balloons()



if selected2 == "Warning":
    st.header("Volcano warning")
    st.text("In case of a volcano eruption, a similar warning could be broadcasted on live television:\n")
    st.video('volcano_warning_video.mp4')
    st.text("")
    st.text("Listen here to the warning sound of a volcano eruption:")
    st.audio('volcano_warning.wav')
    with open("volcano_warning.wav", "rb") as f:
        file = f.read()
    st.download_button('Download volcano warning sound',data=file,file_name="Volcano Warning Sound.wav",icon=":material/volcano:",mime="audio/wav")

if selected2 == "Contact":
    st.title("Contact")


# CODE

# Fun things
