import os
import datetime
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel, QMainWindow, QGridLayout
from PyQt5.QtGui import QFont, QPixmap, QImage
from PyQt5.QtCore import Qt
from PIL import Image
import numpy as np
import re
from component.frame_application import add_complex_frame_to_image
from component.background_setting import set_background

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

        set_background(self, r"resource\wall.jpg")

        # split artist name and title
        artist_name, artwork_title = artwork_name.split('의', 1)

        title_font = QFont("NanumMyeongjo", 20, QFont.Bold)
        font = QFont("NanumMyeongjo", 10)

        # title label
        # delete (2), (3), etc. from the title
        artwork_title = re.sub(r'\s\(\d+\)$', '', artwork_title.strip())
        self.artwork_title_label = QLabel(artwork_title)
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

        # Check if the artwork title contains a number in parentheses at the end
        series_match = re.search(r'\s\(\d+\)$', artwork_name)
        if series_match:
            # If it does, create a label with the series information
            artwork_name2 = re.sub(r'\s\(\d+\)$', '', artwork_name.strip())
            series_info = f"작품정보: {artwork_name2} 연작입니다."
            self.series_label = QLabel(series_info)
            self.series_label.setFont(font)
            layout.addWidget(self.series_label)

        else:
            # If it doesn't, add parentheses and a number to the artwork name
            artwork_name2 = artwork_name.strip() + " (2)"
            # Check if a file with this name exists in the directory
            if os.path.isfile(os.path.join("Gallery Collection", artwork_name2 + '.jpg')):
                artwork_name2 = re.sub(r'\s\(\d+\)$', '', artwork_name.strip())
                # If it does, create a label with the series information
                series_info = f"작품정보: {artwork_name2} 연작입니다."
                self.series_label = QLabel(series_info)
                self.series_label.setFont(font)
                layout.addWidget(self.series_label)

        layout.addStretch(20)

        widget.setLayout(layout)
        widget.setContentsMargins(35, 30, 35, 30)
        self.setCentralWidget(widget)