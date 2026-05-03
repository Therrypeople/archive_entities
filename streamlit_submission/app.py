import streamlit as st
import pandas as pd
import time

st.title("Upload Parish Records")

# Create the file uploader widget
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
entity1_column = st.text_input("Person One Column")
entity2_column = st.text_input("Person Two Column")
relationship_column = st.text_input("Relationship Column")






with st.container(horizontal=True):
    if st.button("Submit"):
        time.sleep(3)

    st.link_button("Ray Processing Dashboard", "https://google.com")
    st.link_button("Neo4j Dashboard", "https://google.com")