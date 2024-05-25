from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QMainWindow, QGridLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class ArtistSelect(QMainWindow):
    def __init__(self, main_page):
        super().__init__()

        self.main_page = main_page

        self.setWindowTitle("Artist Select")
        self.setFixedSize(500, 650)

        widget = QWidget()

        gallery_button = QPushButton('갤러리 화가 선택하기')
        gallery_button.setFixedSize(320, 200)  # Set the size of the button
        my_artist_button = QPushButton('나의 화가 선택하기')
        my_artist_button.setFixedSize(320, 200)  # Set the size of the button

        back_button = QPushButton('뒤로 가기')
        back_button.setFixedSize(320, 80)  # Set the size of the button
        back_button.clicked.connect(self.go_back)  # Connect the button click event to the handler

        button_layout = QGridLayout()
        button_layout.setSpacing(30)
        button_layout.addWidget(gallery_button, 0, 0)
        button_layout.addWidget(my_artist_button, 1, 0)
        button_layout.addWidget(back_button, 2, 0)

        widget.setLayout(button_layout)
        widget.setContentsMargins(30, 30, 30, 30)  # Set the border
        self.setCentralWidget(widget)

    def go_back(self):
        self.close()  # Close the current page
        self.main_page.show()  # Show the main page