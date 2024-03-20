# # TaskModel.py
# from PyQt6.QtCore import Qt, QModelIndex
# from PyQt6.QtGui import QStandardItemModel, QStandardItem
# from PyQt6.QtCore import QAbstractListModel
# import requests



# class TodoModel(QAbstractListModel):
#     def __init__(self, todos=None):
#         super().__init__()
#         self.todos = todos or []

#     def data(self, index, role):
#         if role == Qt.ItemDataRole.DisplayRole:
#             _, text = self.todos[index.row()]
#             return text
#         if role == Qt.ItemDataRole.CheckStateRole:
#             status, _ = self.todos[index.row()]
#             return Qt.CheckState.Checked if status else Qt.CheckState.Unchecked

#     def rowCount(self, index):
#         return len(self.todos)

#     def insertRows(self, position, rows, index = QModelIndex()):
#         self.beginInsertRows(index, position, position + rows - 1)
#         for _ in range(rows):
#             self.todos.insert(position, (False, ""))
#         self.endInsertRows()
#         return True

#     def removeRows(self, position, rows, index = QModelIndex()):
#         self.beginRemoveRows(index, position, position + rows - 1)
#         for _ in range(rows):
#             del self.todos[position]
#         self.endRemoveRows()
#         return True


# TaskModel.py
from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import QAbstractListModel
import requests

class TodoModel(QAbstractListModel):
    def __init__(self, todos=None):
        super().__init__()
        self.todos = todos or []

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            _, text = self.todos[index.row()]
            return text
        if role == Qt.ItemDataRole.CheckStateRole:
            status, _ = self.todos[index.row()]
            return Qt.CheckState.Checked if status else Qt.CheckState.Unchecked

    def rowCount(self, index):
        return len(self.todos)

    def insertRows(self, position, rows, index=QModelIndex()):
        self.beginInsertRows(index, position, position + rows - 1)
        for _ in range(rows):
            self.todos.insert(position, (False, ""))
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, index=QModelIndex()):
        self.beginRemoveRows(index, position, position + rows - 1)
        for _ in range(rows):
            del self.todos[position]
        self.endRemoveRows()
        return True

    def fetchMovieData(self, movie_name):
        movie_response = requests.get('https://localhost:7276/Movie/' + movie_name, headers={'accept': 'application/json'}, verify=False)
        print(f"Response status code: {movie_response.status_code}")  # Print the status code

        if movie_response.status_code == 200:  # Check if the request was successful
            return movie_response.json()
        else:
            print(f"Error: {movie_response.text}")  # Print the error message
            return None