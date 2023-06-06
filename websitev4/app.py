from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from ImageQuadtree import Quadtree
from PIL import Image
import shutil

app = Flask(__name__)
upload_path = "upload"
temp_path = "temporary"
app.secret_key = "mnpw2123"
app.config['UPLOAD_FOLDER'] = 'static/upload'  # Folder to store uploaded images
        
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    folder = request.files.getlist('image_folder')  # Get the uploaded files
    
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        shutil.rmtree(app.config['UPLOAD_FOLDER'])
    os.makedirs(app.config['UPLOAD_FOLDER'])
        
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)
    os.makedirs(temp_path)
    
    
    # # Create a directory to store the uploaded images
    # if not os.path.exists(app.config['UPLOAD_FOLDER']):
    #     os.makedirs(app.config['UPLOAD_FOLDER'])
    # if not os.path.exists(temp_path):
    #     os.makedirs(temp_path)
    
    
    # Save the uploaded images to the server
    for file in folder:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return redirect(url_for('processed_images'))


@app.route('/processed_images')
def processed_images():
    # Get the list of processed images in the 'uploads' folder
    origenal_images_path = os.listdir(app.config['UPLOAD_FOLDER'])
    txt = 0
    for image_name in origenal_images_path:
        # txt += 1
        image_quadtree = Quadtree()
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
        image = Image.open(image_path)
    
        image_quadtree.check_img("temporary/"+image_name.split('.')[0]+"_0",image)
        words_images_path = image_quadtree.get_images()
        
        for words_image_path in words_images_path:
            txt += 1
            word_image = Image.open("temporary/"+words_image_path)
            filename = words_image_path
            word_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # os.remove("temporary/"+words_image_path) 
        # txt += image_quadtree.content
            
    # return render_template('myconsole.html', info=txt)
    return render_template('processed_images.html', OGimages=origenal_images_path)



if __name__ == '__main__':    
    app.run()