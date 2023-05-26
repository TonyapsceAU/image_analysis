import cv2
import os

def find_words(image_path):
    image = cv2.imread(image_path)# Load the image
    rectangles = [] # Create a list to store the speech bubble rectangles
    
    # ger rectangle
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)# Convert the image to grayscale
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU) # Apply adaptive thresholding to obtain a binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)# Find contours in the binary image
    for contour in contours:# Iterate over the contours and find the speech bubble rectangles
        x, y, w, h = cv2.boundingRect(contour)
        rectangles.append((x, y, w, h))

    return rectangles



def draw_rectangles(image_path, rectangles):
    # Load the image
    image = cv2.imread(image_path)

    # Draw rectangles and display information on the image
    for (x, y, w, h) in rectangles:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Display the image with rectangles
    cv2.imshow('Image with Speech Bubbles', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Folder path for input images
input_folder_path = '/Users/aushunying/Documents/coding/python/img_analisi/text_example'
# Create the "output" folder if it doesn't exist
output_folder_path = '/Users/aushunying/Documents/coding/python/img_analisi/v3/output'
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)
    
# Process each image in the input folder
for filename in os.listdir(input_folder_path):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image_path = os.path.join(input_folder_path, filename)
        # Extract text regions and save them as separate images
        rectangles = find_words(image_path)
        print(image_path)
        if len(rectangles) :
            draw_rectangles(image_path, rectangles)
            
