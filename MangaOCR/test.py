import PIL.Image
from manga_ocr import MangaOcr

mocr = MangaOcr()
img = PIL.Image.open("Training_data/test/english.jpg")
text = mocr(img)
print(text)