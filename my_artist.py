from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMainWindow, QGridLayout, QSpacerItem, QSizePolicy, QLabel, QFileDialog
from PyQt5.QtGui import QFont, QPixmap, QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PIL import Image
import tensorflow_hub as hub
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import threading
import os
import cv2
from my_artist_result import MyArtistResult
from component.frame_application import add_complex_frame_to_image
from component.background_setting import set_background

class StylizeThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self, image_processor):
        super().__init__()
        self.image_processor = image_processor

    def run(self):
        output_image_path = self.image_processor.stylize()
        self.finished.emit(output_image_path)
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
        filename, _ = QFileDialog.getOpenFileName(None, "Select Image File", "", "Images (*.png *.xpm *.jpg *.bmp *.gif);;All Files (*)")
        if filename:
            self.set_image_label(filename, image_label)
        return filename

    def set_image_label(self, filename, image_label):
        image = self.load_img_with_frame(filename)
        original_width, original_height = image.size
        content_ratio = original_height / original_width
        if original_width > original_height:
            new_width = 240
            new_height = int(new_width * content_ratio)
        else:
            new_height = 180
            new_width = int(new_height / content_ratio)
        image = image.resize((new_width, new_height))
        data = image.convert("RGBA").tobytes("raw", "BGRA")
        qimage = QImage(data, image.size[0], image.size[1], QImage.Format_ARGB32)
        pixmap = QPixmap.fromImage(qimage)
        image_label.setPixmap(pixmap)

    def load_img(self, path_to_img):
        img = Image.open(path_to_img)
        return img

    def load_img_with_frame(self, path_to_img):
        img = self.load_img(path_to_img)
        # Convert the PIL Image to an OpenCV image (numpy array)
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        # Apply the frame
        img_with_frame = add_complex_frame_to_image(img_cv)
        # Convert the OpenCV image (numpy array) back to a PIL Image
        img = Image.fromarray(cv2.cvtColor(img_with_frame, cv2.COLOR_BGR2RGB))
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

        # Save the stylized image and return its path
        output_image_path = "output.jpg"
        stylized_image.save(output_image_path)

        # Get the original image's size
        original_image = Image.open(self.content_path)
        original_width, original_height = original_image.size
        content_ratio = original_height / original_width
        max_display_size = 200
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

        return output_image_path
    def stylize_button_click(self):
        self.stylize_thread = StylizeThread(self)
        self.stylize_thread.finished.connect(self.on_stylize_finished)
        self.stylize_thread.start()

    def on_stylize_finished(self, output_image_path):
        self.result_page = MyArtistResult(output_image_path)
        self.result_page.show()
class MyArtistPage(QMainWindow):
    def __init__(self, previous_page):
        super().__init__()

        self.previous_page = previous_page

        self.setWindowTitle("화가의 작업 공간")
        self.setFixedSize(500, 700)

        widget = QWidget()
        layout = QVBoxLayout()

        set_background(self, r"resource\wall.jpg")

        self.content_label = QLabel()
        self.style_label = QLabel()
        self.output_label = QLabel()
        
        self.image_processor = ImageProcessor(self.content_label, self.style_label, self.output_label)

        font = QFont("NanumMyeongjo", 10)

        content_button = QPushButton('화가가 그릴 이미지 가져오기')
        content_button.setFixedSize(400, 40)
        content_button.setFont(font)
        content_button.clicked.connect(self.image_processor.update_content_path)

        style_button = QPushButton('화가의 이전 작품 가져오기')
        style_button.setFixedSize(400, 40)
        style_button.setFont(font)
        style_button.clicked.connect(self.image_processor.update_style_path)

        stylize_button = QPushButton('작품 만들기')
        stylize_button.setFixedSize(400, 40)
        stylize_button.setFont(font)
        stylize_button.clicked.connect(self.image_processor.stylize_button_click)

        back_button = QPushButton('뒤로 가기')
        back_button.setFixedSize(400, 40)
        back_button.setFont(font)
        back_button.clicked.connect(self.go_back)

        layout.addLayout(self.centered_layout(self.content_label))
        layout.addItem(QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addLayout(self.centered_layout(content_button))
        layout.addItem(QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addLayout(self.centered_layout(self.style_label))
        layout.addItem(QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addLayout(self.centered_layout(style_button))
        layout.addItem(QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addLayout(self.centered_layout(stylize_button))
        layout.addItem(QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addLayout(self.centered_layout(back_button))

        widget.setLayout(layout)
        widget.setContentsMargins(30, 30, 30, 30)  # Set the border
        self.setCentralWidget(widget)

    def go_back(self):
        self.close()  # Close the current page
        self.previous_page.show()  # Show the previous page

    def centered_layout(self, widget):
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(widget)
        hbox.addStretch()
        return hbox