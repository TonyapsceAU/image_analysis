import easyocr
reader = easyocr.Reader(['en'], gpu=False) # this needs to run only once to load the model into memory
result = reader.readtext('Training_data/test/english.jpg')#, detail = 0)

f = open('EasyOCR/result.txt', 'w')
for item in result:
	f.write(str(item) + "\n")
f.close()
# print(type(result))
