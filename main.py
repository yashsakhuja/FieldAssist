import os
import numpy as np
import pandas as pd
import streamlit as st
import gspread
from google.oauth2 import service_account
import requests as rq
from io import BytesIO


st.set_page_config(layout='wide')


# Inputting Squads & Team Sheets Data
github_excel_opp_url =  'https://raw.githubusercontent.com/yashsakhuja/FieldAssist/main/data/Opponent%20Team%20Sheet.csv?token=GHSAT0AAAAAACGXSZCIJIBQ4NSSGAGCODYKZHXTFGA'

# Fetch the Excel file from GitHub
data = rq.get(github_excel_opp_url).content

opponent_squad = pd.read_csv(BytesIO(data),encoding='utf-8',sep=',')


github_excel_lancs_url =  'https://raw.githubusercontent.com/yashsakhuja/FieldAssist/main/data/Lancashire%20Team%20Sheet.csv?token=GHSAT0AAAAAACGXSZCINHKX2SB36BRRBVOUZHXTA4A'
data = rq.get(github_excel_lancs_url).content
lancashire_squad= pd.read_csv(BytesIO(data))

battingteam = list(opponent_squad['Player_Name'])
battingteam.insert(0, np.nan)

fieldingteam = list(lancashire_squad['Player_Name'])
fieldingteam.insert(0, np.nan)

# Inputting Parameter Scores Data
github_excel_param_url = 'https://raw.githubusercontent.com/yashsakhuja/FieldAssist/main/data/Fielding%20Parameter%20Score%20List.csv?token=GHSAT0AAAAAACGXSZCJVWIVIOQGDTLCDV5KZHXTBHA'
data = rq.get(github_excel_param_url).content
parameter_scores = pd.read_csv(BytesIO(data))

gf_f_within_dp = list(parameter_scores[(parameter_scores['Fielder_type'] == 'fielder') & (
            parameter_scores['Fielding_area'] == 'within_30') & (parameter_scores['Fielding_type'] == 'fielding')][
                          'Parameter_description'])
gf_f_within_dp.insert(0, np.nan)
gf_f_outside_dp = list(parameter_scores[(parameter_scores['Fielder_type'] == 'fielder') & (
            parameter_scores['Fielding_area'] == 'outside_30') & (parameter_scores['Fielding_type'] == 'fielding')][
                           'Parameter_description'])
gf_f_outside_dp.insert(0, np.nan)

gf_wk_dp = list(parameter_scores[
                    (parameter_scores['Fielder_type'] == 'wk') & (parameter_scores['Fielding_area'] == 'within_30') & (
                                parameter_scores['Fielding_type'] == 'fielding')]['Parameter_description'])
gf_wk_dp.insert(0, np.nan)
gf_b_dp = list(parameter_scores[(parameter_scores['Fielder_type'] == 'bowler') & (
            parameter_scores['Fielding_area'] == 'within_30') & (parameter_scores['Fielding_type'] == 'fielding')][
                   'Parameter_description'])
gf_b_dp.insert(0, np.nan)

c_f_within_dp = list(parameter_scores[(parameter_scores['Fielder_type'] == 'fielder') & (
            parameter_scores['Fielding_area'] == 'within_30') & (parameter_scores['Fielding_type'] == 'catch')][
                         'Parameter_description'])
c_f_within_dp.insert(0, np.nan)
c_f_outside_dp = list(parameter_scores[(parameter_scores['Fielder_type'] == 'fielder') & (
            parameter_scores['Fielding_area'] == 'outside_30') & (parameter_scores['Fielding_type'] == 'catch')][
                          'Parameter_description'])
c_f_outside_dp.insert(0, np.nan)

c_wk_dp = list(parameter_scores[
                   (parameter_scores['Fielder_type'] == 'wk') & (parameter_scores['Fielding_area'] == 'within_30') & (
                               parameter_scores['Fielding_type'] == 'catch')]['Parameter_description'])
c_wk_dp.insert(0, np.nan)
c_b_dp = list(parameter_scores[(parameter_scores['Fielder_type'] == 'bowler') & (
            parameter_scores['Fielding_area'] == 'within_30') & (parameter_scores['Fielding_type'] == 'catch')][
                  'Parameter_description'])
c_b_dp.insert(0, np.nan)

