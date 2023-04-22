import pytesseract
from PIL import Image

class OCR:
    def __init__(self, image_file, language):
        # img_type = ["jpg","jpeg","png"]
        # for i in img_type:
        #     print(self.check_path(image_file+img_type))
        self.language = language
        self.image_file = image_file

    def main(self, output_file):
        self.load_image()
        self.perform_ocr()
        self.save_text(output_file)
        # self.check_path()
        
        
    def load_image(self):
        self.image = Image.open(self.image_file)
        
    # def check_path(self):
    #     if os.path.exists(self.image_path):
    #         return 1
    #     else:
    #         return 0

    def perform_ocr(self):
        self.text = pytesseract.image_to_string(self.image , lang = self.language)

    def save_text(self, output_file):
        with open(output_file, 'w') as f:
            f.write(self.text)

        
