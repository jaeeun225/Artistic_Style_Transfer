import tensorflow_hub as hub
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

content_path = 'example/sea2.jpg'
style_path = 'monet/monet3.jpg'

def load_img(path_to_img):
    img = plt.imread(path_to_img)
    img = img.astype(np.float32)[np.newaxis, ...] / 255.
    return img

def stylize_image(content_path, style_path):
    # Load the content and style images.
    content_image = load_img(content_path)
    style_image = load_img(style_path)

    # Resize the style image to 256x256.
    style_image = tf.image.resize(style_image, (256, 256))

    # Load the model.
    hub_module = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

    # Stylize the image.
    outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
    stylized_image = outputs[0]

    return stylized_image

stylized_image = stylize_image(content_path, style_path)
plt.imshow(stylized_image[0])
plt.show()