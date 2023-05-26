from check_word import Check_word

class Quadtree:
    def __init__(self, capacity):
        self.capacity = capacity
        self.images = []
        self.divided = False
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None

    def check_img(self,image,x,y):
        if check_word(image):
            self.images.append((image,x,y)) 
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
        w = image.width
        h = image.height

        self.northeast = Quadtree(self.capacity)
        self.northwest = Quadtree(self.capacity)
        self.southeast = Quadtree(self.capacity)
        self.southwest = Quadtree(self.capacity)

        self.divided = True
        
        images = []
        images.append(image[y:y+h/2, x+w/2:x+w])
        images.append(image[y:y+h/2, x:x+w/2])
        images.append(image[y+h/2:y+h, x+w/2:x+w])
        images.append(image[y+h/2:y+h, x:x+w/2])
        
        
        return images
