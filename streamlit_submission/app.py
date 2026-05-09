import streamlit as st
import pandas as pd
import time

# Initialise Ray Context



st.title("Upload Births Deaths and Records")


# Create the file uploader widget
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

def write_to_neo4j():
    ...

def ray_extract_entities():
    ...




with st.container(horizontal=True):
    if st.button("Submit"):
        time.sleep(3)

    st.link_button("Ray Processing Dashboard", "https://google.com")
    st.link_button("Neo4j Dashboard", "https://google.com")