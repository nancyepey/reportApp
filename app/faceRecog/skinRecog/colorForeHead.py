from PIL import Image
import numpy as np

# getting a pixel rgb color
# def rgb_of_pixel(img_path, x, y):
#    im = Image.open(img_path).convert('RGB')
#    r, g, b = im.getpixel((x, y))
#    a = (r, g, b)
#    return a


#img = 'm1.jpg'
#print (rgb_of_pixel(img, 9, 8))
#print (rgb_of_pixel(img, 15, 15))


# dividing the image into blocks of 8 pixels x 8 pixels = 64pixels
img = Image.open('m1.jpg')
w, h = img.size # width, height of image
bw, bh = 8, 8 # block size

img = np.array(img)

sz = img.itemsize
shape = (h-bh+1, w-bw+1, bh, bw)
strides = (w*sz, sz, w*sz, sz)
blocks = np.lib.stride_tricks.as_strided(img, shape=shape, strides=strides)

print (blocks[1,1])