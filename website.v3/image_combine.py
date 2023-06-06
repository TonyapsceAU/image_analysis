from PIL import Image

def image_combine(OGimages):
    for image in OGimages:
        xy = image.split("(")[0].split(")")[0].split(",")
        x, y = int(xy[0]),int(xy[1])
