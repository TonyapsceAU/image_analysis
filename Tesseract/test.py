from PIL import Image
import pytesseract

img = Image.open("Python/japanese.jpg")
text = pytesseract.image_to_string(img, lang='jpn', config='--psm 5')
print(text)
# import os
# print(os.getcwd())