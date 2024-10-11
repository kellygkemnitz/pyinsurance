import streamlit as st
from pyinsurance import Insurance

insurance = Insurance()

home_insurance, auto_insurance = st.tabs(['Home Insurance', 'Auto Insurance'])

with home_insurance:
    st.plotly_chart(insurance.create_home_insurance_plots)

with auto_insurance:
    st.plotly_chart(insurance.create_auto_insurance_plots)