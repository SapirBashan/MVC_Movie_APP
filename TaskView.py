# TaskView.py
import requests
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLineEdit, QListView, QWidget, QListWidget, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

# Create a view class that inherits from QMainWindow
# The view class will have a setController method that takes the controller as an argument
# The setController method will connect the signals from the view to the controller
# The view class will have methods to add, delete, and complete a task
class TodoView(QMainWindow): 

    def __init__(self):
        super().__init__()
        
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.todoEdit = QLineEdit(self)
        self.addButton = QPushButton("Add", self)
        self.todoList = QListView(self)
        self.deleteButton = QPushButton("Delete", self)
        self.completeButton = QPushButton("Complete", self)
        
        self.todoEdit.returnPressed.connect(self.addTodo)

        self.todoList.setVisible(True)  # Make sure the list is visible

        self.layout.addWidget(self.todoEdit)
        self.layout.addWidget(self.addButton)
        self.layout.addWidget(self.todoList)
        self.layout.addWidget(self.deleteButton)
        self.layout.addWidget(self.completeButton)

        #**************************************************************************#

        self.movieEdit = QLineEdit(self)
        self.searchButton = QPushButton("Search", self)
        self.movieLabel = QLabel(self)
        self.posterLabel = QLabel(self)


        self.movieEdit.returnPressed.connect(self.searchMovie)

        self.layout.addWidget(self.movieEdit)
        self.layout.addWidget(self.searchButton)
        self.layout.addWidget(self.movieLabel)
        self.layout.addWidget(self.posterLabel)
        #**************************************************************************#
    

    def setController(self, controller):
            self.addButton.clicked.connect(self.addTodo)
            self.deleteButton.clicked.connect(self.deleteTodo)
            self.completeButton.clicked.connect(self.completeTodo)
            self.searchButton.clicked.connect(self.searchMovie)

            self.controller = controller

    def addTodo(self):
        text = self.todoEdit.text()
        if text:
            self.controller.addTodo(text)
            self.todoEdit.clear()

    def deleteTodo(self):
        index = self.todoList.currentIndex()
        if index.isValid():
            self.controller.deleteTodo(index)

    def completeTodo(self):
        index = self.todoList.currentIndex()
        if index.isValid():
            self.controller.completeTodo(index)

        # Set the model for the QListView
        self.todoList.setModel(self.controller.model)

  
    def searchMovie(self):
        movie_name = self.movieEdit.text()
        movie_data = self.controller.searchMovieController(movie_name)
        if movie_data:
            self.updateMovieUI(movie_data)
        else:
            print("Failed to fetch movie data")

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
        self.movieLabel.setText(movie_details)     

        if movie_data['poster'] != 'N/A' and movie_data['poster'] is not None:
            data = requests.get(movie_data['poster']).content
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            self.posterLabel.setPixmap(pixmap)
        else:
            self.posterLabel.clear()
    
    