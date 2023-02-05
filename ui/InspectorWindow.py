from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QColorDialog, QLineEdit, QDoubleSpinBox, QSizePolicy, QPushButton
from PySide6.QtCore import Qt


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
                print(self.form)
                while self.formLayout.count():
                    item = self.formLayout.takeAt(0)
                    item.widget().deleteLater()
                self.form.destroy()
            self.model = self.store.getModelById(self.store.currentSelection)

            self.layout.removeWidget(self.form)
            self.form = QWidget()
            self.formLayout = QVBoxLayout()
            self.form.setLayout(self.formLayout)
            self.nameInput = QLineEdit()
            self.nameInput.setPlaceholderText("Enter the name")
            self.nameInput.editingFinished.connect(self.nameEdited)
            self.nameInput.setText(self.model.name)
            self.formLayout.addWidget(QLabel("name:"))
            self.formLayout.addWidget(self.nameInput)

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

            self.formLayout.addWidget(QLabel("position:"), 0, Qt.AlignTop)
            self.formLayout.addWidget(positions, 0, Qt.AlignTop)


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

            self.formLayout.addWidget(QLabel("rotation:"))
            self.formLayout.addWidget(rotations)
            self.formLayout.setAlignment(Qt.AlignTop)

            colorButton = QPushButton("Select color")
            colorButton.clicked.connect(self.colorClicked)
            self.formLayout.addWidget(colorButton)


            if self.model.type == "cube":
                sizeXInput = QDoubleSpinBox()
                sizeXInput.valueChanged.connect(self.widthChanged)
                sizeXInput.setSingleStep(0.1)
                sizeXInput.setRange(0, 10)
                sizeXInput.setValue(self.model.width)
                sizeYInput = QDoubleSpinBox()
                sizeYInput.valueChanged.connect(self.heightChanged)
                sizeYInput.setSingleStep(0.1)
                sizeYInput.setRange(0, 10)
                sizeYInput.setValue(self.model.height)
                sizeZInput = QDoubleSpinBox()
                sizeZInput.valueChanged.connect(self.lengthChanged)
                sizeZInput.setSingleStep(0.1)
                sizeZInput.setRange(0, 10)
                sizeZInput.setValue(self.model.length)

                sizes = QWidget()
                sizesLayout = QHBoxLayout()
                sizes.setLayout(sizesLayout)
                sizesLayout.addWidget(sizeXInput)
                sizesLayout.addWidget(sizeYInput)
                sizesLayout.addWidget(sizeZInput)
                self.formLayout.addWidget(QLabel("size:"))
                self.formLayout.addWidget(sizes)

            else:
                radiusInput = QDoubleSpinBox()
                radiusInput.valueChanged.connect(self.radiusChanged)
                radiusInput.setSingleStep(0.1)
                radiusInput.setRange(0, 10)
                radiusInput.setValue(self.model.radius)

                self.formLayout.addWidget(QLabel("radius:"))
                self.formLayout.addWidget(radiusInput)

            self.layout.addWidget(self.form)

    def colorClicked(self):
        color = QColorDialog.getColor().getRgbF()
        self.model.setColor(color[0], color[1], color[2], color[3])
        self.store.emitChange()


    def nameEdited(self):
        self.model.setName(self.nameInput.text())
        self.store.emitChange()

    def widthChanged(self, value):
        self.model.setWidth(value)
        self.store.emitChange()

    def heightChanged(self, value):
        self.model.setHeight(value)
        self.store.emitChange()

    def lengthChanged(self, value):
        self.model.setLength(value)
        self.store.emitChange()

    def radiusChanged(self, value):
        self.model.setRadius(value)
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
