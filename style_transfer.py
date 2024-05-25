from PyQt5.QtWidgets import QApplication, QPushButton, QGridLayout, QWidget, QFileDialog, QLabel
from PyQt5.QtGui import QFont, QPixmap, QImage
from PIL import Image
import tensorflow_hub as hub
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import threading
import os

class ImageProcessor:
    def __init__(self, content_label, style_label, output_label):
        self.content_path = ""
        self.style_path = ""
        self.content_label = content_label
        self.style_label = style_label
        self.output_label = output_label

    def update_content_path(self):
        self.content_path = self.select_image(self.content_label)

    def update_style_path(self):
        self.style_path = self.select_image(self.style_label)

    def select_image(self, image_label):
        filename, _ = QFileDialog.getOpenFileName() 
        if filename: 
            self.set_image_label(filename, image_label)
        return filename

    def set_image_label(self, filename, image_label):
        image = self.load_img(filename)
        original_width, original_height = image.size
        content_ratio = original_height / original_width
        max_display_size = 350
        if original_width > original_height:
            new_width = max_display_size
            new_height = int(new_width * content_ratio)
        else:
            new_height = max_display_size
            new_width = int(new_height / content_ratio)
        image = image.resize((new_width, new_height))
        data = image.convert("RGBA").tobytes("raw", "BGRA")
        qimage = QImage(data, image.size[0], image.size[1], QImage.Format_ARGB32)
        pixmap = QPixmap.fromImage(qimage)
        image_label.setPixmap(pixmap)
    
    def load_img(self, path_to_img):
        img = Image.open(path_to_img)
        return img

    def stylize_image(self, content_path, style_path):
        # Load the content and style images.
        content_image = np.array(self.load_img(content_path))
        style_image = np.array(self.load_img(style_path))

        # Normalize the images
        content_image = content_image.astype(np.float32)[np.newaxis, ...] / 255.
        style_image = style_image.astype(np.float32)[np.newaxis, ...] / 255.

        # Resize the style image to 256x256.
        style_image = tf.image.resize(style_image, (256, 256))

        # Load the model.
        hub_module = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

        # Stylize the image.
        outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
        stylized_image = outputs[0].numpy()

        return stylized_image

    def stylize(self):
        stylized_image = self.stylize_image(self.content_path, self.style_path)
        # Convert the numpy array to PIL Image
        stylized_image = np.squeeze(stylized_image, axis=0)
        stylized_image = (stylized_image * 255).astype(np.uint8)
        stylized_image = Image.fromarray(stylized_image)

        # Get the original image's size
        original_image = Image.open(self.content_path)  # Changed from content_path to self.content_path
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
        self.output_label.setPixmap(pixmap)

    def stylize_button_click(self):
        threading.Thread(target=self.stylize).start()

app = QApplication([])

window = QWidget()
layout = QGridLayout()

button_font = QFont("Helvetica", 10)

content_label = QLabel()
content_button = QPushButton('Select Content Image')
content_button.setFont(button_font)
content_button.setStyleSheet("background-color: skyblue")

style_label = QLabel()
style_button = QPushButton('Select Style Image')
style_button.setFont(button_font)
style_button.setStyleSheet("background-color: skyblue")

output_label = QLabel()
stylize_button = QPushButton('Stylize')
stylize_button.setFont(button_font)
stylize_button.setStyleSheet("background-color: skyblue")

image_processor = ImageProcessor(content_label, style_label, output_label)

content_button.clicked.connect(image_processor.update_content_path)
style_button.clicked.connect(image_processor.update_style_path)
stylize_button.clicked.connect(image_processor.stylize_button_click)

layout.addWidget(content_label, 0, 0) # Content image label
layout.addWidget(output_label, 0, 1) # Output image label
layout.addWidget(style_label, 0, 2) # Style image label

layout.addWidget(content_button, 1, 0) # Content image button
layout.addWidget(stylize_button, 1, 1) # Stylize button
layout.addWidget(style_button, 1, 2) # Style image button

window.setLayout(layout)
window.show()

app.exec_()