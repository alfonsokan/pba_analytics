import streamlit as st
import pandas as pd



st.title('League Leaders 📈')


if 'stat_leaders' not in st.session_state:
    st.session_state['stat_leaders'] = 'PPG'

if '_stat_leaders' not in st.session_state:
    st.session_state['stat_leaders'] = st.session_state.stat_leaders

if 'min_games_played' not in st.session_state:
    st.session_state['min_games_played'] = 0

if '_min_games_played' not in st.session_state:
    st.session_state['_min_games_played'] = st.session_state.min_games_played

if "stat_type_lead" not in st.session_state:
    st.session_state['stat_type_lead'] = 'Averages'
if "_stat_type_lead" not in st.session_state:
    st.session_state['_stat_type_lead'] = st.session_state.stat_type_lead

def chosen_df(stat_type):
    if stat_type == 'Averages':
        df = pd.read_csv(r'datasets/avg_stats.csv').set_index('#')
    elif stat_type == 'Totals':
        df = pd.read_csv(r'datasets/total_stats.csv').set_index('#')
    elif stat_type == 'Per 36':
        df = pd.read_csv(r'datasets/per36_stats.csv').set_index('#')
    elif stat_type == 'Advanced':
        df = pd.read_csv(r'datasets/adv_stats_cleaned.csv').set_index('#')
    else:
        df = pd.read_csv(r'datasets/misc_stats_cleaned.csv').set_index('#')
    return df

df = chosen_df(st.session_state._stat_type_lead)


def store_value():
    st.session_state['stat_leaders'] = st.session_state._stat_leaders
    st.session_state['_stat_leaders'] = st.session_state._stat_leaders
    st.session_state['min_games_played'] = st.session_state._min_games_played
    st.session_state['_min_games_played'] = st.session_state._min_games_played

    
col1, col2 = st.columns(2)

with col1:
    st.number_input('Min. Games Played', 
        min_value=0, 
        max_value=int(df['GP'].max()),
        on_change=store_value,
        key='_min_games_played')

def store_type():

    st.session_state['stat_type_lead'] = st.session_state._stat_type_lead
    st.session_state['_stat_type_lead'] = st.session_state._stat_type_lead

    st.session_state['_stat_leaders'] = 'GP'
    st.session_state['stat_leaders'] = 'GP'

with col2:
    st.selectbox('Pick a stat type',
    options = ['Averages', 'Totals', 'Per 36', 'Advanced', 'Miscellaneous'],
    key = '_stat_type_lead',
    on_change=store_type)

st.selectbox(
    label = 'Select a stat',
    options = df.drop(columns=['Player', 'Team']).columns,
    key = '_stat_leaders',
    on_change= store_value
)
    

output_df = df[
            (df['GP'] >= st.session_state._min_games_played)
            ]

try:
    st.write(output_df
            .sort_values(by = st.session_state.stat_leaders, ascending=False)
            .reset_index()
            .set_axis(range(1, len(output_df)+1))      # make index start at 1 instead of 0
            [['Player', st.session_state.stat_leaders, 'GP']]
         )
except ValueError as e:
    if "Duplicate column names" in str(e):
        st.write(output_df
                    .sort_values(by = st.session_state.stat_leaders, ascending=False)
                    .reset_index()
                    .set_axis(range(1, len(output_df)+1))      # make index start at 1 instead of 0
                    [['Player', st.session_state.stat_leaders]]
                )