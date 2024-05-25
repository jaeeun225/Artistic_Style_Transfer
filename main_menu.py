from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel, QMainWindow, QGridLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from artist_select import ArtistSelect

class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My mini art gallery")
        self.setFixedSize(500, 700)

        widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("My mini art gallery")
        title_font = QFont("Helvetica", 20)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)  # Center align the title

        create_button = QPushButton('작품 만들기')
        create_button.setFixedSize(320, 80)  # Set the size of the button
        create_button.clicked.connect(self.open_next_page)

        gallery_button = QPushButton('갤러리')
        gallery_button.setFixedSize(320, 80)  # Set the size of the button

        exit_button = QPushButton('나가기')
        exit_button.setFixedSize(320, 80)  # Set the size of the button
        exit_button.clicked.connect(app.quit)

        button_layout = QGridLayout()
        button_layout.setSpacing(30)
        button_layout.addWidget(create_button, 0, 0)
        button_layout.addWidget(gallery_button, 1, 0)
        button_layout.addWidget(exit_button, 2, 0)

        layout.addWidget(title)
        layout.addLayout(button_layout)

        widget.setLayout(layout)
        widget.setContentsMargins(30, 30, 30, 30)  # Set the border
        self.setCentralWidget(widget)

    def open_next_page(self):
        self.hide()  # Hide the main page
        self.next_page = ArtistSelect(self)  # Create the next page with a reference to the main page
        self.next_page.show()  # Show the next page

app = QApplication([])
window = MainPage()
window.show()
app.exec_()