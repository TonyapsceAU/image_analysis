from flask import Flask, render_template, request, redirect, url_for
# import urllib.request
import os
from werkzeug.utils import secure_filename
# import cv2 
from ImageQuadtree import Quadtree
from PIL import Image
import shutil

app = Flask(__name__)
upload_path = "website.v3/upload"
temp_path = "website.v3/temporary"
        
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    folder = request.files.getlist('image_folder')  # Get the uploaded files

    # Save the uploaded images to the server
    for file in folder:
        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_path, filename))

    return redirect(url_for('processed_images'))



@app.route('/processed_images')
def processed_images():
    # Get the list of processed images in the 'uploads' folder
    origenal_images_path = os.listdir(upload_path)

    for image_name in origenal_images_path:
        image_quadtree = Quadtree()
        image_path = os.path.join(upload_path, image_name)
        image = Image.open(image_path)
    
        image_quadtree.check_img("website.v3/temporary/"+image_name.split('.')[0]+"_",image)
        words_images_path = image_quadtree.get_images()
        
        for words_image_path in words_images_path:
            word_image = Image.open("website.v3/temporary/"+words_image_path)
            filename = words_image_path
            # print(filename)
            word_image.save(os.path.join(upload_path, filename))
            os.remove("website.v3/temporary/"+words_image_path)
            
    # return render_template('myconsole.html', info=words_images_path)
    return render_template('processed_images.html', OGimages=origenal_images_path)



if __name__ == '__main__':
    os.system("cls")
    if os.path.exists(upload_path):
        shutil.rmtree(upload_path)
        # try: os.rmdir(upload_pth)
        # except: 
    os.makedirs(upload_path)
        
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)
        # try: os.rmdir(temp_path)
        # except: os.makedirs(temp_path)
    os.makedirs(temp_path)
    app.run()
