import os
import tempfile
import PyPDF2
from PIL import Image
from image_quadtree import Quadtree

def convert_pdf_to_jpg(pdf_path):
    # Create a temporary directory to store intermediate files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Open the PDF file
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)

            # Convert each page of the PDF to JPEG
            for page_num in range(pdf_reader.numPages):
                # Convert the current page to an image
                pdf_page = pdf_reader.getPage(page_num)
                pdf_page.scale(2)  # Increase scale if necessary
                pdf_page.cropBox.lowerLeft = (0, 0)  # Remove margins if necessary
                pdf_page.cropBox.upperRight = (pdf_page.mediaBox.getUpperRight_x(), pdf_page.mediaBox.getUpperRight_y())  # Remove margins if necessary

                # Render the page as an image
                image = pdf_page.to_image()

                # Save the image as a temporary file
                temp_image_path = os.path.join(temp_dir, f'page{page_num + 1}.jpg')
                image.save(temp_image_path, 'JPEG')

    return temp_image_path



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



# Folder path for input images
input_folder_path = 'kbsicnjksdcnj/input'

# Create the "output" folder if it doesn't exist
output_folder_path = 'kbsicnjksdcnj/output'
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)
    
    
# Process each image in the input folder
for filename in os.listdir(input_folder_path):
    # Convert the PDF to JPEG
    if image_path.lower().endswith('.pdf'):
        image_path = convert_pdf_to_jpg(image_path)
    
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image_path = os.path.join(input_folder_path, filename)
        
    # Load the image
    image = cv2.imread(image_path)
    image.show()
    
    # find all words in images
    image_quadtree = Quadtree(4)
    image_quadtree.check_img(image)
    for datas in imaimage_quadtree.images:
        img, _, _, _, _, = datas
        img.show()
        
    
    # combine words into seach bobble
    images = combine_words(imaimage_quadtree.imagesges)
    for datas in images.images:
        img, _, _, _, _, = datas
        img.show()
    
    # do ocr to images
    
    # replace speach bobble image with text
    
    # place speach bobble back 
    
        
            
            
