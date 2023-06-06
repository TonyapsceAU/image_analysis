from PIL import Image
import pytesseract

img = Image.open("Training_data/test/japanese_hiragana.jpg")
text = pytesseract.image_to_string(img, lang='eng') #, config='--psm 5' (vertical)
print(text)
# import os
# print(os.getcwd())