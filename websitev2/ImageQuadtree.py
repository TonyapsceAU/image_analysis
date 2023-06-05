from PIL import Image
import os

class Quadtree:
    def __init__(self):
        self.images = []
        self.divided = False
        self.cuts = []
    
    def check_img(self,path,image):
        w = image.width
        h = image.height
        lengh = 150
        if check_word(image)>0.5 or w<=lengh or h<=lengh:
            w, h = image.size
            self.images.append((image,path[len("temporary/"):]) )
        else :
            images = self.subdivide(image)
            end = str(images[0].width) + "x" + str(images[0].height) + ".jpg"
            for i in range(0,len(images)):
                img_path = (path +  str(i) + "_" + end)
                images[i].save(img_path)
                img = Image.open(img_path)
                self.cuts[i].check_img(path+str(i) + "_", img)
                os.remove(img_path)
                
            

    def subdivide(self,image):
        w, h = image.size

        t0 = Quadtree()
        t1 = Quadtree()
        t2 = Quadtree()
        t3 = Quadtree()
        self.cuts = [t0,t1,t2,t3]

        self.divided = True
        
        images = []
        images.append(image.crop((w/2, 0,w,h/2)))
        images.append(image.crop((0, 0, w/2, h/2)))
        images.append(image.crop((w/2, h/2, w, h)))
        images.append(image.crop((0, h/2, w/2,h)))
        
        return images
    
    def get_images(self):
        images = []
        if self.divided:
            for tree in self.cuts:
                temp = tree.get_images()
                if temp:
                    images += temp
            
        else:
            if self.images:
                images = self.images

        return images


def check_word(image):
    return 0 
    