import easyocr
reader = easyocr.Reader(['ja'], gpu=False) # this needs to run only once to load the model into memory
result = reader.readtext('Training_data/test/japanese_hiragana.jpg', detail = 0)

print(result)