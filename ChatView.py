import time
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QFrame, QScrollArea
from PyQt6.QtGui import QFont

class ChatView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # Horizontal layout for buttons at the top
        button_layout = QHBoxLayout()

        # Button to generate movie recommendation using Chat GPT-3-Ultra
        self.chat_gpt3_button = QPushButton("Use Chat GPT-3-Ultra to recommend 5 movies\n based on your personal preferences")
        self.chat_gpt3_button.setStyleSheet("border: 2px solid white; padding: 10px;")  # Larger button with white border and padding
        self.chat_gpt3_button.setFont(QFont('Arial', 14))  # Bigger text font
        button_layout.addWidget(self.chat_gpt3_button)

        # Button to generate movie recommendation using Chat GPT-Devincie
        self.chat_gpt_devincie_button = QPushButton("Use Chat GPT-Devincie to recommend 5 movies\n based on your personal preferences")
        self.chat_gpt_devincie_button.setStyleSheet("border: 2px solid white; padding: 10px;")  # Larger button with white border and padding
        self.chat_gpt_devincie_button.setFont(QFont('Arial', 14))  # Bigger text font
        button_layout.addWidget(self.chat_gpt_devincie_button)
 
        # Add button layout to main layout
        layout.addLayout(button_layout)

        # Frame to contain the label with scroll area
        text_frame = QFrame()
        text_frame.setStyleSheet("border: 2px solid white;")  # White border
        text_frame.setMinimumHeight(300)  # Set minimum height for the frame
        text_layout = QVBoxLayout(text_frame)

        # Scroll area for the label
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Disable horizontal scroll bar
        text_layout.addWidget(scroll_area)

        # Label for movie recommendation
        self.movie_recommendation_label = QLabel("Press one of the buttons above to get a movie recommendation")
        self.movie_recommendation_label.setFont(QFont('Arial', 16))  # Bigger font
        self.movie_recommendation_label.setAlignment(Qt.AlignmentFlag.AlignTop)  # Align text to top
        self.movie_recommendation_label.setWordWrap(True)  # Allow text to wrap to next line
        self.movie_recommendation_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)  # Enable text selection with mouse
        scroll_area.setWidget(self.movie_recommendation_label)  # Set label as widget for scroll area

        # Add text frame to main layout
        layout.addWidget(text_frame)

        self.setLayout(layout)

        # Connect button clicks to functions
        self.chat_gpt3_button.clicked.connect(self.chat_gpt3_button_clicked)
        self.chat_gpt_devincie_button.clicked.connect(self.chat_gpt_devincie_button_clicked)

    def setController(self, controller):
        self.controller = controller

    def chat_gpt3_button_clicked(self):
        # Use QTimer and async so that while waiting for the response from the API, the GUI does not freeze
        # and call the function loadingAnimation to show the user that the program is working
        self.loadingAnimation(True)
        QTimer.singleShot(100, lambda: self.handleRecommendation("GPT-3-Ultra"))

    def chat_gpt_devincie_button_clicked(self):
        self.loadingAnimation(True)
        QTimer.singleShot(100, lambda: self.handleRecommendation("GPT-Devincie"))

    def handleRecommendation(self, model):
        recommendation = self.controller.getMovieRecommendationController(model)
        self.loadingAnimation(False)
        self.movie_recommendation_label.setText(recommendation)

    def loadingAnimation(self, loading):
        if loading:
            self.loading_timer = QTimer(self)
            self.loading_timer.timeout.connect(self.updateLoadingText)
            self.loading_timer.start(50)  # 200 milliseconds interval for updating text
        else:
            self.loading_timer.stop()
            self.movie_recommendation_label.setText("")

    def updateLoadingText(self):
        self.movie_recommendation_label.setText("Loading Information")
        text = self.movie_recommendation_label.text()
        if text.endswith("...."):
            self.movie_recommendation_label.setText("Loading Information")
        else:
            self.movie_recommendation_label.setText(text + ".")