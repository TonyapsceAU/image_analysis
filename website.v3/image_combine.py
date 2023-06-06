from PIL import Image
# from math import abs

# def image_combine(OGimages):
#     for image in OGimages:
#         xy = image.split("(")[0].split(")")[0].split(",")
#         x, y = int(xy[0]),int(xy[1])

def vertical(up_path, down_path, output_path):
    up = Image.open(up_path)
    up_x = int(up_path.split("(")[1].split(")")[0].split(",")[0])
    up_y = int(up_path.split("(")[1].split(")")[0].split(",")[1])
    down = Image.open(down_path)
    down_x = int(down_path.split("(")[1].split(")")[0].split(",")[0])
    down_y = int(down_path.split("(")[1].split(")")[0].split(",")[1])
    left = max(up_x, down_x)
    # top_right = max(up_x + up.width, down_x + down.width)
    combined_width = max(up_x + up.width, down_x + down.width) - min(up_x, down_x)
    combined_height = up.height + down.height
    combined_image = Image.new('RGBA', (combined_width, combined_height))
    combined_image.paste(up, (0, 0))
    combined_image.paste(down, (abs(up_x - down_x), up.height))
    combined_image.save(output_path.split("(")[0]+"(" + str(left) + "," + str(up_y) + ")" + ".png")

def horizontal(left_path, right_path, output_path):
    left = Image.open(left_path)
    left_x = int(left_path.split("(")[1].split(")")[0].split(",")[0])
    left_y = int(left_path.split("(")[1].split(")")[0].split(",")[1])
    right = Image.open(right_path)
    right_x = int(right_path.split("(")[1].split(")")[0].split(",")[0])
    right_y = int(right_path.split("(")[1].split(")")[0].split(",")[1])
    top = max(left_x, right_x)
    # top_right = max(left_x + left.width, right_x + right.width)
    combined_height = max(left_y + left.height, right_y + right.height) - min(left_y, right_y)
    combined_width = left.width + right.width
    combined_image = Image.new('RGBA', (combined_width, combined_height))
    combined_image.paste(left, (0, 0))
    combined_image.paste(right, (left.width, abs(left_y - right_y)))
    combined_image.save(output_path.split("(")[0]+"(" + str(left_x) + "," + str(top) + ")" + ".png")
def combine(OGimages):
    output_path = "websitev4/temporary/" + OGimages[0].split(".")[0]
    for image_path in OGimages:
        image = Image.open(image_path)
        x = image_path.split("(")[1].split(")")[0].split(",")[0]
        y = image_path.split("(")[1].split(")")[0].split(",")[1]
        for subimage_path in OGimages:
            subimage = Image.open(subimage_path)
            if subimage == image: continue
            sx = subimage_path.split("(")[1].split(")")[0].split(",")[0]
            sy = subimage_path.split("(")[1].split(")")[0].split(",")[1]
            if sy == (y+y.height): #down
                vertical(image_path, subimage_path, output_path)
                break
            elif sx == (x+x.width): #right
                horizontal(image_path, subimage_path, output_path)
                break
            elif y == (sy+sy.height): #up
                vertical(subimage_path, image_path, output_path)
                break
            elif x == (sx+sx.width): #left
                horizontal(subimage_path, image_path, output_path)
                break

# Example usage
# image1_path = 'website.v3\japanese(0,0).jpg'
# image2_path = 'website.v3\japanese(1,2).jpg'
# output_path = 'website.v3\japanese('

# vertical(image1_path, image2_path, output_path)
# horizontal(image1_path, image2_path, output_path)

