import PIL.Image
from manga_ocr import MangaOcr

mocr = MangaOcr()
img = PIL.Image.open("Training_data/test/japanese_small.jpg") #input combine image path here
text = mocr(img)
print(text) #output text