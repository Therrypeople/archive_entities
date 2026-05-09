from neo4j import GraphDatabase
from PIL import Image
import ray
from dataclasses import dataclass
import hashlib

class Neo4JDatabase():
    driver
    ...

class OCRRayCluster():
    ...


@dataclass
class ExtractedDocument():
    document_title : str
    document: Image
    document_hash : str
    document_entities : list[str]


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


with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    create_person(driver, "Alice")

def write_to_neo4j():
    ...

def ray_extract_entities(self, file_paths : list[str]) -> list[ExtractedDocument]:
    """"""
    futures = []
    # Load data into ray cluster as PIL
    for i in range(len(file_paths)):
        file_reference_name = f"pil_image_{i}"
        globals()[file_reference_name] = Image.open(file_paths[i])
        self.ray_context.put(globals()[file_reference_name])
        file_reference_names.append(file_reference_name)

    images = [ for path in file_paths:
        img = 
        

    ...

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
