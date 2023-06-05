from PIL import Image
import os

class Quadtree:
    def __init__(self):
        self.images = []
    
    def check_img(self, path, image):
        w = image.width
        h = image.height
        lengh = 75
        image.save(path + ".jpg")
        Stack = [path]
        while Stack:
            current_path = Stack.pop()
            current_image = Image.open(current_path+".jpg")
            w, h = current_image.size
            
            if check_word(current_image) > 0.5 or w <= lengh or h <= lengh:
                self.images.append(current_path[len("temporary/"):]+".jpg") 
            else:
                devided_images = self.subdivide(current_image)
                for i in range(0,len(devided_images)):
                    newimg_path = (current_path + str(i) + "_")
                    devided_images[i].save(newimg_path + ".jpg")
                    Stack.append(newimg_path)
                    
                os.remove(current_path+".jpg")
        
            

    def subdivide(self,image):
        w, h = image.size
        
        new_images = []
        new_images.append(image.crop((w/2, 0,w,h/2)))
        new_images.append(image.crop((0, 0, w/2, h/2)))
        new_images.append(image.crop((w/2, h/2, w, h)))
        new_images.append(image.crop((0, h/2, w/2,h)))
        
        return new_images
    
    def get_images(self):
        return self.images


def check_word(image):
    return 0 
    
