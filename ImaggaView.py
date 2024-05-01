from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class ImaggaView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Imagga View"))
