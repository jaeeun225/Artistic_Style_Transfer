from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image

class MyArtistResult(QMainWindow):
    def __init__(self, image_path):
        super().__init__()

        self.setWindowTitle("Result Page")
        self.setFixedSize(500, 700)

        widget = QWidget()
        layout = QVBoxLayout()

        self.result_label = QLabel()

        # Load the image
        pixmap = QPixmap(image_path)

        # Get the original image's size
        original_image = Image.open(image_path)
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

        # Now you can use scaled_pixmap to set the pixmap of a QLabel or any other widget
        self.result_label.setPixmap(scaled_pixmap)

        # Align the image to the center
        self.result_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.result_label)

        widget.setLayout(layout)
        widget.setContentsMargins(30, 30, 30, 30)  # Set the border
        self.setCentralWidget(widget)