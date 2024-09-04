import streamlit as st
import pandas as pd


st.title('Team Overview 📄')


# should only run once per session
if "selected_team" not in st.session_state:
    st.session_state['selected_team'] = 'Barangay Ginebra San Miguel'

# saves last option chosen even after switching pages
if "_selected_team" not in st.session_state:
    st.session_state['_selected_team'] = st.session_state.selected_team


if "stat_type_overview" not in st.session_state:
    st.session_state['stat_type_overview'] = 'Averages'

if "_stat_type_overview" not in st.session_state:
    st.session_state['_stat_type_overview'] = st.session_state.stat_type_overview


if "team_leader_stat" not in st.session_state:
    st.session_state['team_leader_stat'] = "GP"

if "_team_leader_stat" not in st.session_state:
    st.session_state['_team_leader_stat'] = st.session_state.team_leader_stat


if "min_games_played" not in st.session_state:
    st.session_state['min_games_played'] = 10

if "_min_games_played" not in st.session_state:
    st.session_state['_min_games_played'] = st.session_state.min_games_played



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

df = chosen_df(st.session_state._stat_type_overview)


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

if st.session_state._selected_team == 'All':
    selected_team_df = df
    
else:
    selected_team_df = df[df['Team'] == reverse_mapping.get(st.session_state._selected_team)]


col_1, col_2 = st.columns(2)

def store_type():
    st.session_state['selected_team'] = st.session_state._selected_team     # perma key
    st.session_state['_selected_team'] = st.session_state._selected_team    # temp key

    st.session_state['stat_type_overview'] = st.session_state._stat_type_overview
    st.session_state['_stat_type_overview'] = st.session_state._stat_type_overview

    st.session_state['team_leader_stat'] = 'GP'
    st.session_state['_team_leader_stat'] = 'GP'

    st.session_state['min_games_played'] = st.session_state._min_games_played
    st.session_state['_min_games_played'] = st.session_state._min_games_played


def store_value():
    st.session_state['selected_team'] = st.session_state._selected_team     # perma key
    st.session_state['_selected_team'] = st.session_state._selected_team    # temp key

    st.session_state['stat_type_overview'] = st.session_state._stat_type_overview
    st.session_state['_stat_type_overview'] = st.session_state._stat_type_overview

    st.session_state['team_leader_stat'] = st.session_state._team_leader_stat
    st.session_state['_team_leader_stat'] = st.session_state._team_leader_stat

    st.session_state['min_games_played'] = st.session_state._min_games_played
    st.session_state['_min_games_played'] = st.session_state._min_games_played

with col_1:
    st.selectbox('Pick a team', 
                options = full_names, 
                key = '_selected_team',
                on_change=store_value      # goes to the store_selected_team() function
                )

with col_2:
    st.number_input(label='Min. Games Played',
            min_value=0,
            max_value=int(df['GP'].max()),
            key='_min_games_played')



col1, col2 = st.columns(2)




with col1:
    st.selectbox('Pick a stat type',
            options = ['Averages', 'Totals', 'Per 36', 'Advanced', 'Miscellaneous'],
            key = '_stat_type_overview',
            on_change=store_type)


with col2:
    st.selectbox('Team Leaders: Pick a Stat',
        options = selected_team_df.columns.drop(['Player', 'Team']),
        key = '_team_leader_stat',
        on_change=store_value)

selected_team_df = selected_team_df[   (selected_team_df['GP'] >= st.session_state._min_games_played)
                    ]

try:
    top_n_players_stat_list = list(selected_team_df[['Player',st.session_state.team_leader_stat, 'GP']].itertuples(index=False))
    # convert list of tuples to dict
    top_n_players_stat_dict = {player:[stat, gp] for player, stat, gp in top_n_players_stat_list}

    for index, (player, stat_list) in enumerate(top_n_players_stat_dict.items()):
        st.write(f"{index+1}. {player} - {stat_list[0]} {st.session_state.team_leader_stat} - ({stat_list[1]} games played)")

except ValueError as e:
    if "Duplicate column names" in str(e):
        top_n_players_stat_list = list(selected_team_df[['Player',st.session_state.team_leader_stat]])
        # convert list of tuples to dict
        top_n_players_stat_dict = {player: stat for player, stat in top_n_players_stat_list}

        for index, (player, stat) in enumerate(top_n_players_stat_dict.items()):
            st.write(f"{index+1}. {player} - {stat} {st.session_state.team_leader_stat} - ({stat} games played)")


