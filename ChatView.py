from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class ChatView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Chat View"))
