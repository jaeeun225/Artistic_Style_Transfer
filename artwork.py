import os
import datetime
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel, QMainWindow, QGridLayout
from PyQt5.QtGui import QFont, QPixmap, QImage
from PyQt5.QtCore import Qt
from PIL import Image
import numpy as np
from component.frame_application import add_complex_frame_to_image

class ArtworkPage(QMainWindow):
    def __init__(self, artwork_name):
        super().__init__()

        # delete .ico
        artwork_name = artwork_name.rsplit('.', 1)[0]

        self.setWindowTitle(artwork_name)
        self.setFixedSize(500, 700)

        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(25)

        # split artist name and title
        artist_name, artwork_title = artwork_name.split('의')

        title_font = QFont("NanumMyeongjo", 20, QFont.Bold)
        font = QFont("NanumMyeongjo", 10)

        # title label
        self.artwork_title_label = QLabel(artwork_title.strip())
        self.artwork_title_label.setFont(title_font)
        self.artwork_title_label.setAlignment(Qt.AlignCenter)

        # artist label
        self.artist_label = QLabel(f"아티스트: {artist_name.strip()}")
        self.artist_label.setFont(font)

        # artwork image path(.jpg)
        current_dir = os.getcwd()
        artwork_image_path = os.path.join(current_dir, "Gallery Collection", artwork_name + '.jpg')

        self.artwork_image = QLabel()
        self.artwork_image.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(artwork_image_path)

        # add frame
        numpy_image = np.array(Image.open(artwork_image_path))
        framed_image = add_complex_frame_to_image(numpy_image)
        pixmap = QPixmap.fromImage(QImage(framed_image.data, framed_image.shape[1], framed_image.shape[0], QImage.Format_RGB888))

       # scale size
        max_display_size = 400
        original_width, original_height = pixmap.width(), pixmap.height()

        content_ratio = original_height / original_width
        if original_width > original_height:
            new_width = max_display_size
            new_height = int(new_width * content_ratio)
        else:
            new_height = max_display_size
            new_width = int(new_height / content_ratio)

        pixmap = pixmap.scaled(new_width, new_height, Qt.KeepAspectRatioByExpanding)

        self.artwork_image.setPixmap(pixmap)
        self.artwork_image.setScaledContents(False)

        # get year
        timestamp = os.path.getmtime(artwork_image_path)
        dt = datetime.datetime.fromtimestamp(timestamp)
        year = dt.year

        # year label
        self.year_label = QLabel(f"제작연도: {year}")
        self.year_label.setFont(font)

        layout.addWidget(self.artwork_image)
        layout.addWidget(self.artwork_title_label)
        layout.addWidget(self.artist_label)
        layout.addWidget(self.year_label)

        layout.addStretch(20)

        widget.setLayout(layout)
        widget.setContentsMargins(35, 30, 35, 30)
        self.setCentralWidget(widget)