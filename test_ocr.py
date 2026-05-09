
from paddleocr import PaddleOCR
import re

# class ScannedEntities:





# Initialize the OCR engine (defaults to English)
ocr = PaddleOCR(use_angle_cls=True, lang='en', enable_mkldnn=False)

# Run OCR on an image
img_path = 'test_data/example_2.jpg'
result = ocr.predict(img_path)


text = []
text.append(" ".join(result[0]["rec_texts"]))


# Matches capitalized words and allows for spaces
pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'

places = [re.findall(pattern, t) for t in text]
filtered = [[element for element in l if len(element)>3] for l in places]
print(filtered) 