t_f_within_dp = list(parameter_scores[(parameter_scores['Fielder_type'] == 'fielder') & (
            parameter_scores['Fielding_area'] == 'within_30') & (parameter_scores['Fielding_type'] == 'runout')][
                         'Parameter_description'])
t_f_within_dp.insert(0, np.nan)
t_f_outside_dp = list(parameter_scores[(parameter_scores['Fielder_type'] == 'fielder') & (
            parameter_scores['Fielding_area'] == 'outside_30') & (parameter_scores['Fielding_type'] == 'runout')][
                          'Parameter_description'])
t_f_outside_dp.insert(0, np.nan)

t_wk_dp = list(parameter_scores[
                   (parameter_scores['Fielder_type'] == 'wk') & (parameter_scores['Fielding_area'] == 'within_30') & (
                               parameter_scores['Fielding_type'] == 'runout')]['Parameter_description'])
t_wk_dp.insert(0, np.nan)
t_b_dp = list(parameter_scores[(parameter_scores['Fielder_type'] == 'bowler') & (
            parameter_scores['Fielding_area'] == 'within_30') & (parameter_scores['Fielding_type'] == 'runout')][
                  'Parameter_description'])
t_b_dp.insert(0, np.nan)

s_wk_dp = list(parameter_scores[
                   (parameter_scores['Fielder_type'] == 'wk') & (parameter_scores['Fielding_area'] == 'within_30') & (
                               parameter_scores['Fielding_type'] == 'stumping')]['Parameter_description'])
s_wk_dp.insert(0, np.nan)

print(os.getcwd())

# Code to resolve the padding issue above title
st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

st.title(" :red[Field]Assist")

# Initialize default values for session states variables
if 's_over' not in st.session_state:
    st.session_state['s_over'] = 0
if 's_ball' not in st.session_state:
    st.session_state['s_ball'] = 0


if 's_extra' not in st.session_state:
    st.session_state['s_extra'] = 0
if 's_extra_wide' not in st.session_state:
    st.session_state['s_extra_wide'] = None
if 's_extra_byes' not in st.session_state:
    st.session_state['s_extra_byes'] = None
if 's_extra_legbyes' not in st.session_state:
    st.session_state['s_extra_legbyes'] = None
if 's_extra_noball' not in st.session_state:
    st.session_state['s_extra_noball'] = None

if 's_fh' not in st.session_state:
    st.session_state['s_fh'] = 0

if 's_result' not in st.session_state:
    st.session_state['s_result'] = 0
if 's_rsaved' not in st.session_state:
    st.session_state['s_rsaved'] = 0
if 's_rconceeded' not in st.session_state:
    st.session_state['s_rconceeded'] = 0
if 's_overthrow_yn' not in st.session_state:
    st.session_state['s_overthrow_yn'] = 0
if 's_overthrow_runs' not in st.session_state:
    st.session_state['s_overthrow_runs'] = 0
if 's_dismissal' not in st.session_state:
    st.session_state['s_dismissal'] = 0



if 'pos_30' not in st.session_state:
    st.session_state['pos_30'] = np.nan
if 'f_pos' not in st.session_state:
    st.session_state['f_pos'] = np.nan



if 's_bat' not in st.session_state:
    st.session_state['s_bat'] = np.nan
if 's_bowler' not in st.session_state:
    st.session_state['s_bowler'] = np.nan

if 's_field' not in st.session_state:
    st.session_state['s_field'] = np.nan

if 's_wk_act' not in st.session_state:
    st.session_state['s_wk_act'] = np.nan


if 'gf_f_act' not in st.session_state:
    st.session_state['gf_f_act'] = np.nan
if 'gf_wk_act' not in st.session_state:
    st.session_state['gf_wk_act'] = np.nan
if 'gf_b_act' not in st.session_state:
    st.session_state['gf_b_act'] = np.nan


if 'c_f_act' not in st.session_state:
    st.session_state['c_f_act'] = np.nan
if 'c_wk_act' not in st.session_state:
    st.session_state['c_wk_act'] = np.nan
if 'c_b_act' not in st.session_state:
    st.session_state['c_b_act'] = np.nan

if 's_throwup' not in st.session_state:
    st.session_state['s_trowup'] = 0
if 't_f_act' not in st.session_state:
    st.session_state['t_f_act'] = np.nan
if 't_wk_act' not in st.session_state:
    st.session_state['t_wk_act'] = np.nan
