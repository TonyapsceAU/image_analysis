from PIL import Image
import pytesseract

img = Image.open("Python/test.jpg")
text = pytesseract.image_to_string(img, lang='jpn')
print(text)
# import os
# print(os.getcwd())