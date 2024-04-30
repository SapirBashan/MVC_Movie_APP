# main.py
import sys
from PyQt6.QtWidgets import QApplication
from TaskController import TodoController
from TaskModel import TodoModel
from TaskView import TodoView

def main():
    app = QApplication(sys.argv)
    model = TodoModel()
    view = TodoView()
    controller = TodoController(model, view)
    view.setController(controller)  # Set the controller before showing the view
    view.show()
    controller.GetAllMoviesController()  # Fetch all movies after showing the view
    sys.exit(app.exec())

if __name__ == "__main__":
    main()