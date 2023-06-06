import os
import easyocr

class OCR:
    def __init__(self,path,language):
        self.reader = easyocr.Reader([language])
        self.folder_path = path

    def read_all_img(self):
        for filename in os.listdir(self.folder_path):
            if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
                img_path = os.path.join(self.folder_path, filename)
                results = self.read_image(img_path)
                return results
    
    
    def read_image(self, img_path):
        return self.reader.readtext(img_path)

if __name__ == '__main__':
    ocr = OCR("testimg","en")
    texts = ocr.read_all_img()
    for text in texts:
        print(text)
