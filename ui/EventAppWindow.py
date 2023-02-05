from PySide6.QtWidgets import QWidget
from PySide6 import QtWidgets, QtCore

from ui.SceneWindow import SceneWindow


class EventAppWindow(QWidget):
    "Overriding base class with event methods"

    def __init__(self,
                 store
                 ):
        super().__init__()

        self.glWidget = SceneWindow(store)

        glLayout = QtWidgets.QVBoxLayout()
        glLayout.addWidget(self.glWidget)
        self.setLayout(glLayout)


    def moveGLCamera(self, direction: str):
        self.glWidget.moveCamera(direction)

    def moveCameraForward(self):
        self.moveGLCamera("forward")

    def moveCameraBackward(self):
        self.moveGLCamera("backward")

    def moveCameraLeft(self):
        self.moveGLCamera("left")

    def moveCameraRight(self):
        self.moveGLCamera("right")

    def moveCameraUp(self):
        self.moveGLCamera("up")

    def moveCameraDown(self):
        self.moveGLCamera("down")


    def mousePressEvent(self, event):
        self.mousePosition = event.pos()

    def mouseMoveEvent(self, event):
        currentPosition = event.pos()
        if event.buttons() == QtCore.Qt.RightButton:
            if currentPosition.x() < self.mousePosition.x():
                self.moveCameraLeft()
            elif currentPosition.x() > self.mousePosition.x():
                self.moveCameraRight()
            if currentPosition.y() < self.mousePosition.y():
                self.moveCameraDown()
            elif currentPosition.y() > self.mousePosition.y():
                self.moveCameraUp()
        elif event.buttons() == QtCore.Qt.LeftButton:
            print("left")
        
        self.mousePosition = currentPosition
        return super().mouseMoveEvent(event)

    def wheelEvent(self, event):
        if event.pixelDelta().y() < 0:
            self.moveCameraForward()
        elif event.pixelDelta().y() > 0:
            self.moveCameraBackward()

