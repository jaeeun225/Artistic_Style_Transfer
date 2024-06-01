from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel, QMainWindow, QGridLayout, QScrollArea, QFrame
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from functools import partial
import os
from artist_select import ArtistSelect
from artwork import ArtworkPage
from component.background_setting import set_background

class GalleryPage(QMainWindow):
    def __init__(self, main_page):
        super().__init__()

        self.main_page = main_page
        self.setWindowTitle("갤러리")
        self.setFixedSize(500, 700)

        widget = QWidget()
        layout = QVBoxLayout()

        set_background(self, r"resource\wall.jpg")

        title = QLabel("감상할 작품을 선택해주세요")
        title_font = QFont("NanumMyeongjo", 13)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)

        font = QFont("NanumMyeongjo", 10)

        back_button = QPushButton('뒤로 가기')
        back_button.setFixedSize(400, 80)
        back_button.setFont(font)
        back_button.clicked.connect(self.go_back)

        current_dir = os.getcwd()
        gallery_collection_ico_dir = os.path.join(current_dir, "Gallery Collection/ico")
        artworks = os.listdir(gallery_collection_ico_dir)

        scroll = QScrollArea()  # Create a scroll area
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QGridLayout(scroll_content)  # Use QGridLayout
        scroll_layout.setVerticalSpacing(20)

        for i, artwork in enumerate(artworks):
            button = QPushButton()
            icon = QPixmap(os.path.join(gallery_collection_ico_dir, artwork))
            scaled_icon = icon.scaled(96, 96, Qt.KeepAspectRatio)
            button.setIcon(QIcon(scaled_icon))
            button.setIconSize(QSize(96, 96)) 
            button.setFixedSize(110, 110) 
            button.clicked.connect(partial(self.open_artwork_page, artwork))
            row = i // 3  # Calculate row index
            col = i % 3  # Calculate column index
            scroll_layout.addWidget(button, row, col)

        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)

        layout.addWidget(title)
        layout.addWidget(scroll)  # Add the scroll area to the layout
        layout.addWidget(back_button)

        widget.setLayout(layout)
        widget.setContentsMargins(30, 30, 30, 30)
        self.setCentralWidget(widget)

    def go_back(self):
        self.hide()
        self.main_page.show()

    def open_artwork_page(self, artwork):
        self.artwork_page = ArtworkPage(artwork)
        self.artwork_page.show()