from PIL import Image

count = 0

class Quadtree:
    def __init__(self):
        self.images = []
        self.divided = False
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None
    
    def check_img(self,image,x,y):
        global count 
        if check_word(image)>0.5:
            w, h = image.size
            self.images.append((image,x,y,w,h)) 
        else :
            if not self.divided:
                images = self.subdivide(image,x,y)
                
            w = image.width
            h = image.height
            if self.northeast.check_img(images[0],x+w/2,y):
                return True
            elif self.northwest.check_img(images[1],x,y):
                return True
            elif self.southeast.check_img(images[2],x+w/2,y+h/2):
                return True
            elif self.southwest.check_img(images[3],x,y+h/2):
                return True

    def subdivide(self,image,x,y):
        w, h = image.size

        self.northeast = Quadtree()
        self.northwest = Quadtree()
        self.southeast = Quadtree()
        self.southwest = Quadtree()

        self.divided = True
        
        images = []
        images.append(image.crop((x + w/2, y,x+w, y+h/2)))
        images.append(image.crop((x, y, x + w/2, y + h/2)))
        images.append(image.crop((x + w/2, y+h/2, x+w, y+h)))
        images.append(image.crop((x, y+h/2, x+w/2,y+h)))
        return images
    
    def get_images(self):
        images = []
        if self.divided:
            temp = self.northeast.get_images()
            if temp:
                images += temp

            temp = self.northwest.get_images()
            if temp:
                images += temp

            temp = self.southeast.get_images()
            if temp:
                images += temp

            temp = self.southwest.get_images()
            if temp:
                images += temp
        else:
            if self.images:
                images = self.images

        return images


def check_word(image):
    # return True
    global count 
    if(count==0):
        count+=1
        return False
    else :
        return True
    