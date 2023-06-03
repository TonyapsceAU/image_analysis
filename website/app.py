from flask import Flask, render_template, request, redirect, url_for
import urllib.request
import os
from werkzeug.utils import secure_filename
import cv2 
from ImageQuadtree import Quadtree
from PIL import Image

app = Flask(__name__)
app.secret_key = "mnpw2123"
app.config['UPLOAD_FOLDER'] = 'static/upload'  # Folder to store uploaded images
        
        
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    folder = request.files.getlist('image_folder')  # Get the uploaded files

    # Create a directory to store the uploaded images
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

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
        image_quadtree.check_img(image, 0, 0)
        words_images = image_quadtree.get_images()

        count_digits = len(str(len(words_images)))
        for i, word_image_tuple in enumerate(words_images):
            word_image = word_image_tuple[0]  # Extract the actual image from the tuple
            count_str = str(i+1).zfill(count_digits)
            filename = f"{image_name.split('.')[0]}_{count_str}.{image_name.split('.')[1]}"
            word_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
    # origenal_images = os.listdir(app.config['UPLOAD_FOLDER'])

    return render_template('processed_images.html', OGimages=origenal_images)


if __name__ == '__main__':
    app.run()
