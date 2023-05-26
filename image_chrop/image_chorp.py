import cv2
import os
import numpy as np

def find_speech_bubbles(image_path):
    image = cv2.imread(image_path)# Load the image
    rectangles = [] # Create a list to store the speech bubble rectangles
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)# Convert the image to grayscale
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU) # Apply adaptive thresholding to obtain a binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)# Find contours in the binary image
    
    for contour in contours:# Iterate over the contours and find the speech bubble rectangles
        x, y, w, h = cv2.boundingRect(contour)
        rectangles.append((x, y, w, h))

    return rectangles

def calculate_area_threshold(rectangles):
    total_area = sum(w * h for (_, _, w, h) in rectangles)
    average_area = total_area / len(rectangles)
    return average_area


def filter_speech_bubbles(rectangles):
    filtered_rectangles = []
    
    area_threshold = calculate_area_threshold(rectangles)

    for (x, y, w, h) in rectangles:
        aspect_ratio = float(w) / h
        area = w * h
        
        if area > area_threshold:
            filtered_rectangles.append((x, y, w, h))

    return filtered_rectangles

def calculate_middle_rectangle_size(rectangles):
    sorted_rectangles = sorted(rectangles, key=lambda rect: rect[2] * rect[3])  # Sort by area (width * height)
    num_rectangles = len(sorted_rectangles)

    if num_rectangles % 2 == 0:  # Even number of rectangles
        middle_index = num_rectangles // 2
        middle_rectangle = sorted_rectangles[middle_index]
    else:  # Odd number of rectangles
        middle_index = (num_rectangles - 1) // 2
        middle_rectangle = sorted_rectangles[middle_index]

    size = (middle_rectangle[2] + middle_rectangle[3])/2
    return size


def filter_extreme_rectangles(rectangles,maxs):
    filtered_rectangles = []
    mins = 5

    for rect in rectangles:
        x, y, w, h = rect
        if mins <= w <= maxs and mins <= h <= maxs:
            filtered_rectangles.append(rect)

    return filtered_rectangles

def combine_overlapping_rectangles(rectangles):
    merging = True
    i = 0
    count = 0

    while merging:
        if i < len(rectangles) - 1:
            op = check_overlap(rectangles[i], rectangles[i + 1])
            if op:
                combined_rect = combine_rectangles(rectangles[i], rectangles[i + 1])
                rectangles[i] = combined_rect
                del rectangles[i + 1]
                count = 0
            else:
                count += 1

            i += 1
        else:
            i = 0

        if count == len(rectangles)-1:
            merging = False

    return rectangles



def check_overlap(rect1, rect2):
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2

    if (x1 < x2 + w2*1,25 and x1 + w1*1,25 > x2 and y1 < y2 + h2*1,25 and y1 + h1*1,25 > y2):
        return True

    return False


def combine_rectangles(rect1, rect2):
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2

    x_combined = min(x1, x2)
    y_combined = min(y1, y2)
    w_combined = max(x1 + w1, x2 + w2) - x_combined
    h_combined = max(y1 + h1, y2 + h2) - y_combined

    return (x_combined, y_combined, w_combined, h_combined)


def draw_size_curve(rects):
    sorted_rects = sorted(rects, key=lambda rect: rect[2] * rect[3])  # Sort rectangles based on area (width * height)
    num_rects = len(sorted_rects)

    # Create a blank image with white background
    image = np.ones((300, 400, 3), dtype=np.uint8) * 255

    for i in range(num_rects):
        rect = sorted_rects[i]
        width, height = rect[2], rect[3]
        rect_height = int((width + height) / 2)

        # Calculate rectangle position and size on the image
        x = int(i * 400 / num_rects)
        y = 0
        rect_width = int(400 / num_rects)

        # Draw the rectangle on the image
        cv2.rectangle(image, (x, y), (x + rect_width, rect_height), (0, 255, 0), -1, cv2.LINE_AA)

    # Display the image
    cv2.imshow("Size Curve", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def draw_distribution_curve(rects):
    sorted_rects = sorted(rects, key=lambda rect: rect[2] * rect[3])  # Sort rectangles based on area (width * height)
    num_rects = len(sorted_rects)
    if num_rects==1:
        return rects[0][2] * rects[0][3]

    # Create a blank image with white background
    image = np.ones((600, 800, 3), dtype=np.uint8) * 255
    heights = []
    maxs = mins = 0
    if(0==len(rects)):
        return []
    for i in range(len(rects)):
        rect = sorted_rects[i]
        width, height = rect[2], rect[3]
        rect_height = int((width + height) / 2)
        if i == 0:
            mins = rect_height
        if i == len(rects) - 1:
            maxs = rect_height
        
        heights.append(rect_height)
    # print(heights)

    gap = 10
    # print(len(heights))
    smo = int(heights[len(heights) - 1] / gap)
    distribution = []
    for i in range(smo):
        distribution.append([0,0])
    for h in heights:
        for i in range(smo):
            if h < gap * (i + 1):
                distribution[i][0] += 1
                distribution[i][1] = h
                break
    # print(distribution)
            
    # for i in range(len(distribution)):
    #     # Calculate rectangle position and size on the image
    #     x = int(i * 800 / len(distribution))
    #     y = 600 - distribution[i][0]  # Adjust y-coordinate to start from the bottom
    #     rect_width = int(800 / len(distribution))

    #     # Draw the rectangle on the image
    #     cv2.rectangle(image, (x, y), (x + rect_width, 600), (0, 255, 0), -1, cv2.LINE_AA)
    #     info_text = str(distribution[i])
    #     cv2.putText(image, info_text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (0, 0, 0), 1, cv2.LINE_AA)
    
    new_d = []
    for h in distribution:
        if h[0]:
            new_d.append(h)

    # # Display the image
    # cv2.imshow("Size Curve", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    return new_d[len(new_d)-1][1]


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

        
def output_images_from_rectangles(image_path, rectangles, output_prefix):
    image = cv2.imread(image_path)
    output_dir = output_prefix

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cnt = len(os.listdir(output_dir))  # Get the number of existing images in the output directory

    for i, rect in enumerate(rectangles):
        x, y, w, h = rect
        cropped_img = image[y:y+h, x:x+w]
        output_path = os.path.join(output_dir, f"{cnt + i}.png")
        cv2.imwrite(output_path, cropped_img)


# Folder path for input images
input_folder_path = 'img_analisi/text_example'
# Create the "output" folder if it doesn't exist
output_folder_path = 'img_analisi/v3/output'
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)
# Process each image in the input folder
amount = 0
for filename in os.listdir(input_folder_path):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image_path = os.path.join(input_folder_path, filename)
        print(image_path)
        
        # Extract text regions and save them as separate images
        rectangles = find_speech_bubbles(image_path)
        
        if len(rectangles) :
            # draw_size_curve(rectangles)
            maxs = draw_distribution_curve(rectangles)*1.5
            
            # # filters
            # rectangles = filter_speech_bubbles(rectangles)
            rectangles = filter_extreme_rectangles(rectangles,maxs)
            # rectangles = combine_overlapping_rectangles(rectangles)
            
            # draw_rectangles(image_path, rectangles)
            name_without_extension = os.path.splitext(filename)[0]
            output_images_from_rectangles(image_path, rectangles, output_folder_path+"/"+name_without_extension)
            
    amount += 1
