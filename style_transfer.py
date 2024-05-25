from PyQt5.QtWidgets import QApplication, QPushButton, QGridLayout, QWidget, QFileDialog, QLabel
from PyQt5.QtGui import QFont, QPixmap, QImage
from PIL import Image
import tensorflow_hub as hub
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import threading
import os

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
    stylized_image = outputs[0].numpy()

    return stylized_image

def stylize(content_path, style_path):
    stylized_image = stylize_image(content_path, style_path)
    # Convert the stylized image to a PIL image
    stylized_image = Image.fromarray(np.uint8(stylized_image[0] * 255))

    # Get the original image's size
    original_image = Image.open(content_path)
    original_width, original_height = original_image.size
    content_ratio = original_height / original_width
    max_display_size = 350
    if original_width > original_height:
        new_width = max_display_size
        new_height = int(new_width * content_ratio)
    else:
        new_height = max_display_size
        new_width = int(new_height / content_ratio)

    # Convert the output image to a display image
    display_image = stylized_image.resize((new_width, new_height))
    data = display_image.convert("RGBA").tobytes("raw", "BGRA")
    qimage = QImage(data, display_image.size[0], display_image.size[1], QImage.Format_ARGB32)
    pixmap = QPixmap.fromImage(qimage)

    # Update the output label with the stylized image
    output_label.setPixmap(pixmap)

def stylize_button_click():
    threading.Thread(target=stylize, args=(content_path, style_path)).start()

def select_image(image_label):
    filename, _ = QFileDialog.getOpenFileName() 
    if filename: 
        image = Image.open(filename)
        width, height = image.size
        content_ratio = height / width
        max_display_size = 350
        if width > height:
            new_width = max_display_size
            new_height = int(new_width * content_ratio)
        else:
            new_height = max_display_size
            new_width = int(new_height / content_ratio)
        display_image = image.resize((new_width, new_height)) 
        data = display_image.convert("RGBA").tobytes("raw", "BGRA")
        qimage = QImage(data, display_image.size[0], display_image.size[1], QImage.Format_ARGB32)
        pixmap = QPixmap.fromImage(qimage)
        image_label.setPixmap(pixmap)
    return filename

def update_content_path():
    global content_path
    content_path = select_image(content_label)

def update_style_path():
    global style_path
    style_path = select_image(style_label)

app = QApplication([])

window = QWidget()
layout = QGridLayout()

button_font = QFont("Helvetica", 10)

content_path = ""
style_path = ""

content_label = QLabel()
content_button = QPushButton('Select Content Image')
content_button.setFont(button_font)
content_button.setStyleSheet("background-color: skyblue")
content_button.clicked.connect(update_content_path)

style_label = QLabel()
style_button = QPushButton('Select Style Image')
style_button.setFont(button_font)
style_button.setStyleSheet("background-color: skyblue")
style_button.clicked.connect(update_style_path)

output_label = QLabel()
stylize_button = QPushButton('Stylize')
stylize_button.setFont(button_font)
stylize_button.setStyleSheet("background-color: skyblue")
stylize_button.clicked.connect(lambda: threading.Thread(target=stylize, args=(content_path, style_path)).start())

layout.addWidget(content_label, 0, 0) # Content image label
layout.addWidget(output_label, 0, 1) # Output image label
layout.addWidget(style_label, 0, 2) # Style image label

layout.addWidget(content_button, 1, 0) # Content image button
layout.addWidget(stylize_button, 1, 1) # Stylize button
layout.addWidget(style_button, 1, 2) # Style image button

window.setLayout(layout)
window.show()

app.exec_()