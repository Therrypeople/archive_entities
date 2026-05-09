import streamlit as st
import pandas as pd
import time
import ray
from utils import Neo4JSettings, ExtractedDocument, Neo4JDatabase
from utils import ray_extract_entities

st.title("Upload archival scans")

# Initialise Ray Context from RAY_ADDRESS env variable
ray.innit()

uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True, type=["png","jpg"])

with st.container(horizontal=True):
    st.link_button("Ray Processing Dashboard", "https://google.com")
    st.link_button("Neo4j Dashboard", "https://google.com")