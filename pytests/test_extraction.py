from streamlit_submission.utils import ocr_extract_entities
import pytest
from PIL import Image

@pytest.fixture
def test_image_1():
    return {"image":Image.open("test_data/example_1.png"),"image_name":"test_image_1"}

@pytest.fixture
def expected_result_1():
    return {}

@pytest.fixture
def test_image_2():
    return {"image":Image.open("test_data/example_1.jpg"),"image_name":"test_image_2"}


@pytest.fixture
def expected_result_2():
    return {}


def test_entity_extraction_1(test_image_1,expected_result_1):
    entities = ocr_extract_entities(**test_image_1)
    assert entities == expected_result_1

def test_entity_extraction_2(test_image2,expected_result_2):
    entities = ocr_extract_entities(**test_image_2)
    assert entities == expected_result_2