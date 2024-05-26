from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel, QMainWindow, QGridLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from my_artist import MyArtistPage
class ArtistSelect(QMainWindow):
    def __init__(self, main_page):
        super().__init__()

        self.main_page = main_page

        self.setWindowTitle("Artist Select")
        self.setFixedSize(500, 700)

        widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("화가를 선택하세요")
        title_font = QFont("NanumMyeongjo", 14)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)

        font = QFont("NanumMyeongjo", 10)

        gallery_button = QPushButton('갤러리 화가 선택하기')
        gallery_button.setFixedSize(400, 200)
        gallery_button.setFont(font)

        my_artist_button = QPushButton('나의 화가 선택하기')
        my_artist_button.setFixedSize(400, 200)
        my_artist_button.setFont(font)
        my_artist_button.clicked.connect(self.open_my_artist_page)

        back_button = QPushButton('뒤로 가기')
        back_button.setFixedSize(400, 80)
        back_button.setFont(font)
        back_button.clicked.connect(self.go_back)

        button_layout = QGridLayout()
        button_layout.setSpacing(30)
        button_layout.addWidget(title, 0, 0)
        button_layout.addWidget(gallery_button, 1, 0)
        button_layout.addWidget(my_artist_button, 2, 0)
        button_layout.addWidget(back_button, 3, 0)

        layout.addWidget(title)
        widget.setLayout(button_layout)

        widget.setContentsMargins(30, 30, 30, 30)  # Set the border
        self.setCentralWidget(widget)

    def open_my_artist_page(self):
        self.hide()  # Hide the current page
        self.my_artist_page = MyArtistPage(self)  # Create the MyArtistPage
        self.my_artist_page.show()  # Show the MyArtistPage

    def go_back(self):
        self.close()  # Close the current page
        self.main_page.show()  # Show the main page