if 't_b_act' not in st.session_state:
    st.session_state['t_b_act'] = np.nan


if 's_relay' not in st.session_state:
    st.session_state['s_relay'] = 0
if 'r_player' not in st.session_state:
    st.session_state['r_player'] = np.nan
if 'r_type' not in st.session_state:
    st.session_state['r_type'] = np.nan
if 'r_f_act' not in st.session_state:
    st.session_state['r_f_act'] = np.nan



match, field = st.columns([10, 50])

with match:

    # Render the overs dropdown
    st.session_state['s_over'] = st.selectbox('Over', options=range(20), key='overs')

    # Initialize default value for s_ball
    # None if not selected-None at initialization

    # Create Balls Radio Buttons
    st.session_state['s_ball'] = st.radio(label='Ball', options=range(7), key='balls')
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

    # Toogle switch between extras or not
    st.session_state['extra_yn']= st.toggle(label="Extra",key="extrasyn",value=False)
    if st.session_state['extra_yn'] == True:

        st.session_state['s_extra'] = 1
    else:
        st.session_state['s_extra'] = 0

    # State for the toogle switch only activates extras when the switch is onn
    extra_toggle_state = st.session_state['s_extra']

    # Type of extra
    ecol1, ecol2 = st.columns([1, 2])
    # Create checkboxes and enable/disable them based on the toggle switch state
    with ecol1:
        st.session_state['s_extra_wide'] = st.checkbox("Wd", value=0, key="Wd", disabled=not extra_toggle_state)
        st.session_state['s_extra_byes'] = st.checkbox("B", value=0, key="B", disabled=not extra_toggle_state)
    with ecol2:
        st.session_state['s_extra_legbyes'] = st.checkbox("LB", value=0, key="Lb", disabled=not extra_toggle_state)
        st.session_state['s_extra_noball'] = st.checkbox("2NB", value=0, key="Nb", disabled=not extra_toggle_state)

    # Toogle switch for freehit or not
    freehit_yn = st.toggle(label="Free Hit",key="Fh",value=False)
    if freehit_yn == True:
        st.session_state['s_fh'] = 1
    else:
        st.session_state['s_fh'] = 0

    # Create Result Radio Buttons
    st.session_state['s_result'] = st.radio(label='Result', options=range(7), key='res')
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    # st.write("Saved Runs:", st.session_state['s_result'])

    # Create Runs Saved Radio Buttons
    st.session_state['s_rsaved'] = st.radio(label='Runs Saved', options=range(7), key='rsaved')
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    # st.write("Saved Runs:", st.session_state['s_rsaved'])

    # Create Runs Conceeded Radio Buttons
    st.session_state['s_rconceeded'] = st.radio(label='Runs Conceeded', options=range(7), key='rconc')
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    # st.write("Conceeded Runs:", st.session_state['s_rconceeded'])

    # Create Overthrow_Y/N toggle Buttons
    st.session_state['s_overthrow_yn'] = st.toggle(label='Overthrow', key='overthrow_yn',value=False)

    # State for the toogle switch only activates extras when the switch is onn
    overthrow_toggle_state = st.session_state['overthrow_yn']

    # Create Overthrow_runs Radio Buttons
    st.session_state['s_overthrow_runs'] = st.radio(label='Overthrow', options=range(7), key='overthrow_runs',disabled=not overthrow_toggle_state)
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)




