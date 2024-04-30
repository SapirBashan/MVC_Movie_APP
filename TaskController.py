from PyQt6.QtCore import QStringListModel  # Import QStringListModel

class TodoController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def addMovieController(self, movie_data):
        #if the movie is added successfully, update the movie list
        if self.model.addMovie(movie_data):
            self.GetAllMoviesController()
            return True
        

    def removeMovieController(self, movie_name):
        #if the movie is removed successfully, update the movie list
        if self.model.removeMovie(movie_name):
            self.GetAllMoviesController()
            return True
        

    def searchMovieController(self, movie_name):
        return self.model.fetchMovieData(movie_name)
    
    def GetAllMoviesController(self):
        movies_data = self.model.GetAllMovies()
        if movies_data:
            movie_titles = [movie['title'] for movie in movies_data]
            self.view.updateMovieList(movie_titles)