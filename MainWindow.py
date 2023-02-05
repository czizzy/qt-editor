from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QVBoxLayout
from PySide6.QtCore import QSize
from HierarchyWindow import HierarchyWindow
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QMenuBar,
    QSizePolicy, QStatusBar, QWidget)
from EventAppWindow import EventAppWindow

from PySide6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QToolBar, QStatusBar
)
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt
from InspectorWindow import InspectorWindow

from store import Store

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("QT Editor")
        self.setMinimumSize(QSize(800, 600))

        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)

        button_action = QAction("Add Cube", self)
        button_action.setStatusTip("Add new Cube")
        button_action.triggered.connect(self.onNewCubeClick)
        toolbar.addAction(button_action)

        button_action2 = QAction("Add Sphere", self)
        button_action2.setStatusTip("Add new Sphere")
        button_action2.triggered.connect(self.onNewSphereClick)
        toolbar.addAction(button_action2)

        delete_action = QAction("Remove", self)
        delete_action.setStatusTip("Remove Current Selection")
        delete_action.triggered.connect(self.onDeleteClick)
        toolbar.addAction(delete_action)

        self.store = Store()

        widget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(EventAppWindow(self.store))

        sideWidget = QWidget()
        sideLayout = QVBoxLayout()
        hierarchy = HierarchyWindow(self.store)

        hierarchySizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        hierarchySizePolicy1.setHorizontalStretch(0)
        hierarchySizePolicy1.setVerticalStretch(1)
        hierarchy.setSizePolicy(hierarchySizePolicy1)
        hierarchy.setMinimumSize(QSize(200, 0))
        hierarchy.setMaximumSize(QSize(300, 16777215))

        sideLayout.addWidget(hierarchy)
        sideLayout.addWidget(InspectorWindow(self.store))
        sideWidget.setLayout(sideLayout)

        sideSizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sideSizePolicy.setHorizontalStretch(1)
        sideSizePolicy.setVerticalStretch(0)
        sideWidget.setSizePolicy(sideSizePolicy)
        sideWidget.setMinimumSize(QSize(200, 0))
        sideWidget.setMaximumSize(QSize(300, 16777215))
        layout.addWidget(sideWidget)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    
    def onNewCubeClick(self):
        self.store.addCube()

    def onNewSphereClick(self):
        self.store.addSphere()

    def onDeleteClick(self):
        self.store.remove()
