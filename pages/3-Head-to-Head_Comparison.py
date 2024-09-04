import streamlit as st
import pandas as pd

st.title('Head-to-Head Comparison 🆚')

df = pd.read_csv(r'datasets\avg_stats.csv').set_index('#')

col1, col2 = st.columns(2)

# should only run once per session
if "player1" not in st.session_state:
    st.session_state['player1'] = 'Robert Bolick'

# should only run once per session
if "player2" not in st.session_state:
    st.session_state['player2'] = 'Juami Tiongson'

# saves last option chosen even after switching pages
if "_player1" not in st.session_state:
    st.session_state['_player1'] = st.session_state.player1

# saves last option chosen even after switching pages
if "_player2" not in st.session_state:
    st.session_state['_player2'] = st.session_state.player2

if "filters_submitted_comparison" not in st.session_state:
    st.session_state['filters_submitted_comparison'] = False

if "stat_type_head" not in st.session_state:
    st.session_state['stat_type_head'] = 'Averages'


if "_stat_type_head" not in st.session_state:
    st.session_state['_stat_type_head'] = st.session_state.stat_type_head

if "chosen_stats_head" not in st.session_state:
    st.session_state['chosen_stats_head'] = ['GP']

if "_chosen_stats_head" not in st.session_state:
    st.session_state['_chosen_stats_head'] = st.session_state.chosen_stats_head



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


df = chosen_df(st.session_state._stat_type_head)


with st.container():
    def update_options():
        # Update the options for each multiselect based on the selections in the other multiselect
        player1_options = [player for player in df['Player'] if player not in st.session_state.player2]
        player2_options = [player for player in df['Player'] if player not in st.session_state.player1]
        return player1_options, player2_options    
    
    # Update the options for each multiselect based on the current state
    player1_options, player2_options = update_options()
    
    def store_player():
        st.session_state['player1'] = st.session_state._player1   # perma key
        st.session_state['_player1'] = st.session_state._player1    # temp key

        st.session_state['player2'] = st.session_state._player2    # perma key
        st.session_state['_player2'] = st.session_state._player2    # temp key

    
    def store_type():
        st.session_state['chosen_stats_head'] =['GP']

        st.session_state['stat_type_head'] = st.session_state._stat_type_head
        st.session_state['_stat_type_head'] = st.session_state._stat_type_head

        st.session_state['player1'] = st.session_state._player1   # perma key
        st.session_state['_player1'] = st.session_state._player1    # temp key

        st.session_state['player2'] = st.session_state._player2    # perma key
        st.session_state['_player2'] = st.session_state._player2    # temp key
        

    col1, col2 = st.columns(2)

    with col1:
        st.selectbox('Player 1', 
                       options=player1_options, 
                       on_change=store_player,
                       key='_player1')
    
    with col2:
        st.selectbox('Player 2', 
                       options=player2_options, 
                       on_change=store_player,
                       key='_player2')

# st.write(st.session_state)

with st.sidebar:
    # slider_val = st.slider("Form slider")
    relevant_filters = [column for column in df.drop(columns=['Player','Team']).columns]

    st.selectbox('Pick a stat type',
        options = ['Averages', 'Totals', 'Per 36', 'Advanced', 'Miscellaneous'],
        key = '_stat_type_head',
        on_change=store_type)
    
    with st.form('filter_form'):
        st.multiselect("Click 'Apply' to submit changes:", 
                       options = relevant_filters, 
                       default=['GP'],
                       key='chosen_stats_head')
        submitted = st.form_submit_button("Apply")
        if submitted:
            st.session_state.filters_submitted_comparison = True


if st.session_state.filters_submitted_comparison:
    col1, col2 = st.columns(2)

    

    df2 = df[
        (df['Player'] == st.session_state._player1) |
        (df['Player'] == st.session_state._player2)
    ][['Player'] + st.session_state.chosen_stats_head]

    player_stats = {
        row['Player']: {
                stat: row[stat] 
                for stat in st.session_state.chosen_stats_head
            }
        for _, row in df2.iterrows()
    }

    with col1:
        # st.write(st.session_state._player1)
        for index, filter in enumerate(st.session_state.chosen_stats_head):
            stat_value = player_stats[st.session_state._player1][filter]
            delta_value = round(stat_value - player_stats[st.session_state._player2][filter], 2) 
            st.metric(label=filter, value=stat_value, delta=delta_value)

    with col2:
        # st.write(st.session_state._player2)
        for index, filter in enumerate(st.session_state.chosen_stats_head):
            stat_value = player_stats[st.session_state._player2][filter]
            delta_value = round(stat_value - player_stats[st.session_state._player1][filter], 2) 
            st.metric(label=filter, value=stat_value, delta=delta_value)

else:
    st.write("Click on 'Apply' to display results")
