from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QDialog, QLineEdit, QFormLayout, QDialogButtonBox, QGridLayout
from PyQt5.QtGui import QPixmap, QFont, QImage
from PyQt5.QtCore import Qt
from PIL import Image
from component.frame_application import add_complex_frame_to_image
import cv2
import numpy as np

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
        self.name_button.setFixedSize(400, 50)
        self.name_button.setFont(font)
        self.name_button.clicked.connect(self.enter_image_name)

        # Center align the artwork name button
        layout.addWidget(self.name_button, alignment=Qt.AlignCenter)

        # Create a grid layout for the buttons
        grid_layout = QGridLayout()

        # Set the vertical spacing
        grid_layout.setVerticalSpacing(10)

        # Add the buttons
        self.home_button = QPushButton("메인 메뉴")
        self.home_button.setFixedSize(120, 50)  # Set the button size
        self.home_button.setFont(font)

        self.back_button = QPushButton("뒤로 가기")
        self.back_button.setFixedSize(120, 50)  # Set the button size
        self.back_button.setFont(font)

        self.save_button = QPushButton("저장하기")
        self.save_button.setFixedSize(120, 50)  # Set the button size
        self.save_button.setFont(font)

        grid_layout.addWidget(self.home_button, 0, 0)
        grid_layout.addWidget(self.back_button, 0, 1)
        grid_layout.addWidget(self.save_button, 0, 2)

        # Center align the buttons
        grid_layout.setAlignment(self.home_button, Qt.AlignCenter)
        grid_layout.setAlignment(self.back_button, Qt.AlignCenter)
        grid_layout.setAlignment(self.save_button, Qt.AlignCenter)

        # Add the grid layout to the main layout
        layout.addLayout(grid_layout)

        # Add a stretch at the end of the layout
        layout.addStretch(40)

        widget.setLayout(layout)
        widget.setContentsMargins(30, 30, 30, 30)  # Set the border
        self.setCentralWidget(widget)

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