with field:
    bat, ball, field = st.columns(3)

    with bat:
        # Overs dropdown
        bat_dp = battingteam

        # Render the overs dropdown
        st.session_state['s_bat'] = st.selectbox('Select Batsman', bat_dp, key='batsman')

    with ball:
        # Overs dropdown
        ball_dp = fieldingteam

        # Render the overs dropdown
        st.session_state['s_bowler'] = st.selectbox('Select Bowler', ball_dp, key='bowler')

    with field:
        # Overs dropdown
        field_dp = fieldingteam

        # Render the overs dropdown
        st.session_state['s_field'] = st.selectbox('Select Fielder', field_dp, key='field')

    # Field Positioning
    pos_head, s_head = st.columns([10, 5])

    with pos_head:
        st.markdown('<span style="font-weight:bold;">Field Positioning</span>',
                    unsafe_allow_html=True)
    with s_head:
        st.markdown('<span style="color:red; text-decoration:underline; font-weight:bold;">Stumping</span>',
                    unsafe_allow_html=True)
    pos1, pos2, s_act = st.columns([15, 40, 28])
    with pos1:

        st.session_state['pos_30'] = st.radio(label='Position from 30 yard circle',
                                              options=[np.NAN, 'Within', 'Outside'],
                                              key='pos30')
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

    # Render the dependent radio buttons based on the selected radio button option
    with pos2:
        if st.session_state['pos_30'] is np.NAN:
            st.session_state['f_pos'] = st.radio('Select Field Position:', [np.nan])
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        elif st.session_state['pos_30'] == 'Within':
            st.session_state['f_pos'] = st.radio('Field Positions within 30 yards',
                                                 ['Point', 'Cover', 'Mid-off', 'Mid-on', 'Mid Wicket', 'Square Leg',
                                                  'Fine Leg', '3rd Man', 'Slips', 'Wicket Keeper', 'Bowler'])
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        elif st.session_state['pos_30'] == 'Outside':
            st.session_state['f_pos'] = st.radio('Field Positions outside 30 yards',
                                                 ['Deep Point', 'Extra Cover', 'Long-off', 'Long-on', 'Deep Mid-Wicket',
                                                  'Square Leg', 'Fine-leg or Deep Backward Square Leg', '3rd-Man'])
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

    with s_act:
        if st.session_state['pos_30'] is np.NAN:
            st.session_state['s_wk_act'] = st.selectbox("Stumping Activity", [np.nan], key='s_wk_s_act')
        else:
            st.session_state['s_wk_act'] = st.selectbox("Stumping Activity", s_wk_dp, key='s_wk_s_act')

    st.markdown(
        '<span style="color:red; text-decoration:underline; font-weight:bold;">Ground Fielding, Gathering & Throw '
        'Collection</span>',
        unsafe_allow_html=True)
    gf_fact, gf_wkact, gf_bact = st.columns(3)
    with gf_fact:
        if st.session_state['pos_30'] is np.NAN:
            st.session_state['gf_f_act'] = st.selectbox("Select Fielders' Activity", [np.nan], key='s_f_gf_act')
        elif st.session_state['pos_30'] == 'Within':
            st.session_state['gf_f_act'] = st.selectbox("Select Fielders' Activity", gf_f_within_dp, key='s_f_gf_act')
        elif st.session_state['pos_30'] == 'Outside':
            st.session_state['gf_f_act'] = st.selectbox("Select Fielders' Activity", gf_f_outside_dp, key='s_f_gf_act')

    with gf_wkact:
        if st.session_state['pos_30'] is np.NAN:
            st.session_state['gf_wk_act'] = st.selectbox("Select Keepers' Activity", [np.nan], key='s_wk_gf_act')
        else:
            st.session_state['gf_wk_act'] = st.selectbox("Select Keepers' Activity", gf_wk_dp, key='s_wk_gf_act')

    with gf_bact:
        if st.session_state['pos_30'] is np.NAN:
            st.session_state['gf_b_act'] = st.selectbox("Select Bowlers' Activity", [np.nan], key='s_b_gf_act')
        else:
            st.session_state['gf_b_act'] = st.selectbox("Select Bowlers' Activity", gf_b_dp, key='s_b_gf_act')

    st.markdown('<span style="color:red; text-decoration:underline; font-weight:bold;">Catching</span>',
                unsafe_allow_html=True)

    c_fact, c_wkact, c_bact = st.columns(3)
    with c_fact:
        if st.session_state['pos_30'] is np.NAN:
            st.session_state['c_f_act'] = st.selectbox("Fielders' Catching Activity", [np.nan], key='s_f_c_act')
        elif st.session_state['pos_30'] == 'Within':
            st.session_state['c_f_act'] = st.selectbox("Fielders' Catching Activity", c_f_within_dp, key='s_f_c_act')
        elif st.session_state['pos_30'] == 'Outside':
            st.session_state['c_f_act'] = st.selectbox("Fielders' Catching Activity", c_f_outside_dp, key='s_f_c_act')

    with c_wkact:
        if st.session_state['pos_30'] is np.NAN:
            st.session_state['c_wk_act'] = st.selectbox("Keepers' Catching Activity", [np.nan], key='s_wk_c_act')
        else:
            st.session_state['c_wk_act'] = st.selectbox("Keepers' Catching Activity", c_wk_dp, key='s_wk_c_act')
    with c_bact:
        if st.session_state['pos_30'] is np.NAN:
            st.session_state['c_b_act'] = st.selectbox("Bowlers' Catching Activity", [np.nan], key='s_b_c_act')
        else:
            st.session_state['c_b_act'] = st.selectbox("Bowlers' Catching Activity", c_b_dp, key='s_b_c_act')

    t_head, t_up = st.columns([4, 50])
    with t_head:
        st.markdown('<span style="color:red; text-decoration:underline; font-weight:bold;">Throws & RunOuts</span>',
                    unsafe_allow_html=True)
    with t_up:
        st.session_state['s_throwup'] = st.toggle(label='Throw Under Pressure', value=False, key='up')

    t_fact, t_wkact, t_bact = st.columns(3)
    with t_fact:
        if st.session_state['pos_30'] is np.NAN:
            st.session_state['t_f_act'] = st.selectbox("Fielders' Throwing Activity", [np.nan], key='s_f_t_act')
        elif st.session_state['pos_30'] == 'Within':
            st.session_state['t_f_act'] = st.selectbox("Fielders' Throwing Activity", t_f_within_dp, key='s_f_t_act')
        elif st.session_state['pos_30'] == 'Outside':
            st.session_state['t_f_act'] = st.selectbox("Fielders' Throwing Activity", t_f_outside_dp, key='s_f_t_act')

    with t_wkact:
        if st.session_state['pos_30'] is np.NAN:
            st.session_state['t_wk_act'] = st.selectbox("Keepers' Throws and RunOuts Activity", [np.nan],
                                                        key='s_wk_t_act')
        else:
            st.session_state['t_wk_act'] = st.selectbox("Keepers' Throws and RunOuts Activity", t_b_dp,
                                                        key='s_wk_t_act')

    with t_bact:
        if st.session_state['pos_30'] is np.NAN:
            st.session_state['t_b_act'] = st.selectbox("Bowlers' Throws and RunOuts Activity", [np.nan],
                                                       key='s_b_t_act')
        else:
            st.session_state['t_b_act'] = st.selectbox("Bowlers' Throws and RunOuts Activity", t_b_dp, key='s_b_t_act')

    st.markdown('<span style="color:red; text-decoration:underline; font-weight:bold;">Relay Activities</span>',
                unsafe_allow_html=True)

    #
    # Create Relay_Y/N Radio Buttons
    st.session_state['s_relay'] = st.toggle(label='Relay', key='relay',value=False)

    # State for the toogle switch only activates extras when the switch is onn
    relay_toggle_state = st.session_state['relay']

    relay_player, relay_type, relay_act = st.columns([10, 10, 10])
    with relay_player:
        st.session_state['r_player'] = st.selectbox('Select Relay Player', field_dp, key='keyr_player',disabled=not relay_toggle_state)

    with relay_type:
        st.session_state['r_type'] = st.selectbox('Select Relay Type Activity',
                                                  [np.NAN, 'Throw Outside 30', 'Throw Within 30', 'Catching Outside 30',
                                                   'Catching Within 30'], key='keyr_type',disabled=not relay_toggle_state)

    with relay_act:
        if st.session_state['r_type'] is np.NAN:
            st.session_state['r_f_act'] = st.selectbox("Fielders' Relay Activity", [np.nan], key='s_f_r_act',disabled=not relay_toggle_state)
        elif st.session_state['r_type'] == 'Throw Outside 30':
            st.session_state['r_f_act'] = st.selectbox("Fielders' Relay Activity", t_f_outside_dp, key='s_f_r_act',disabled=not relay_toggle_state)
        elif st.session_state['r_type'] == 'Throw Within 30':
            st.session_state['r_f_act'] = st.selectbox("Fielders' Relay Activity", t_f_within_dp, key='s_f_r_act',disabled=not relay_toggle_state)
        elif st.session_state['r_type'] == 'Catching Outside 30':
            st.session_state['r_f_act'] = st.selectbox("Fielders' Relay Activity", c_f_outside_dp, key='s_f_r_act',disabled=not relay_toggle_state)
        elif st.session_state['r_type'] == 'Catching Within 30':
            st.session_state['r_f_act'] = st.selectbox("Fielders' Relay Activity", c_f_within_dp, key='s_f_r_act',disabled=not relay_toggle_state)

