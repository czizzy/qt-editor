from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QTreeWidget, QTreeWidgetItem

class HierarchyWindow(QWidget):

    def __init__(self, store):
        super(HierarchyWindow, self).__init__()
        self.store = store
        self.store.changed.connect(self.renderTree)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Hierarchy"))

        self.list = QListWidget()
        self.tree = QTreeWidget()
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(["Name"])
        self.renderTree()


        self.tree.itemClicked.connect( self.itemClicked )

        layout.addWidget(self.tree)
        self.setLayout(layout)
    
    def renderTree(self):
        self.tree.clear()
        currentItem = None
        root = QTreeWidgetItem(["Scene"])
        for i, model in enumerate(self.store.models):
            item = QTreeWidgetItem([model.name])

            item.setData(1, 1, model.id)
            root.addChild(item)
            subCurrent = self.renderTreeItem(item, model.children)
            if subCurrent != None:
                currentItem = subCurrent
            if self.store.currentSelection != None and self.store.currentSelection == model.id:
                currentItem = item
        self.tree.insertTopLevelItem(0, root)
        self.tree.expandAll()
        if currentItem != None:
            self.tree.setCurrentItem(currentItem)

    def renderTreeItem(self, parent, children):
        currentItem = None
        for i, model in enumerate(children):
            item = QTreeWidgetItem([model.name])

            item.setData(1, 1, model.id)
            parent.addChild(item)
            subCurrentItem = self.renderTreeItem(item, model.children)
            if subCurrentItem != None:
                currentItem = subCurrentItem
            if subCurrentItem == None and self.store.currentSelection != None and self.store.currentSelection == model.id:
                currentItem = item
        return currentItem
        
    def itemClicked(self, item: QTreeWidgetItem):
        id = item.data(1, 1)
        if id != self.store.currentSelection:
            self.store.setCurrentSelection(id)

