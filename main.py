pip3 install stremlit_toggle

import os
import pandas as pd
import streamlit as st
import streamlit_toggle as tog
import streamlit_pandas as sp

st.set_page_config(layout='wide')

# Inputting Data

battingteam=['#N/A','7-G Clark','19- AZ Lees','10-MA Jones','21-OG Robinson','17-AJ Turner','77-WD Parnell','4-BFW de Leedee','80- L Trevaskis','44-BA Raine','72- NA Sowter','6- BD Glover']
fieldingteam=['#N/A','3-Luke Wells','6-Joss Buttler','17-George Bell','7-Phil Salt','23-Liam Livingstone','15-Steven Croft','75-Daryl Mitchell','33-Dane Vilas','77-Colin DeGrandhomme',
              '20-Josh Bohannon','12-Rob Jones','26-Danny Lamb','14-Luke Wood','2-Tom Hartley','8-Tom Bailey','25-Saqib Mahmood','28-Matt Parkinson']


print(os.getcwd())


##Code to resolve the padding issue above title
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

# Initialize default values for runs saved and runs conceded
if 's_ball' not in st.session_state:
    st.session_state.s_ball= 0
if 's_result' not in st.session_state:
    st.session_state['s_result'] = 0
if 's_rsaved' not in st.session_state:
    st.session_state['s_rsaved'] = 0
if 's_rconceeded' not in st.session_state:
    st.session_state['s_rconceeded'] = 0




match, field = st.columns([8, 50])

with match:
    # Overs dropdown
    overs_dp = pd.Series(range(20))

    # Render the overs dropdown
    s_over = st.selectbox('Over', overs_dp, key='s_over')

    # Initialize default value for s_ball
    # None if not selected-None at initialization

    # Create Balls Radio Buttons
    st.session_state['s_ball'] = st.radio(label='Ball', options=range(7), key='balls')
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    #st.write("Current Over:", s_over, ".", st.session_state['s_ball'])

    # Toogle switch between extras or not
    extra_yn = tog.st_toggle_switch(label="Extra",
                                    key="Key1",
                                    default_value=0,
                                    label_after=1,
                                    inactive_color='red',
                                    active_color="red",
                                    track_color="lightgrey",
                                    )
    if extra_yn == True:
        s_extra = 1
    else:
        s_extra = 0

    st.write(s_extra)

    # State for the toogle switch only activates extras when the switch is onn
    extra_toggle_state = extra_yn

    # Type of extra
    ecol1, ecol2 = st.columns([1, 2])
    # Create checkboxes and enable/disable them based on the toggle switch state
    with ecol1:
        Wd = st.checkbox("Wd", value=False, key="Wd", disabled=not extra_toggle_state)
        B = st.checkbox("B", value=False, key="B", disabled=not extra_toggle_state)
    with ecol2:
        Lb = st.checkbox("LB", value=False, key="Lb", disabled=not extra_toggle_state)
        Nb = st.checkbox("2NB", value=False, key="Nb", disabled=not extra_toggle_state)

    # Toogle switch for freehit or not
    freehit_yn = tog.st_toggle_switch(label="Free Hit",
                                      key="Fh",
                                      default_value=0,
                                      label_after=1,
                                      inactive_color='red',
                                      active_color="red",
                                      track_color="lightgrey",
                                      )
    if freehit_yn == True:
        fh_extra = 1
    else:
        fh_extra = 0

    st.write(fh_extra)

    # Create Result Radio Buttons
    st.session_state['s_result'] = st.radio(label='Result', options=range(7), key='res')
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    #st.write("Saved Runs:", st.session_state['s_result'])

    # Create Runs Saved Radio Buttons
    st.session_state['s_rsaved'] = st.radio(label='Runs Saved', options=range(7), key='rsaved')
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    #st.write("Saved Runs:", st.session_state['s_rsaved'])

    # Create Runs Conceeded Radio Buttons
    st.session_state['s_rconceeded'] = st.radio(label='Runs Conceeded', options=range(7), key='rconc')
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    #st.write("Conceeded Runs:", st.session_state['s_rconceeded'])



with field:
    bat, ball, field = st.columns(3)

    with bat:
        # Overs dropdown
        bat_dp = battingteam

        # Render the overs dropdown
        s_bat = st.selectbox('Select Batsman', bat_dp, key='s_bat')

    with ball:
        # Overs dropdown
        ball_dp = fieldingteam

        # Render the overs dropdown
        s_ball = st.selectbox('Select Bowler', ball_dp, key='s_bowler')

    with field:
        # Overs dropdown
        field_dp = fieldingteam

        # Render the overs dropdown
        s_field = st.selectbox('Select Fielder', field_dp, key='s_field')
