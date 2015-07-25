from PyQt4.Qt import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class ModuleListModel(QAbstractListModel):

    def __init__(self, parent = None):
        super (ModuleListModel, self).__init__(parent)
        self.modules = []

    def rowCount(self, parent):
        return len(self.modules)

    def data(self, index, role = Qt.DisplayRole):
        data = self.modules[index.row()]
        if role != Qt.DisplayRole:
            return QVariant()

        return QVariant(data["module"])

    def flags(self, index):
        f = super (ModuleListModel, self).flags(index)
        return f

    def headerData(self, sections, orientation):
        if orientation == Qt.Vertical:
            return QVariant()
        else:
            return QVariant(QString("Project Name"))

    def removeRows(self, row, count, parent = None):
        self.beginRemoveRows()
        del(self.module[row])
        self.endRemoveRows()
        return True

    def addItem(self, item):
        index = self.createIndex(0, 0)

        self.beginInsertRows(index, len(self.modules), len(self.modules))
        self.modules.append(item)
        self.endInsertRows()

    def remove_module_by_name(self, name):
        module = self.get_module_by_name(name)
        row = self.modules.index(module)
        self.removeRows(row, 1)

    def get_module_by_name(self, name):
        if not in_list(name):
            raise LookupError("Module: %s is not in list" % name)

        for module in self.modules:
            if str(name).lower() == str(module["module"]).lower():
                return module
            

    def get_module_tags(index):
        return self.modules(index)

    def in_list(self, name):
        for module in self.modules:
            if str(name).lower() == str(module["module"]).lower():
                return True
        return False
