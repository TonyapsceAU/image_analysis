from PIL import Image
# from Check_word import check_word

class Quadtree:
    def __init__(self):
        self.images = []
        self.divided = False
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None

    def check_word(self,image):
        w, h = image.size
        if(w<1000 or h<1000):
            return True
        else:
            return False
    
    def check_img(self,image,x,y):
        # image.show()
        # if check_word(image)>0.5:
        if self.check_word(image):
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
