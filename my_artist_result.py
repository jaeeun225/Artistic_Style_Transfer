from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QDialog, QLineEdit, QFormLayout, QDialogButtonBox, QGridLayout, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap, QFont, QImage
from PyQt5.QtCore import Qt
from PIL import Image, ImageEnhance
from component.frame_application import add_complex_frame_to_image
import cv2
import numpy as np
import os

class MyArtistResult(QMainWindow):
    def __init__(self, image_path):
        super().__init__()

        self.setWindowTitle("완성된 작품")
        self.setFixedSize(500, 700)

        widget = QWidget()
        layout = QVBoxLayout()

        layout.setSpacing(20)  # Set the spacing between widgets

        self.result_label = QLabel()

        # Load the image
        pixmap = QPixmap(image_path)

        # Get the original image's size
        original_image = Image.open(image_path)

        # Convert the PIL Image to a numpy array
        numpy_image = np.array(original_image)

        # Apply the complex frame to the image
        framed_image = add_complex_frame_to_image(numpy_image)

        # Convert the numpy array back to a PIL Image
        framed_image = Image.fromarray(framed_image)

        # Convert the PIL Image to a QImage
        qim = QImage(framed_image.tobytes(), framed_image.width, framed_image.height, QImage.Format_RGB888)

        # Create a QPixmap from the QImage
        pixmap = QPixmap.fromImage(qim)

        # Get the original image's size
        original_width, original_height = original_image.size
        content_ratio = original_height / original_width
        max_display_size = 400
        if original_width > original_height:
            new_width = max_display_size
            new_height = int(new_width * content_ratio)
        else:
            new_height = max_display_size
            new_width = int(new_height / content_ratio)

        # Scale the image to the desired size for display
        scaled_pixmap = pixmap.scaled(new_width, new_height, Qt.KeepAspectRatio)

        # Use scaled_pixmap to set the pixmap of a QLabel or any other widget
        self.result_label.setPixmap(scaled_pixmap)

        # Align the image to the center
        self.result_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.result_label)

        # Add the artwork name label
        self.artwork_name_label = QLabel()
        self.artwork_name_label.setFont(QFont("NanumMyeongjo", 12))
        self.artwork_name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.artwork_name_label)

        font = QFont("NanumMyeongjo", 10)

        self.name_button = QPushButton("작품명을 붙여주세요")
        self.name_button.setFixedSize(400, 40)
        self.name_button.setFont(font)
        self.name_button.clicked.connect(self.enter_image_name)

        self.save_button = QPushButton('작품 소장하기')
        self.save_button.setFixedSize(400, 40)
        self.save_button.setFont(font)
        self.save_button.clicked.connect(self.save_image) 

        layout.addLayout(self.centered_layout(self.name_button))
        layout.addItem(QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addLayout(self.centered_layout(self.save_button))

        layout.addStretch(30)

        widget.setLayout(layout)
        widget.setContentsMargins(30, 30, 30, 30)  # Set the border
        self.setCentralWidget(widget)

    def centered_layout(self, widget):
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(widget)
        hbox.addStretch()
        return hbox

    def enter_image_name(self):
        # Create a custom dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("작품명 입력")

        font = QFont("NanumMyeongjo", 10)

        # Create two line edits for the artist's name and the artwork's name
        self.artist_edit = QLineEdit()
        self.artist_edit.setFont(font)
        self.artwork_edit = QLineEdit()
        self.artwork_edit.setFont(font)

        artist_label = QLabel("작가:")
        artist_label.setFont(font)
        artwork_label = QLabel("작품명:")
        artwork_label.setFont(font)

        form_layout = QFormLayout()
        form_layout.addRow( artist_label, self.artist_edit)
        form_layout.addRow(artwork_label, self.artwork_edit)

        # Create a button box with OK and Cancel buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        form_layout.addRow(button_box)

        # Set the dialog's layout
        dialog.setLayout(form_layout)

        # Show the dialog and wait for the user to click OK or Cancel
        result = dialog.exec_()

        # If the user clicked OK, update the button text and artwork name label
        if result == QDialog.Accepted:
            artist_name = self.artist_edit.text()
            artwork_name = self.artwork_edit.text()
            self.name_button.setText("작품명 다시 붙이기")
            self.artwork_name_label.setText(f"{artist_name}의 {artwork_name}")

    def save_image(self):
        if not self.artwork_name_label.text():
            return

        # Save the image with the artwork name
        current_dir = os.getcwd()
        save_dir = os.path.join(current_dir, "Gallery Collection")

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        artwork_name = self.artwork_name_label.text()
        save_path = os.path.join(save_dir, f"{artwork_name}.jpg")

        # Rename and move the file
        os.rename(os.path.join(current_dir, "output.jpg"), save_path)

        # Convert the saved image to a bitmap icon
        img = Image.open(save_path)

        img = img.convert('RGB')

        # enhance the contrast of the image by 2.0
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0) 

        # Resize the image 32X32 to use as an icon
        img = img.resize((32, 32))

        # save the icon file
        icon_save_path = os.path.join(save_dir, f"{artwork_name}.ico")
        img.save(icon_save_path, format='ICO')