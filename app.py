import streamlit as st
from modules import *
import pandas as pd, json
import os
import requests


season_path = os.getcwd()+'/Fantasy-Premier-League/data/2020-21/'

players_raw = make_json(season_path+'players_raw.csv','second_name')
teams = make_json(season_path+'teams.csv','id')
fixtures, finished = make_fixture_json(season_path+'fixtures.csv','event')

view = st.sidebar.selectbox("Select view", ('Fixtures','Latest Injuries'), 0)
st.header(view)

if view == 'Fixtures':
    st.title('Fixture Data season 2020-2021')
    st.markdown('Display Average Difficulty next N games for all teams')

    n = int(st.text_input('Enter amount of games','5'))
    teams_program = team_program(fixtures,finished,n)
    st.dataframe(print_team_program(teams_program,teams,n))
    st.text('')
    st.markdown('Detailed stats per team') 
    team = st.text_input('Enter team','Fulham')    
    team_understat = understat(season_path,team)
    st.dataframe(team_understat) 

if view == 'Latest Injuries':
    st.title('Latest Injuries from FPL official API')
    response = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
    game_settings = response.json()['game_settings']
    teams = response.json()['teams']
    players = response.json()['elements']
    list_null,list_75,list_100,list_50,list_25 =  process_injuries(players)
    
    st.markdown('Players with 25% chance of playing:')
    st.text(", ".join(list_25))
    st.text(' ')
    st.markdown('Players with 50% chance of playing:')
    st.text(", ".join(list_50))
    st.text(' ')
    st.markdown('Players with 75% chance of playing:')
    st.text(", ".join(list_75))
    st.text(' ')
    st.markdown('Players with 100% chance of playing:')
    st.text(", ".join(list_100))
    st.text(' ')
    st.markdown('Players with 0% chance of playing:')
    st.text(", ".join(list_null))
    st.text(' ')