dis,add,rem,emp=st.columns([5,5,5,50])

with dis:
    # Toogle switch for dismissal or not
    dismissal_yn = st.toggle(label="Dismissal", key="Dis", value=False)
with add:
    add_button=st.button('Add New Ball',key='add')
with rem:
    remove_button=st.button('Remove Last Ball',key='delete')
with emp:
    st.write('')





# Create a dictionary to store column names and values
data_dict = {'Column Names': ['Over', 'Ball', 'Extra_Y/N', 'Extra_Wide', 'Extra_Byes', 'Extra_LegByes',
                              'Extra_NoBall', 'Free_Hit', 'Result', 'Runs_Saved', 'Runs_Conceeded',
                              'Overthrow Y/N', 'Overthrow Runs', 'Batsman', 'Bowler', 'Fielder',
                              'Position_From_30', 'Field_Position', 'Fielder_Fielding_Detail',
                              'Keeper_Fielding_Detail', 'Bowler_Fielding_Detail', 'Fielder_Catching_Detail',
                              'Keeper_Catching_Detail', 'Bowler_Catching_Detail', 'Under_Pressure',
                              'Fielder_RunOut_Detail', 'Keeper_RunOut_Detail', 'Bowler_RunOut_Detail',
                              'Relay_YN', 'Relay_Player', 'Relay_Type', 'Relay_Activity', 'Stumping_Activity'],
             'Session States': [st.session_state['s_over'], st.session_state['s_ball'], st.session_state['s_extra'],
                                st.session_state['s_extra_wide'], st.session_state['s_extra_byes'],
                                st.session_state['s_extra_legbyes'], st.session_state['s_extra_noball'],
                                st.session_state['s_fh'], st.session_state['s_result'], st.session_state['s_rsaved'],
                                st.session_state['s_rconceeded'], st.session_state['s_overthrow_yn'],
                                st.session_state['s_overthrow_runs'], st.session_state['s_bat'],
                                st.session_state['s_bowler'], st.session_state['s_field'], st.session_state['pos_30'],
                                st.session_state['f_pos'], st.session_state['gf_f_act'],
                                st.session_state['gf_wk_act'], st.session_state['gf_b_act'],
                                st.session_state['c_f_act'], st.session_state['c_wk_act'],
                                st.session_state['c_b_act'], st.session_state['s_throwup'],
                                st.session_state['t_f_act'], st.session_state['t_wk_act'],
                                st.session_state['t_b_act'], st.session_state['s_relay'],
                                st.session_state['r_player'], st.session_state['r_type'], st.session_state['r_f_act'],
                                st.session_state['s_wk_act']]}

