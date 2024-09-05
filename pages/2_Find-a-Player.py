import streamlit as st
import pandas as pd

st.title('Find-a-Player 🔎')

# should only run once per session
if "player_team" not in st.session_state:
    st.session_state['player_team'] = 'No selection'


# saves last option chosen even after switching pages
if "_player_team" not in st.session_state:
    st.session_state['_player_team'] = st.session_state.player_team

#################

if "filters_submitted" not in st.session_state:
    st.session_state['filters_submitted'] = False

if "stat_type_find" not in st.session_state:
    st.session_state['stat_type_find'] = 'Averages'


if "_stat_type_find" not in st.session_state:
    st.session_state['_stat_type_find'] = st.session_state.stat_type_find

if "chosen_stats_find" not in st.session_state:
    st.session_state['chosen_stats_find'] = ['GP']

if "_chosen_stats" not in st.session_state:
    st.session_state['_chosen_stats_find'] = st.session_state.chosen_stats_find




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



shortened_teams_list = ['NONE', 'ALL'] + list(sorted(df['Team'].unique()))


pba_teams_mapping = {
    'NONE': 'No selection',
    'ALL': 'All',
    'BGK': 'Barangay Ginebra San Miguel',
    'BLAC': 'Blackwater Bossing',
    'SHOT': 'Blackwater Bossing',
    'DYIP': 'Terrafirma Dyip',
    'MER': 'Meralco Bolts',
    'NLEX': 'NLEX Road Warriors',
    'NPB': 'NorthPort Batang Pier',
    'XERS': 'Phoenix Super LPG Fuel Masters',
    'FUEL': 'Phoenix Super LPG Fuel Masters',
    'ROS': 'Rain or Shine Elasto Painters',
    'SMB': 'San Miguel Beermen',
    'TNT': 'TNT Tropang Giga'
}

reverse_mapping = {full_name: abbreviation for abbreviation, full_name in pba_teams_mapping.items()}

full_names = [pba_teams_mapping.get(team, 'N/A') for team in shortened_teams_list]

def store_value():
    st.session_state['player_team'] = st.session_state._player_team     # perma key
    st.session_state['_player_team'] = st.session_state._player_team    # temp key

    st.session_state['stat_type_find'] = st.session_state._stat_type_find
    st.session_state['_stat_type_find'] = st.session_state._stat_type_find

    st.session_state['player_team'] = st.session_state._player_team     # perma key
    st.session_state['_player_team'] = st.session_state._player_team    # temp key

    st.session_state['chosen_stats_find'] = st.session_state._chosen_stats_find
    st.session_state['_chosen_stats_find'] = st.session_state._chosen_stats_find

def store_type():
    st.session_state['chosen_stats_find'] =['GP']
    
    st.session_state['stat_type_find'] = st.session_state._stat_type_find
    st.session_state['_stat_type_find'] = st.session_state._stat_type_find

    st.session_state['player_team'] = st.session_state._player_team     # perma key
    st.session_state['_player_team'] = st.session_state._player_team    # temp key



st.selectbox('Pick a team', 
             options = full_names, 
             key = '_player_team',
             on_change=store_value      # goes to the store_selected_team() function
             )



with st.sidebar:
    # slider_val = st.slider("Form slider")
    relevant_filters = [column for column in df.drop(columns=['Player','Team']).columns]
    st.selectbox('Pick a stat type',
        options = ['Averages', 'Totals', 'Per 36', 'Advanced', 'Miscellaneous'],
        key = '_stat_type_find',
        on_change=store_type)
    
    with st.form('filter_form'):
        st.multiselect("Click 'Apply' to submit changes:", 
                       options = relevant_filters, 
                       default=['GP'],
                       key='chosen_stats_find')
        
        submitted = st.form_submit_button("Apply")
        if submitted:
            st.session_state.filters_submitted = True
    
if st.session_state.filters_submitted:
    num_columns = 2
    columns = st.columns(num_columns)

    for index, filter in enumerate(st.session_state.chosen_stats_find):
        with columns[index % num_columns]:
            st.slider(filter, 0, 50, (0,50), key=filter)

    if st.session_state._player_team == 'All':
        selected_team_df = df
        
    else:
        selected_team_df = df[df['Team'] == reverse_mapping.get(st.session_state._player_team)]




    # case where person chooses more than one filter


    if len(st.session_state.chosen_stats_find) > 1:
        slider_dict = {}
        filter_statement = []

        for filter in st.session_state.chosen_stats_find:
            filter_tuple = st.session_state.get(filter)
            slider_dict[filter] = filter_tuple
            statement = f"(selected_team_df['{filter}'] <= {filter_tuple[1]}) & (selected_team_df['{filter}'] >= {filter_tuple[0]})"
            filter_statement.append(statement)

        combined_filter_statement = " & ".join(filter_statement)
        output_df = selected_team_df[eval(combined_filter_statement)]
        final_df = output_df.reset_index().set_axis(range(1, len(output_df)+1))
        st.write(final_df)

    elif len(st.session_state.chosen_stats_find) == 1:
        statement = f"(selected_team_df['{st.session_state.chosen_stats_find[0]}'] <= {st.session_state.get(st.session_state.chosen_stats_find[0])[1]}) & (selected_team_df['{st.session_state.chosen_stats_find[0]}'] >= {st.session_state.get(st.session_state.chosen_stats_find[0])[0]})"
        output_df = selected_team_df[eval(statement)]
        final_df = output_df.reset_index().set_axis(range(1, len(output_df)+1))
        st.write(final_df)

    else:
        st.write(selected_team_df)

else:
    st.write("Click on 'Apply' to display results")
