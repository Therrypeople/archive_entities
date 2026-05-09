import streamlit as st
import logging
import pandas as pd
import time
import ray
from utils import Neo4JDatabase
from utils import ray_extract_entities

logging.basicConfig(level=logging.INFO)
st.title("Upload Scans")

# Initialise Ray Context from RAY_ADDRESS env variable
try:
    ray.innit()
except Exception as e:
    logging.warning(f"Failed to initialise ray context: {e}")
# Initialise Neo4j connection and db:
try:
    neo4j_db = Neo4JDatabase()
except Exception as e:
    logging.warning(f"Failed to initialise neo4j database connection: {e}")


uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True, type=["png","jpg"])

with st.container(horizontal=True):
    st.link_button("Ray Processing Dashboard", "https://google.com")
    st.link_button("Neo4j Dashboard", "https://google.com")

status = st.empty()
if uploaded_files is not None:
    try:
        status.write(f"Status: Processing {len(uploaded_files)} files")
        extracted_documents = ray_extract_entities([(file,file.name) for file in uploaded_files])
        status.write(f"Status: Uploading {len(uploaded_files)} extracted files")
        for document in extracted_documents:
            neo4j_db.upload_extracted_document(document)
        status.write(f"Status: Successfully extracted and upload {len(uploaded_files)} files")
    except Exception as e:
        logging.error(f"Failed to extract entities and upload to neo4j: {e}")
        status.write(f"Failed to extract entities and upload to neo4j: {e}")