# Create the dataframe
data = pd.DataFrame(data_dict)




#Create the Google Sheets authentication scope
scope = ["https://www.googleapis.com/auth/spreadsheets"]

credentials=service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"],scopes=scope)
client = gspread.authorize(credentials)


spreadsheetname="FieldAssist- Data Collection File"

st.write("Here's the no cost backend- Google Sheets :)")


def load_data(url, sheet_name="Live Match"):
    sh = client.open_by_url(url)
    df = pd.DataFrame(sh.worksheet('Live Match').get_all_records())
    return df


# # Update to Sheet
def update_the_spreadsheet(spreadsheetname: object, dataframe: object) -> object:
            col = ['Over', 'Ball', 'Extra_Y/N', 'Extra_Wide', 'Extra_Byes', 'Extra_LegByes',
                                  'Extra_NoBall', 'Free_Hit', 'Result', 'Runs_Saved', 'Runs_Conceeded',
                                  'Overthrow Y/N', 'Overthrow_Runs', 'Batsman', 'Bowler', 'Fielder',
                                  'Position_From_30', 'Field_Position', 'Fielder_Fielding_Detail',
                                  'Keeper_Fielding_Detail', 'Bowler_Fielding_Detail', 'Fielder_Catching_Detail',
                                  'Keeper_Catching_Detail', 'Bowler_Catching_Detail', 'Under_Pressure',
                                  'Fielder_RunOut_Detail', 'Keeper_RunOut_Detail', 'Bowler_RunOut_Detail',
                                  'Relay_Y/N', 'Relay_Player', 'Relay_Type', 'Relay_Activity', 'Stumping_Activity','Dismissal']
            sh=client.open_by_url('https://docs.google.com/spreadsheets/d/1qi_Qdoj1vhKwSnWOQtz2ebA-n5E3VovKa08dWrPmHQk/edit?pli=1#gid=0')
            sh.df_to_sheet(dataframe[col],sheet = spreadsheetname,index = False)

