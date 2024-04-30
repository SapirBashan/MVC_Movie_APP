import requests
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLineEdit, QListView, QWidget, QListWidget, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TodoView(QMainWindow): 
    def __init__(self):
        super().__init__()
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.movieEdit = QLineEdit(self)
        self.addButton = QPushButton("Add", self)
        self.removeButton = QPushButton("Remove", self)
        self.searchButton = QPushButton("Search", self)
        self.movieLabel = QLabel(self)
        self.posterLabel = QLabel(self)  # Define posterLabel here

        self.layout.addWidget(self.movieEdit)
        self.layout.addWidget(self.addButton)
        self.layout.addWidget(self.removeButton)
        self.layout.addWidget(self.searchButton)
        self.layout.addWidget(self.movieLabel)
        self.layout.addWidget(self.posterLabel)  # Add posterLabel to the layout

    def setController(self, controller):
        self.controller = controller
        self.addButton.clicked.connect(self.addMovie)
        self.removeButton.clicked.connect(self.removeMovie)
        self.searchButton.clicked.connect(self.searchMovie)
        #method to update the movie list when GetAllMoviesController is called
        self.movieList = QListWidget(self)
        self.layout.addWidget(self.movieList)

    def updateMovieList(self, movie_titles):
        self.movieList.clear()
        #now we will change the movie list to the new movie list
        self.movieList.addItems(movie_titles)


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
            self.updateMovieUI(movie_data)
        else:
            self.movieLabel.setText(f"Failed to fetch movie data for {movie_name}")

    def updateMovieUI(self, movie_data):
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

        #if there is not movie data then write no movie data
        if movie_details == "":
            movie_details = "No movie data"
        #make it so if the movie title is to long it will go to the next line
        self.movieLabel.setWordWrap(True)
        self.movieLabel.setText(movie_details)

        if movie_data['poster'] != 'N/A' and movie_data['poster'] is not None:
            data = requests.get(movie_data['poster']).content
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            self.posterLabel.setPixmap(pixmap)
        else:
            self.posterLabel.clear()