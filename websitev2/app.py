from flask import Flask, render_template, request, redirect, url_for
import urllib.request
import os
from werkzeug.utils import secure_filename
import cv2 
from ImageQuadtree import Quadtree
from PIL import Image
import shutil

app = Flask(__name__)
app.secret_key = "mnpw2123"
app.config['UPLOAD_FOLDER'] = 'static/upload'  # Folder to store uploaded images
        
def clear_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    folder = request.files.getlist('image_folder')  # Get the uploaded files

    
    # Create a directory to store the uploaded images
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    # clear_folder(app.config['UPLOAD_FOLDER'])
        
    if not os.path.exists("temporary"):
        # shutil.rmtree("temporary")
        os.makedirs("temporary")
    
    
    # Save the uploaded images to the server
    for file in folder:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return redirect(url_for('processed_images'))



@app.route('/processed_images')
def processed_images():
    # Get the list of processed images in the 'uploads' folder
    origenal_images = os.listdir(app.config['UPLOAD_FOLDER'])

    for image_name in origenal_images:
        image_quadtree = Quadtree()
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
        image = Image.open(image_path)
    
        image_quadtree.check_img("temporary/"+image_name.split('.')[0]+"_",image)
        words_images_path = image_quadtree.get_images()
        
        for words_image_path in words_images_path:
            word_image = Image.open("temporary/"+words_image_path)
            filename = words_image_path
            word_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            os.remove("temporary/"+words_image_path)
            
    # return render_template('myconsole.html', info=words_images_path)
    return render_template('processed_images.html', OGimages=origenal_images)


if __name__ == '__main__':
    app.run()
