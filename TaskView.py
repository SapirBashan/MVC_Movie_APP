from PyQt6.QtWidgets import QMainWindow, QTabWidget, QApplication, QWidget, QVBoxLayout
#######################################################################################
import qdarkstyle

from ListView import TodoView
from ChatView import ChatView

app = QApplication([])
############################################################################################
app.setStyleSheet(qdarkstyle.load_stylesheet())

class TaskView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager")

        self.tabWidget = QTabWidget()

        # Initialize TodoView and set it as the layout for tab1
        self.tab1 = QWidget()
        self.todoView = TodoView()
        self.tab1.setLayout(QVBoxLayout())
        self.tab1.layout().addWidget(self.todoView)
        self.tabWidget.addTab(self.tab1, "Watch list")

        # Initialize ChatView and set it as the layout for tab2
        self.tab2 = QWidget()
        self.chatView = ChatView()
        self.tab2.setLayout(QVBoxLayout())
        self.tab2.layout().addWidget(self.chatView)
        self.tabWidget.addTab(self.tab2, "Chat")

        self.setCentralWidget(self.tabWidget)

        self.controller = None

    def setController(self, controller):
        self.controller = controller
        self.todoView.setController(controller)
        self.chatView.setController(controller)  # set controller for ChatView


    def show(self):
        self.showMaximized()