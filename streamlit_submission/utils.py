from neo4j import GraphDatabase, Driver
from PIL import Image
import ray
from dataclasses import dataclass
import hashlib
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from paddleocr import PaddleOCR
import re

class Neo4JSettings(BaseSettings):
    """"""
    model_config = SettingsConfigDict(env_prefix='NEO4J_')
    uri: str
    username: str
    password: str

class RaySettings(BaseSettings):
    """"""
    model_config = SettingsConfigDict(env_prefix='RAY_')
    address: str

@dataclass
class ExtractedDocument():
    document_title : str
    document: Image
    document_hash : str
    document_entities : list[str]

class Neo4JDatabase():
    """"""
    driver: Driver

    def __init__(self, settings: Neo4JSettings):
        self.driver = GraphDatabase.driver(settings.uri,
                                           auth=(settings.username,settings.password))

    def upload_extracted_document(self, extraction : ExtractedDocument):
        """"""

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

def ray_extract_entities(file_paths : list[Path]) -> list[ExtractedDocument]:
    """"""
    # Load data into ray cluster
    ray_references = []
    for i in range(len(file_paths)):
        ray_dict = {"image": Image.open(file_paths[i]),
                    "image_name": file_paths[i].name,
                    }
        ray_references.append(ray.put(ray_dict))
        
    # Submit ray jobs to process data
    results = ray.get([
        ocr_extract_entities.remote(**image) for image in ray_references
    ])

    return [ExtractedDocument(**result) for result in results] 

@ray.remote
def ocr_extract_entities(image: Image, image_name: str) -> dict:
    """"""
    # Regex pattern to capture captilized multiword entities longer than 3 character
    entity_pattern = r'\b(?=.{4,})[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'
    ocr = PaddleOCR(use_angle_cls=True, lang='en', enable_mkldnn=False)
    
    result = ocr.predict(asarray(image))
    text = " ".join(result[0]["rec_texts"])
    entities = re.findall(text, entity_pattern)

    return {"document_title":image_name,
            "document_hash": hashlib.md5(image.tobytes()).hexdigest(),
            "document_entities": entities} 
