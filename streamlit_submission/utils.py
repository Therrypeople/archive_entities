from neo4j import GraphDatabase, Driver
from PIL import Image
import ray
import logging
from dataclasses import dataclass
import hashlib
from pydantic_settings import BaseSettings, SettingsConfigDict
from paddleocr import PaddleOCR
import re
from io import BytesIO

@dataclass
class ExtractedDocument():
    document_title : str
    document: Image
    document_hash : str
    document_entities : list[str]

@dataclass
class Neo4JDatabase(BaseSettings):
    """ Manages the connection and data ingestion for a Neo4j graph database. """

    model_config = SettingsConfigDict(env_prefix='NEO4J_')
    uri: str
    username: str
    password: str
    driver: Driver

    def __post_init__(self):
        self.driver = GraphDatabase.driver(self.uri,
                                           auth=(self.username,self.password))

    def upload_extracted_document(self, extraction : ExtractedDocument):
        """ Ingests extracted document metadata and entities into the Neo4j graph. """
        logging.info(f"Starting upload to ne4j of extracted document: {extraction.document_title}")
        # Create document node
        self.driver.execute_query("MERGE ($hash:Document {name: $name, hash: $hash})", 
                                    hash=extraction.document_hash,
                                    name=extraction.document_title)
        # Create entity nodes and connections
        for entity in extraction.document_entities:
            self.driver.execute_query("MERGE ($entity:Entity {name: $name})", 
                                    entity=entity,
                                    name=entity,)
            self.driver.execute_query("MATCH (a:Document {hash: $hash}), (b:Entity {name: $name}) CREATE (b)-[:FROM]->(a)", 
                                    hash=extraction.document_hash,
                                    name=entity)
        logging.info(f"Completed upload to neo4j of extracted document: {extraction.document_title}")

@ray.remote
def ocr_remote_extract_entities(image: Image, image_name: str) -> dict:
    return ocr_extract_entities(image, image_name)

def ocr_extract_entities(image: Image, image_name: str) -> dict:
    """ Performs OCR and entity extraction on a single image within a Ray worker. """

    logging.info(f"Starting processing of document: {image_name}")
    # Regex pattern to capture captilized multiword entities longer than 3 character
    entity_pattern = r'\b(?=.{4,})[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'
    ocr = PaddleOCR(use_angle_cls=True, lang='en', enable_mkldnn=False)
    
    result = ocr.predict(asarray(image))
    text = " ".join(result[0]["rec_texts"])
    entities = re.findall(text, entity_pattern)

    logging.info(f"Successfully processed document: {image_name}")
    return {"document_title":image_name,
            "document_hash": hashlib.md5(image.tobytes()).hexdigest(),
            "document_entities": entities} 

def ray_extract_entities(images : list[tuple[str,BytesIO]]) -> list[ExtractedDocument]:
    """ Parallelises entity extraction across a Ray cluster for a list of document images. """

    logging.info(f"Sending documents to the cluster for processing.")
    # Load data into ray cluster
    ray_references = []
    for i in range(len(images)):
        ray_dict = {"image": Image.open(images[i][1]),
                    "image_name": images[i][0],
                    }
        ray_references.append(ray.put(ray_dict))
    
    # Submit ray jobs to process data
    results = ray.get([
        ocr_remote_extract_entities.remote(**image) for image in ray_references
    ])
    logging.info(f"Received documents processed from cluster.")
    return [ExtractedDocument(**result) for result in results] 


