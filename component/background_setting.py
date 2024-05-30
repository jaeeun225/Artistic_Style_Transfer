from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt

def set_background(widget, image_path):
    background = QPixmap(image_path)

    palette = QPalette()

    palette.setBrush(QPalette.Background, QBrush(background))

    widget.setPalette(palette)