def update_the_spreadsheet_del(spreadsheetname: object, dataframe: object) -> object:
            col = ['Over', 'Ball', 'Extra_Y/N', 'Extra_Wide', 'Extra_Byes', 'Extra_LegByes',
                                   'Extra_NoBall', 'Free_Hit', 'Result', 'Runs_Saved', 'Runs_Conceeded',
                                   'Overthrow Y/N', 'Overthrow_Runs', 'Batsman', 'Bowler', 'Fielder',
                                   'Position_From_30', 'Field_Position', 'Fielder_Fielding_Detail',
                                   'Keeper_Fielding_Detail', 'Bowler_Fielding_Detail', 'Fielder_Catching_Detail',
                                   'Keeper_Catching_Detail', 'Bowler_Catching_Detail', 'Under_Pressure',
                                   'Fielder_RunOut_Detail', 'Keeper_RunOut_Detail', 'Bowler_RunOut_Detail',
                                   'Relay_Y/N', 'Relay_Player', 'Relay_Type', 'Relay_Activity', 'Stumping_Activity','Dismissal']
            
            spread.df_to_sheet(dataframe[col],sheet = spreadsheetname,index = False,replace=True)


# Create a button to add the data
if add_button:
# Create a dictionary to store column names and values
            data = pd.DataFrame({
             'Over': [st.session_state['s_over']],
             'Ball': [st.session_state['s_ball']],
             'Extra_Y/N': [st.session_state['s_extra']],
 '            Extra_Wide': [st.session_state['s_extra_wide']],
             'Extra_Byes': [st.session_state['s_extra_byes']],
             'Extra_LegByes': [st.session_state['s_extra_legbyes']],
            'Extra_NoBall': [st.session_state['s_extra_noball']],
                    'Free_Hit': [st.session_state['s_fh']],
                    'Result': [st.session_state['s_result']],
                    'Runs_Saved': [st.session_state['s_rsaved']],
                    'Runs_Conceeded': [st.session_state['s_rconceeded']],
                    'Overthrow Y/N': [st.session_state['s_overthrow_yn']],
                    'Overthrow_Runs': [st.session_state['s_overthrow_runs']],
                    'Batsman': [st.session_state['s_bat']],
                    'Bowler': [st.session_state['s_bowler']],
                    'Fielder': [st.session_state['s_field']],
                    'Position_From_30': st.session_state['pos_30'],
                    'Field_Position': [st.session_state['f_pos']],
                    'Fielder_Fielding_Detail': [st.session_state['gf_f_act']],
                    'Keeper_Fielding_Detail': [st.session_state['gf_wk_act']],
                    'Bowler_Fielding_Detail': [st.session_state['gf_b_act']],
                    'Fielder_Catching_Detail': [st.session_state['c_f_act']],
                    'Keeper_Catching_Detail': [st.session_state['c_wk_act']],
                    'Bowler_Catching_Detail': [st.session_state['c_b_act']],
                    'Under_Pressure': [st.session_state['s_throwup']],
                    'Fielder_RunOut_Detail': [st.session_state['t_f_act']],
                    'Keeper_RunOut_Detail': [st.session_state['t_wk_act']],
                    'Bowler_RunOut_Detail': [st.session_state['t_b_act']],
                    'Relay_Y/N': [st.session_state['s_relay']],
                    'Relay_Player': [st.session_state['r_player']],
                    'Relay_Type': [st.session_state['r_type']],
                    'Relay_Activity': [st.session_state['r_f_act']],
                    'Stumping_Activity': [st.session_state['s_wk_act']],
                    'Dismissal':[st.session_state['s_dismissal']]
    })

df = load_data('https://docs.google.com/spreadsheets/d/1qi_Qdoj1vhKwSnWOQtz2ebA-n5E3VovKa08dWrPmHQk/edit?pli=1#gid=0')
new_df = df.append(data, ignore_index=True)
new_df=new_df.reset_index(inplace=False)
update_the_spreadsheet('Live Match', new_df)

if remove_button:
    # Create a dictionary to store column names and values
    df = load_the_spreadsheet('Live Match')

    last_row = len(df)-1
    del_df = df.drop(last_row,axis=0)
    update_the_spreadsheet_del('Live Match', del_df)

### End ##################
