from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem

class HierarchyWindow(QWidget):

    def __init__(self, store):
        super(HierarchyWindow, self).__init__()
        self.store = store
        self.store.changed.connect(self.renderList)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Hierarchy"))

        self.list = QListWidget()
        self.renderList()

        self.list.itemClicked.connect( self.itemClicked )

        layout.addWidget(self.list)
        self.setLayout(layout)


    def renderList(self):
        self.list.clear()
        for i, model in enumerate(self.store.models):
            item = QListWidgetItem(model.name)
            item.setData(1, model.id)
            self.list.addItem(item)
            if self.store.currentSelection != None and self.store.currentSelection == model.id:
                self.list.setCurrentItem(item)
        
    def itemClicked(self, item: QListWidgetItem):
        id = item.data(1)
        if id != self.store.currentSelection:
            self.store.setCurrentSelection(id)

