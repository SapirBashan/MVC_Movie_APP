
# Movie Manager Application

This Movie Manager application is designed to help users manage their movie collection by integrating with external APIs for movie data retrieval and leveraging AI capabilities for generating movie recommendations. The backend of the application is powered by a C# server that consolidates HTTP requests for all APIs into one place, providing a seamless experience for users.


https://github.com/SapirBashan/PyQt_frontend_Movie_APP/assets/99900812/7f7a8038-b390-4048-86f2-5485834bee5f

##Link to the backend C# server
https://github.com/SapirBashan/Server_Movie_App_API/tree/master

![image](https://github.com/SapirBashan/PyQt_frontend_Movie_APP/assets/99900812/75e5c394-73bc-4a2a-974a-c1e3849f5d68)


## Features

- **CRUD Operations**: Perform Create, Read, Update, and Delete operations on movies.
- **Integration with External APIs**: Utilize OMDB API for fetching movie data and OpenAI API for generating movie recommendations.
- **MongoDB Integration**: Store movie information using MongoDB for efficient data management.
- **MVC Architecture**: The application is structured using the Model-View-Controller (MVC) design pattern for a clear separation of concerns.

...

## Installation

1. Clone the repository to your local machine.
2. Install the required Python packages using `pip install -r requirements.txt`.
3. Ensure MongoDB is installed and running locally.
4. Run the backend C# .NET Core API following the instructions in the `Movie_Fetch_API` folder.
5. Start the PyQt frontend application by running `python main.py`.

## Usage

### Model (TodoModel.py)

```python
import requests

class TodoModel:
    def __init__(self):
        pass
    
    # POST request to add a movie
    def addMovie(self, movie_data):
        formatted_data = {
            "title": movie_data['title'],
            "year": movie_data['year'],
            "imdbID": movie_data['imdbID'],
            "rated": movie_data['rated'],
            "type": movie_data['type'],
            "poster": movie_data['poster'],
            "plot": movie_data['plot'],
            "imdbRating": movie_data['imdbRating']
        }
        response = requests.post(f'https://localhost:7276/api/MovieValue', json=formatted_data, verify=False)
        return response.status_code == 201
    
    # DELETE request to remove a movie
    def removeMovie(self, movie_name):
        response = requests.delete(f'https://localhost:7276/api/MovieValue/{movie_name}', verify=False)
        return response.status_code == 200

    # GET request to fetch movie data from the OMDB API
    def fetchMovieData(self, movie_name):
        response = requests.get(f'https://localhost:7276/Omdb/{movie_name}', verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            return None
```

### View (TaskView.py)

```python
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QGridLayout, QScrollArea, QSizePolicy, QApplication, QHBoxLayout
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt

class TodoView(QMainWindow):
    def __init__(self):
        super().__init__()
        # View initialization code
```

### Controller (TodoController.py)

```python
class TodoController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    # Controller method to add a movie
    def addMovieController(self, movie_data):
        if self.model.addMovie(movie_data):
            self.view.updateMovieList()  # Update the movie list in the view
            return True

    # Other controller methods omitted for brevity
```

## Development Setup

1. Ensure Python and .NET Core SDK are installed on your machine.
2. Install required Python packages using `pip install -r requirements.txt`.
3. Install MongoDB and start the MongoDB server.
4. Clone the backend C# .NET Core API and follow the setup instructions.
5. Start the PyQt frontend application using `python main.py`.
6. Start testing and developing new features!

## Contributors
- [Sapir Bashan](https://github.com/SapirBashan)
- [Noam Benisho](https://github.com/noambenisho)

