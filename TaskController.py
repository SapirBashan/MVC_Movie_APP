
# TaskController.py

from PyQt6.QtCore import Qt
import logging

class TodoController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.setController(self)
        logging.basicConfig(level=logging.INFO)

    def addTodo(self, text):
        self.model.insertRows(len(self.model.todos), 1)
        self.model.todos[-1] = (False, text)
        self.model.dataChanged.emit(self.model.index(len(self.model.todos) - 1), self.model.index(len(self.model.todos) - 1))
        self.printTodos()

    def deleteTodo(self, index):
        todo = self.model.todos[index.row()]
        self.model.removeRows(index.row(), 1)

    def printTodos(self):
        for i, todo in enumerate(self.model.todos):
            status, text = todo
            status_str = 'Done' if status else 'Not done'

    def completeTodo(self, index):
        row = index.row()
        _, text = self.model.todos[row]
        self.model.todos[row] = (True, text)
        # Emit signal to notify view about the data change
        self.model.dataChanged.emit(index, index)
        self.printTodos()

    def updateView(self):
        # Set the model for the QListView
        self.view.todoList.setModel(self.model)
        
    def searchMovieController(self, movie_name):
        return self.model.fetchMovieData(movie_name)
    
    