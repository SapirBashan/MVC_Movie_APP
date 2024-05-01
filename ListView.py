import requests
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QGridLayout, QScrollArea, QSizePolicy, QApplication,QHBoxLayout
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TodoView(QMainWindow): 
    def __init__(self):
        super().__init__()
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create a horizontal layout for the top bar
        self.top_layout = QHBoxLayout()

        self.movieEdit = QLineEdit(self)
        self.movieEdit.setMaximumWidth(300)
        # Set the style and placeholder text of the search bar
        self.movieEdit.setStyleSheet("border: 1px solid white;")
        self.movieEdit.setPlaceholderText("Enter movie")

        self.addButton = QPushButton("Add", self)
        self.removeButton = QPushButton("Remove", self)
        self.searchButton = QPushButton("Search", self)
        self.refreshButton = QPushButton("Back", self)
        self.refreshButton.clicked.connect(self.refresh)

        # Set the style and font of the buttons
        button_font = QFont('Arial', 10)
        button_style = "border: 1px solid white;"
        for button in [self.addButton, self.removeButton, self.searchButton, self.refreshButton]:
            button.setFont(button_font)
            button.setStyleSheet(button_style)

        self.top_layout.addWidget(self.movieEdit)
        self.top_layout.addWidget(self.searchButton)
        self.top_layout.addWidget(self.addButton)
        self.top_layout.addWidget(self.removeButton)
        self.top_layout.addWidget(self.refreshButton)

        self.movieLabel = QLabel(self)
        self.movieLabel.setFont(QFont('Arial', 14))

        self.posterLayout = QGridLayout()  

        self.posterWidget = QWidget()
        self.posterWidget.setLayout(self.posterLayout)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.posterWidget)

        self.layout.addLayout(self.top_layout)
        self.layout.addWidget(self.scrollArea)
        self.layout.addWidget(self.movieLabel)

        self.posterWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.controller = None

    def updateMovieUI(self, movie_data, flag):
        movie_details = ""
        if movie_data['title'] != "N/A" and movie_data['title'] is not None:
            movie_details += f"Title: {movie_data['title']}\n"
        if movie_data['year'] != "N/A" and movie_data['year'] is not None:
            movie_details += f"Year: {movie_data['year']}\n"
        if movie_data['rated'] != "N/A" and movie_data['rated'] is not None:
            if movie_data['rated'] == "R":
                movie_details += f"Rated: SHIGETZ\n"
            elif movie_data['rated'] == "PG-13" or movie_data['rated'] == "PG":
                movie_details += f"Rated: BE-DI-AVAD\n"
            elif movie_data['rated'] == "G":
                movie_details += f"Rated: KOSHER\n"
            else:
                movie_details += f"Rated: {movie_data['rated']}\n"
        if movie_data['type'] != "N/A" and movie_data['type'] is not None:
            movie_details += f"Type: {movie_data['type']}\n"
        if movie_data['plot'] != "N/A" and movie_data['plot'] is not None:
            movie_details += f"Plot: {movie_data['plot']}\n"
        if movie_data['imdbRating'] != "N/A" and movie_data['imdbRating'] is not None:
            movie_details += f"IMDB Rating: {movie_data['imdbRating']}\n"

        if movie_details == "":
            movie_details = "No movie data"
        
        self.movieLabel.setWordWrap(True)
        self.movieLabel.setText(movie_details)

        if movie_data['poster'] != 'N/A' and movie_data['poster'] is not None:
            if flag:
                layout = QVBoxLayout(self.central_widget)
                text_label = QLabel("Hello, PyQt!")
                layout.addWidget(text_label)
            else:
                data = requests.get(movie_data['poster']).content
                pixmap = QPixmap()
                pixmap.loadFromData(data)
                self.movieLabel.setPixmap(pixmap)
        else:
            self.movieLabel.clear()

    def updateMovieList(self, movie_posters):
        # Clear existing posters
        for i in reversed(range(self.posterLayout.count())):
            self.posterLayout.itemAt(i).widget().setParent(None)

        row = 0
        col = 0
        for poster_url in movie_posters:
            pixmap = self.get_pixmap_from_url(poster_url)
            if pixmap:
                label = QLabel()
                label.setPixmap(pixmap)
                label.mouseDoubleClickEvent = lambda event, url=poster_url: self.showMovieDetails(url)  # Double-click event handler
                self.posterLayout.addWidget(label, row, col)
                col += 1
                if col >= 4:  # Adjust the number of columns based on your preference
                    row += 1
                    col = 0

    def get_pixmap_from_url(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                return pixmap
        except Exception as e:
            print(f"Error loading image from URL: {e}")
        return None

    def setController(self, controller):
        self.controller = controller
        self.addButton.clicked.connect(self.addMovie)
        self.removeButton.clicked.connect(self.removeMovie)
        self.searchButton.clicked.connect(self.searchMovie)

    def addMovie(self):
        movie_name = self.movieEdit.text()
        movie_data = self.controller.searchMovieController(movie_name)
        if self.controller.addMovieController(movie_data):
            self.movieLabel.setText(f"Movie {movie_name} added successfully")
        else:
            self.movieLabel.setText(f"Failed to add movie {movie_name}")

    def removeMovie(self):
        movie_name = self.movieEdit.text()
        if self.controller.removeMovieController(movie_name):
            self.movieLabel.setText(f"Movie {movie_name} removed successfully")
        else:
            self.movieLabel.setText(f"Failed to remove movie {movie_name}")

    def searchMovie(self):
        movie_name = self.movieEdit.text()
        movie_data = self.controller.searchMovieController(movie_name)
        if movie_data:
            self.updateMovieUI(movie_data, True)
            self.updateMovieList([movie_data['poster']])  # Update poster layout with the poster URL
        else:
            self.movieLabel.setText(f"Failed to fetch movie data for {movie_name}")

    def showMovieDetails(self, url):
        movie_data = self.controller.getMovieDetailsByPosterController(url)
        if isinstance(movie_data, list):
            for movie in movie_data:
                if isinstance(movie, dict):
                    self.updateMovieUI(movie, True)
                else:
                    print("Invalid movie data format.")
        elif isinstance(movie_data, dict):
            self.updateMovieUI(movie_data, True)
        else:
            print(f"Unexpected type {type(movie_data)} for movie_data")

    def refresh(self):
        self.controller.GetAllMoviesController()
        self.movieLabel.setText("Movies refreshed successfully")
        self.movieEdit.clear()