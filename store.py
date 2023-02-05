import json

from model import (Cube, Sphere)

from PySide6.QtCore import QObject, Signal
from PySide6.QtCore import QSettings
from PySide6.QtGui import QMatrix4x4, QQuaternion, QVector4D, QVector3D

class Store(QObject):

    models = []
    id = 0
    modelDict = {}

    currentSelection = None

    changed = Signal()
    selectionChanged = Signal()

    def __init__(self):
        super(Store, self).__init__()
        qsettings = QSettings()
        data = json.loads(qsettings.value("data"))
        for i, item in enumerate(data):
            if item["type"] == "cube":
                model = self.addCube()
                model.setName(item["name"])
                model.setColor(item["color"][0], item["color"][1], item["color"][2], item["color"][3])
                model.setPosition(item["position"][0], item["position"][1], item["position"][2])
                model.setQuaternion(item["rotation"][0], item["rotation"][1], item["rotation"][2], item["rotation"][3])
                model.setWidth(item["width"])
                model.setHeight(item["height"])
                model.setLength(item["length"])

            if item["type"] == "sphere":
                model = self.addSphere()
                model.setName(item["name"])
                model.setColor(item["color"][0], item["color"][1], item["color"][2], item["color"][3])
                model.setPosition(item["position"][0], item["position"][1], item["position"][2])
                model.setQuaternion(item["rotation"][0], item["rotation"][1], item["rotation"][2], item["rotation"][3])
                model.setRadius(item["radius"])
            
            self.emitChange()


    def addCube(self):
        self.id += 1
        model = Cube(self.id)
        self.models.append(model)
        self.modelDict[self.id] = model
        self.emitChange()
        return model


    def addSphere(self):
        self.id += 1
        model = Sphere(self.id)
        self.models.append(model)
        self.modelDict[self.id] = model
        self.emitChange()
        return model

    def remove(self):
        if self.currentSelection != None:
            item = self.getModelById(self.currentSelection)
            self.models.remove(item)
            del self.modelDict[self.currentSelection]
            self.currentSelection = None
            self.emitChange()

    def setCurrentSelection(self, current):
        self.currentSelection = current
        self.selectionChanged.emit()

    def getData(self):
        data = []
        for i, model in enumerate(self.models):
          data.append(model.value())
        return json.dumps(data)

    def emitChange(self):
        self.changed.emit()
        qsettings = QSettings()
        qsettings.setValue("data", self.getData())


    def getModelById(self, id):
        return self.modelDict[id]



