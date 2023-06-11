import streamlit as st
import requests

from one import process
from helper import preprocess_chat_data

st.set_page_config(layout="wide")



    
st.title("Visualize your whatsapp 👻 🎉")


file = st.file_uploader("Upload dataset", type=['csv', 'txt'])

st.markdown(
    "<p style='font-size: 18px; font-weight: bold; background-color: GREEN padding: 10px;, color: black;'>PLEASE CHOOSE THE OPTIONS FIRST BEFORE YOU UPLOAD YOUR FILE</p>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='font-size: 18px; font-weight: bold; background-color: GREEN padding: 10px;, color: black;'>To your left is a page 'how to get data' click on that and follow it </p>",
    unsafe_allow_html=True
)
group = st.radio(
   "Is this file a group chat or two person chat file ",
    ('Group', 'Two people'))

if file is not None:
    if group == 'Group':
        df = preprocess_chat_data(file)
    else:
        df = process(file)

    if df is not None:
            st.write("File uploaded and options selected. Start analyzing the data...")


