from flask import Flask, render_template, request, redirect, url_for
import urllib.request
import os
from werkzeug.utils import secure_filename
import cv2 
from ImageQuadtree import Quadtree
from PIL import Image
import shutil

app = Flask(__name__)
upload_pth = "website.v2/upload"
temp_path = "website.v2/temporary"
        
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    folder = request.files.getlist('image_folder')  # Get the uploaded files
    # if os.path.exists(upload_pth):
    #     os.rmdir(upload_pth)
    # os.makedirs(upload_pth)

    # if os.path.exists(temp_path):
    #     os.rmdir(temp_path)
    # os.makedirs(temp_path)
    
    if not os.path.exists(upload_pth):
        # os.rmdir(upload_pth)
        os.makedirs(upload_pth)

    if not os.path.exists(temp_path):
        # os.rmdir(temp_path)
        os.makedirs(temp_path)
    
    
    # Save the uploaded images to the server
    for file in folder:
        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_pth, filename))

    return redirect(url_for('processed_images'))



@app.route('/processed_images')
def processed_images():
    # Get the list of processed images in the 'uploads' folder
    origenal_images_path = os.listdir(upload_pth)

    for image_name in origenal_images_path:
        image_quadtree = Quadtree()
        image_path = os.path.join(upload_pth, image_name)
        image = Image.open(image_path)
    
        image_quadtree.check_img("website.v2/temporary/"+image_name.split('.')[0]+"_",image)
        words_images_path = image_quadtree.get_images()
        
        for words_image_path in words_images_path:
            word_image = Image.open("website.v2/temporary/"+words_image_path)
            filename = words_image_path
            word_image.save(os.path.join(upload_pth, filename))
            os.remove("website.v2/temporary/"+words_image_path)
            
    # return render_template('myconsole.html', info=words_images_path)
    return render_template('processed_images.html', OGimages=origenal_images_path)



if __name__ == '__main__':
    app.run()
