import streamlit as st
import pandas as pd
import altair as alt


st.title('Stat Scatter 📊')


# should only run once per session
if "x_axis" not in st.session_state:
    st.session_state['x_axis'] = 'MPG'

if "y_axis" not in st.session_state:
    st.session_state['y_axis'] = 'PPG'


if "games_played" not in st.session_state:
    st.session_state['_games_played'] = 10

if "mpg_played" not in st.session_state:
    st.session_state['mpg_played'] = 0

if "_x_axis" not in st.session_state:
    st.session_state['_x_axis'] = st.session_state.x_axis


if "_y_axis" not in st.session_state:
    st.session_state['_y_axis'] = st.session_state.y_axis

if "_games_played" not in st.session_state:
    st.session_state['_games_played'] = st.session_state.games_played

if "_mpg_played" not in st.session_state:
    st.session_state['_mpg_played'] = st.session_state.mpg_played



df = pd.read_csv(r'datasets\compiled_stats.csv')

with st.container():


            
    relevant_filters = [column for column in df.drop(columns=['Player','Team']).columns]

    def store_value():
        st.session_state['y_axis'] = st.session_state._y_axis   # perma key
        st.session_state['_y_axis'] = st.session_state._y_axis   # temp key
        st.session_state['x_axis'] = st.session_state._x_axis   # perma key
        st.session_state['_x_axis'] = st.session_state._x_axis   # temp key
        st.session_state['games_played'] = st.session_state._games_played   # perma key
        st.session_state['_games_played'] = st.session_state._games_played   # temp key
        st.session_state['mpg_played'] = st.session_state._mpg_played   # perma key
        st.session_state['_mpg_played'] = st.session_state._mpg_played   # temp key

    

    st.number_input('Min. Games Played', 
        min_value=0, 
        max_value=int(df['GP'].max()),
        on_change=store_value,
        key='_games_played')


    
    col1, col2 = st.columns(2)


    with col1:
        st.selectbox('Y-axis', 
                       options=relevant_filters,
                       on_change=store_value,
                       key='_y_axis')
        
    with col2:
        st.selectbox('X-axis', 
                       options=relevant_filters,
                       on_change=store_value,
                       key='_x_axis')
    
    filtered_df = df[   (df['GP'] >= st.session_state._games_played)
                    ]

    chart = alt.Chart(filtered_df).mark_circle().encode(
        alt.X(st.session_state._x_axis).scale(zero=False),
        alt.Y(st.session_state._y_axis).scale(zero=False, padding=1),
        color='Team',
        size=st.session_state._y_axis,
        description='Player'
    )


    st.altair_chart(chart)
