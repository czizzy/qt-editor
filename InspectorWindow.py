from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QListWidgetItem, QLineEdit, QDoubleSpinBox, QSizePolicy
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import QSize


class InspectorWindow(QWidget):
    form = None

    def __init__(self, store):
        super(InspectorWindow, self).__init__()
        self.store = store
        self.store.selectionChanged.connect(self.render)

        self.layout = QVBoxLayout()
        label = QLabel("Inspector")
        labelSizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        labelSizePolicy1.setHorizontalStretch(0)
        labelSizePolicy1.setVerticalStretch(1)
        label.setSizePolicy(labelSizePolicy1)
        # label.setMinimumSize(QSize(200, 0))
        # label.setMaximumSize(QSize(300, 16777215))

        self.layout.addWidget(label)

        self.setLayout(self.layout)

    def render(self):
        if self.store.currentSelection != None:
            if self.form != None:
                self.form.destroy()
            self.model = self.store.getModelById(self.store.currentSelection)

            self.layout.removeWidget(self.form)
            self.form = QWidget()
            formLayout = QVBoxLayout()
            self.form.setLayout(formLayout)
            self.nameInput = QLineEdit()
            self.nameInput.setPlaceholderText("Enter the name")
            self.nameInput.editingFinished.connect(self.nameEdited)
            self.nameInput.setText(self.model.name)
            formLayout.addWidget(QLabel("name:"))
            formLayout.addWidget(self.nameInput)

            positionXInput = QDoubleSpinBox()
            positionXInput.valueChanged.connect(self.positionXchanged)
            positionXInput.setSingleStep(0.01)
            positionXInput.setRange(-100, 100)
            positionXInput.setValue(self.model.position.x())
            positionYInput = QDoubleSpinBox()
            positionYInput.valueChanged.connect(self.positionYchanged)
            positionYInput.setSingleStep(0.01)
            positionYInput.setRange(-100, 100)
            positionYInput.setValue(self.model.position.y())
            positionZInput = QDoubleSpinBox()
            positionZInput.valueChanged.connect(self.positionZchanged)
            positionZInput.setSingleStep(0.01)
            positionZInput.setRange(-100, 100)
            positionZInput.setValue(self.model.position.z())

            positions = QWidget()
            positionsLayout = QHBoxLayout()
            positions.setLayout(positionsLayout)
            positionsLayout.addWidget(positionXInput)
            positionsLayout.addWidget(positionYInput)
            positionsLayout.addWidget(positionZInput)

            formLayout.addWidget(QLabel("position:"))
            formLayout.addWidget(positions)


            rotationXInput = QDoubleSpinBox()
            rotationXInput.valueChanged.connect(self.rotationXchanged)
            rotationXInput.setSingleStep(0.01)
            rotationXInput.setRange(-1, 1)
            rotationXInput.setValue(self.model.quaternion.x())
            rotationYInput = QDoubleSpinBox()
            rotationYInput.valueChanged.connect(self.rotationYchanged)
            rotationYInput.setSingleStep(0.01)
            rotationYInput.setRange(-1, 1)
            rotationYInput.setValue(self.model.quaternion.y())
            rotationZInput = QDoubleSpinBox()
            rotationZInput.valueChanged.connect(self.rotationZchanged)
            rotationZInput.setSingleStep(0.01)
            rotationZInput.setRange(-1, 1)
            rotationZInput.setValue(self.model.quaternion.z())
            rotationWInput = QDoubleSpinBox()
            rotationWInput.valueChanged.connect(self.rotationWchanged)
            rotationWInput.setSingleStep(0.01)
            rotationWInput.setRange(-1, 1)
            rotationWInput.setValue(self.model.quaternion.scalar())

            rotations = QWidget()
            rotationsLayout = QHBoxLayout()
            rotations.setLayout(rotationsLayout)
            rotationsLayout.addWidget(rotationXInput)
            rotationsLayout.addWidget(rotationYInput)
            rotationsLayout.addWidget(rotationZInput)
            rotationsLayout.addWidget(rotationWInput)

            formLayout.addWidget(QLabel("rotation:"))
            formLayout.addWidget(rotations)

            self.layout.addWidget(self.form)



    def nameEdited(self):
        self.model.setName(self.nameInput.text())
        self.store.emitChange()

    def positionXchanged(self, value):
        self.model.setPositionX(value)
        self.store.emitChange()

    def positionYchanged(self, value):
        self.model.setPositionY(value)
        self.store.emitChange()

    def positionZchanged(self, value):
        self.model.setPositionZ(value)
        self.store.emitChange()

    def rotationXchanged(self, value):
        self.model.setQuaternionX(value)
        self.store.emitChange()

    def rotationYchanged(self, value):
        self.model.setQuaternionY(value)
        self.store.emitChange()

    def rotationZchanged(self, value):
        self.model.setQuaternionZ(value)
        self.store.emitChange()

    def rotationWchanged(self, value):
        self.model.setQuaternionW(value)
        self.store.emitChange()
