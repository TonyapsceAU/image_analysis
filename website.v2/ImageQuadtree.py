from PIL import Image
import os
import js2py

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
            tf = """
                const URL = "https://teachablemachine.withgoogle.com/models/z8ceXdsVg/";
                let model, labelContainer, maxPredictions, classinfo;

                async function init(event) {
                    const modelURL = URL + "model.json";
                    const metadataURL = URL + "metadata.json";
                    model = await tmImage.load(modelURL, metadataURL);
                    maxPredictions = model.getTotalClasses();

                    labelContainer = document.getElementById("label-container");
                    for (let i = 0; i < maxPredictions; i++) {
                        labelContainer.appendChild(document.createElement("div"));
                    }
                    handleImageUpload(event);
                }

                async function predict(image) {
                    if (model) {
                        const prediction = await model.predict(image);
                        classinfo = console.log(prediction[0].probability.toFixed(2))
                        for (let i = 0; i < maxPredictions; i++) {
                            const classPrediction =
                                prediction[i].className + ": " + prediction[i].probability.toFixed(2);
                            labelContainer.childNodes[i].innerHTML = classPrediction;
                        }
                    }
                }

                function handleImageUpload(event) {
                    const file = event.target.files[0];
                    const reader = new FileReader();

                    reader.onload = async function() {
                        const image = new Image();
                        image.src = reader.result;
                        image.onload = async function() {
                            document.getElementById("image-container").innerHTML = "";
                            document.getElementById("image-container").appendChild(image);
                            await predict(image);
                        };
                    };
                    reader.readAsDataURL(file);
                }
                
                document.getElementById("image-upload").addEventListener("change", init);
            """
            class_info = js2py.tf()
            class_info.execute(tf)
            print(class_info.classinfo)
            if check_word(current_image) > 0.5 or w <= lengh or h <= lengh:
                self.images.append(current_path[len("website.v2/temporary/"):]+".jpg") 
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
    
