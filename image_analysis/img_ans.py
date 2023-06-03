import os
from PIL import Image
import cv2
from image_quadtree import Quadtree
# import tempfile
# import PyPDF2

# def convert_pdf_to_jpg(pdf_path):
#     # Create a temporary directory to store intermediate files
#     with tempfile.TemporaryDirectory() as temp_dir:
#         # Open the PDF file
#         with open(pdf_path, 'rb') as pdf_file:
#             pdf_reader = PyPDF2.PdfFileReader(pdf_file)

#             # Convert each page of the PDF to JPEG
#             for page_num in range(pdf_reader.numPages):
#                 # Convert the current page to an image
#                 pdf_page = pdf_reader.getPage(page_num)
#                 pdf_page.scale(2)  # Increase scale if necessary
#                 pdf_page.cropBox.lowerLeft = (0, 0)  # Remove margins if necessary
#                 pdf_page.cropBox.upperRight = (pdf_page.mediaBox.getUpperRight_x(), pdf_page.mediaBox.getUpperRight_y())  # Remove margins if necessary

#                 # Render the page as an image
#                 image = pdf_page.to_image()

#                 # Save the image as a temporary file
#                 temp_image_path = os.path.join(temp_dir, f'page{page_num + 1}.jpg')
#                 image.save(temp_image_path, 'JPEG')

#     return temp_image_path

def show_img(image_path):
    # Load the image
    image = cv2.imread(image_path)
    # Display the image with rectangles
    cv2.imshow('Image with Speech Bubbles', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def combine_words(images):
    merging = True

    while merging:
        merged_images = []
        merged = False

        for i in range(len(images)):
            merged_with_other = False

            for j in range(i + 1, len(images)):
                if check_overlap(images[i], images[j]):
                    combined_image = combine_image(images[i], images[j])
                    merged_images.append(combined_image)
                    merged_with_other = True
                    merged = True

            if not merged_with_other:
                merged_images.append(images[i])

        images = merged_images

        if not merged:
            merging = False

    return images




def check_overlap(img1, img2):
    _, x1, y1, w1, h1 = img1
    _, x2, y2, w2, h2 = img2

    proximity_factor = 1.25  # Adjust this factor to determine the proximity threshold

    # Calculate the proximity threshold for x and y directions
    x_proximity_threshold = proximity_factor * max(w1, w2)
    y_proximity_threshold = proximity_factor * max(h1, h2)

    if (abs(x1 - x2) <= x_proximity_threshold) and (abs(y1 - y2) <= y_proximity_threshold):
        return True

    return False



def combine_image(img1, img2):
    image1, x1, y1, w1, h1 = img1
    image2, x2, y2, w2, h2 = img2

    x_combined = min(x1, x2)
    y_combined = min(y1, y2)
    w_combined = max(x1 + w1, x2 + w2) - x_combined
    h_combined = max(y1 + h1, y2 + h2) - y_combined

    # Create a new blank image for combining
    image_combined = Image.new("RGB", (w_combined, h_combined))

    # Calculate the offset coordinates for pasting the images
    offset1 = (x1 - x_combined, y1 - y_combined)
    offset2 = (x2 - x_combined, y2 - y_combined)

    # Paste the first image onto the combined image
    image_combined.paste(image1, offset1)

    # Paste the second image onto the combined image
    image_combined.paste(image2, offset2)

    return (image_combined, x_combined, y_combined, w_combined, h_combined)

def show_images(images):
    for datas in images:
        img, _, _, _, _, = datas
        cv2.imshow('Image with Speech Bubbles', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    

# Folder path for input images
input_folder_path = '/Users/aushunying/Documents/coding/python/img_analisi/text_example'
# Create the "output" folder if it doesn't exist
output_folder_path = '/Users/aushunying/Documents/coding/python/img_analisi/v3/output'
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path) 

# word_folder_path = '/Users/aushunying/Documents/coding/python/img_analisi/v3/word'
# if not os.path.exists(word_folder_path):
#     os.makedirs(word_folder_path)
# other_folder_path = '/Users/aushunying/Documents/coding/python/img_analisi/v3/other'
# if not os.path.exists(other_folder_path):
#     os.makedirs(other_folder_path)
    
    
# Process each image in the input folder
coun = 0
for filename in os.listdir(input_folder_path):
    if coun==2:
        break
    # Convert the PDF to JPEG
    if filename.lower().endswith('.pdf'):
        image_path = convert_pdf_to_jpg(input_folder_path)
    
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image_path = os.path.join(input_folder_path, filename)
    print(image_path)
    show_img(image_path)
    
    
    # Load the image
    image = Image.open(image_path)
    
    # find all words in images
    image_quadtree = Quadtree()
    image_quadtree.check_img(image,0,0)
    # print(len(image_quadtree.images),image.size)
    for datas in image_quadtree.images:
        img, _, _, _, _, = datas
        cv2.imshow('Image with Speech Bubbles', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    
    # combine words into seach bobble
    images = combine_words(image_quadtree.images)
    for datas in images:
        img, _, _, _, _, = datas
        cv2.imshow('Image with Speech Bubbles', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    # do ocr to images
    
    # replace speach bobble image with text
    
    # place speach bobble back 
    
    coun+=1
    
        
            
            
