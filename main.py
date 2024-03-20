# main.py

import sys
from PyQt6.QtWidgets import QApplication
from TaskController import TodoController
from TaskModel import TodoModel
from TaskView import TodoView
import requests

#this is a check for real

def main():
    
    app = QApplication(sys.argv)
    model = TodoModel()
    view = TodoView()
    controller = TodoController(model, view)

    view.show()
      
    sys.exit(app.exec())
   


if __name__ == "__main__":
    main()
