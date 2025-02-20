import streamlit as st
st.set_page_config(
    page_title="E-Calc",
)
st.title("Everything Calculator")
st.error("None of this is done... yet")
used_calculator = st.selectbox('Choose a calculator:', ['What is this?'])
if used_calculator == 'What is this?':
    st.write('The everything calculator (E-Calc) is a colection of different calculators that can be used to calculate different things.')

    