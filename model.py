import tensorflow as tf
import numpy as np
from PIL import Image, ImageFilter
import os
from tensorflow.keras.preprocessing.image import load_img
import PIL
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
from PIL import Image

def load_image(path, downfactor=1):
	original_img = load_img(path)
	downscaled = original_img.resize((original_img.size[0] // downfactor,
		original_img.size[1] // downfactor), Image.BICUBIC)
	return (original_img, downscaled)

def normalize(image):
    return image / 255

def grayscale(input):
    input = tf.image.rgb_to_yuv(input)
    last_dimension_axis = len(input.shape) - 1
    y, u, v = tf.split(input, 3, axis=last_dimension_axis)
    return y
def get_y_channel(image):
	ycbcr = image.convert("YCbCr")
	(y, cb, cr) = ycbcr.split()
	y = np.array(y)
	y = normalize(y.astype("float32"))
	return (y, cb, cr)

def upscale_image(img, model):
    y, cb, cr = get_y_channel(img)
    input = np.expand_dims(y, axis=0)
    out = model.predict(input)[0]
    out *= 255.0
    out = out.clip(0, 255)
    out = out.reshape((np.shape(out)[0], np.shape(out)[1]))
    new_y = Image.fromarray(np.uint8(out), mode="L")
    new_cb = cb.resize(new_y.size, PIL.Image.BICUBIC)
    new_cr = cr.resize(new_y.size, PIL.Image.BICUBIC)
    res = PIL.Image.merge("YCbCr", (new_y, new_cb, new_cr)).convert(
        "RGB"
    )
    return res




#upscale4x("X4/0801x4.png")

def upscale2x(original_img):
    image = Image.open(original_img)
    model = load_model('resolution2x.h5')
    scaled_image = upscale_image(image, model)
    return scaled_image


def upscale3x(original_img):
    image = Image.open(original_img)
    model = load_model('resolution3x.h5')
    scaled_image = upscale_image(image, model)
    return scaled_image

def upscale4x(original_img):
    image = Image.open(original_img)
    model = load_model('resolution.h5')
    scaled_image = upscale_image(image, model)
    return scaled_image


def median_filter(original_img):
    image = Image.open(original_img)
    image = image.convert('RGB')
    filtered_image = image.filter(ImageFilter.MedianFilter(5))
    return filtered_image


img = load_img('noise-before.jpg')
#img = median_filter(img)
#img =  upscale2x(img)
#img.save("1234.png")



#plt.figure(figsize=(10, 5))


#plt.subplot(1, 3, 2)
#plt.imshow(scaled_image)
#plt.title('Model')
#plt.axis('off')

#plt.show()
