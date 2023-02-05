from model import (Cube, Sphere)

from PySide6.QtCore import QObject, Signal

class Store(QObject):

    models = []
    id = 0
    modelDict = {}

    currentSelection = None

    changed = Signal()
    selectionChanged = Signal()

    def __init__(self):
        super(Store, self).__init__()

    
    def addCube(self):
        self.id += 1
        model = Cube(self.id)
        self.models.append(model)
        self.modelDict[self.id] = model
        self.changed.emit()


    def addSphere(self):
        self.id += 1
        model = Sphere(self.id)
        self.models.append(model)
        self.modelDict[self.id] = model
        self.changed.emit()

    def remove(self):
        if self.currentSelection != None:
            item = self.getModelById(self.currentSelection)
            self.models.remove(item)
            del self.modelDict[self.currentSelection]
            self.currentSelection = None
            self.changed.emit()

    def setCurrentSelection(self, current):
        self.currentSelection = current
        self.selectionChanged.emit()

    def emitChange(self):
        self.changed.emit()


    def getModelById(self, id):
        return self.modelDict[id]



