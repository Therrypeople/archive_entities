from streamlit_submission.utils import ocr_extract_entities
import pytest
from PIL import Image

@pytest.fixture
def test_image_1():
    return {"image":Image.open("test_data/example_1.png"),"image_name":"test_image_1"}

@pytest.fixture
def expected_result_1():
    return {
    'document_title': 'test_image_1',
    'document_hash': '10b9226c476c16c510a177ca17ad954e',
    'document_entities': [
        'Dawson',
        'Ballaarat',
        'Powell',
        'Doing',
        'Victoria',
        'Elliot',
        'Peter',
        'Church',
        'Handfield',
        'Whittenbury',
        'Frances Mary',
        'Melbourne',
        'Sandridge',
        'Dickinson',
        'Samuel Furneaux Mann',
        'Christina',
        'Millar',
        'Emerald Hill',
        'Ist August',
        'Guichen Bay',
        'South Australia',
        'David Munro',
        'Boomer',
        'Australian',
        'Gurthon Gatehouse',
        'Flect',
        'Scotland'
    ]
}

@pytest.fixture
def test_image_2():
    return {"image":Image.open("test_data/example_2.jpg"),"image_name":"test_image_2"}


@pytest.fixture
def expected_result_2():
    return {
    'document_title': 'test_image_2',
    'document_hash': '56db23acb0c848b786816d3d412f1483',
    'document_entities': [
        'Extracts',
        'Sydney Momning Herald',
        'April',
        'Mrs Joseph Abrahams',
        'Mrs Joseph Lauriston Terrace',
        'Phillip Street',
        'March',
        'Mrs J',
        'Alcock',
        'Riley Mrs J',
        'Street',
        'Surry Hills',
        'Mrs E',
        'Allen',
        'Forbes',
        'Mrs E',
        'June',
        'Mrs A',
        'Alley',
        'Mt Mrs A',
        'Victoria',
        'Mrs Alton',
        'Mrs Snow',
        'Dagmar House',
        'Toll',
        'Paddington',
        'Both',
        'Mrs John Andrew',
        'Holloway Mrs John Cottage',
        'Rosehill Street',
        'Redfern',
        'Mrs Thomas Andrews',
        'Penrith',
        'Mrs Thomas',
        'April',
        'Mrs Armstrong',
        'Burrowa',
        'June',
        'Mrs F',
        'Artlett',
        'Mrs F',
        'Parramatta Streets',
        'March',
        'Mrs J',
        'Austin',
        'Wesleyan Mission Mrs J',
        'House',
        'Newington Heights',
        'Savaii',
        'Samoa',
        'April',
        'Mrs Lewis Austin',
        'Noumea',
        'New Caledonia',
        'Mrs Lewis',
        'Mrs W',
        'Avery',
        'Tree Hill',
        'Mt Victoria',
        'Mrs W',
        'Port Stephens Family History Socicty Inc',
        'Page'
    ]
}

def test_entity_extraction_1(test_image_1,expected_result_1):
    entities = ocr_extract_entities(**test_image_1)
    print(entities)
    assert entities == expected_result_1

def test_entity_extraction_2(test_image_2,expected_result_2):
    entities = ocr_extract_entities(**test_image_2)
    print(entities)
    assert entities == expected_result_2