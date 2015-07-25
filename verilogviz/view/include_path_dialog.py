import sys
import os
import logging

from PyQt4.Qt import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class IncludePathDialog(QDialog):

    def __init__(self, parent = None):
        super (IncludePathDialog, self).__init__(parent)
        self.logger = logging.getLogger("verilogviz")
        layout = QVBoxLayout()

        path_layout = QHBoxLayout()
        self.path_tree_view = QTreeView()
        self.set_dir_path_model()
        self.path_tree_view.clicked.connect(self.path_tree_clicked)

        add_remove_button_layout = QVBoxLayout()
        self.add_button = QPushButton("+")
        self.add_button.setEnabled(False)
        self.add_button.clicked.connect(self.add_button_clicked)

        self.remove_button = QPushButton("-")
        self.remove_button.setEnabled(False)
        self.remove_button.clicked.connect(self.remove_button_clicked)

        self.clear_button = QPushButton("Clear")
        self.clear_button.setEnabled(False)
        self.clear_button.clicked.connect(self.clear_button_clicked)

        add_remove_button_layout.addWidget(self.add_button)
        add_remove_button_layout.addWidget(self.remove_button)
        add_remove_button_layout.addWidget(self.clear_button)

        self.include_dir_list = QListWidget()
        self.include_dir_list.currentRowChanged.connect(self.path_item_changed)

        self.priority_layout = QVBoxLayout()
        self.up_button = QPushButton("Move Up")
        self.up_button.setEnabled(False)
        self.down_button = QPushButton("Move Down")
        self.down_button.setEnabled(False)
        self.priority_layout.addWidget(self.up_button)
        self.priority_layout.addWidget(self.down_button)

        path_layout.addWidget(self.path_tree_view)
        path_layout.addLayout(add_remove_button_layout)
        path_layout.addWidget(self.include_dir_list)
        path_layout.addLayout(self.priority_layout)


        ok_button = QPushButton("OK")
        #ok_button.clicked.connect(self.accepted)
        #ok_button.clicked.connect(self.finished)
        ok_button.clicked.connect(self.ok_button_clicked)
        cancel_button = QPushButton("Cancel")
        #cancel_button.clicked.connect(self.rejected)
        #cancel_button.clicked.connect(self.finished)
        cancel_button.clicked.connect(self.cancel_button_clicked)

        layout.addLayout(path_layout)
        layout.addWidget(ok_button)
        layout.addWidget(cancel_button)

        self.setLayout(layout)
        self.path = os.path.curdir
        self.logger.debug("Initial Path: %s" % self.path)

    def set_dir_path_model(self):
        file_model = QFileSystemModel()
        user_path = os.path.expanduser("~")
        file_model.setRootPath(user_path)
        self.path_tree_view.setModel(file_model)

    def set_start_path(self, path):
        self.logger.debug("Start Path: %s" % path)
        index = self.path_tree_view.model().index(path)
        self.path_tree_view.setCurrentIndex(index)

    def set_path_list(self, include_paths):
        self.include_dir_list.clear()
        self.include_dir_list.addItems(include_paths)

    def get_path_list(self):
        paths = []
        for index in xrange(self.include_dir_list.count()):
            item = self.include_dir_list.item(index)
            paths.append(str(item.text()))
        return paths

    def get_start_path(self):
        index = self.path_tree_view.currentIndex()
        path = self.path_tree_view.model().filePath(index)
        self.logger.info("Setting new path: %s" % str(path))
        return path

    def ok_button_clicked(self):
        self.setResult(QDialog.Accepted)
        self.accepted.emit()
        self.finished.emit(QDialog.Accepted)
        #self.close()
        self.done(QDialog.Accepted)

    def cancel_button_clicked(self):
        self.setResult(QDialog.Rejected)
        self.rejected.emit()
        self.finished.emit(QDialog.Rejected)
        #self.close()
        self.done(QDialog.Rejected)

    def path_tree_clicked(self):
        index = self.path_tree_view.currentIndex()
        path = str(self.path_tree_view.model().filePath(index))
        if os.path.isdir(path):
            self.logger.debug("Enable Add")
            self.add_button.setEnabled(True)
        else:
            self.logger.debug("Not a Path")
            self.add_button.setEnabled(False)

    def path_item_changed(self, index):
        if index == None:
            self.remove_button.setEnabled(False)
            self.up_button.setEnabled(False)
            self.down_button.setEnabled(False)
            return


        if self.include_dir_list.count() == 0:
            self.remove_button.setEnabled(False)
            return

        self.remove_button.setEnabled(True)

        if self.include_dir_list.count() <= 1:
            self.up_button.setEnabled(False)
            self.down_button.setEnabled(False)
            return

        if index == 0: 
            self.up_button.setEnabled(False)
            self.down_button.setEnabled(True)

        elif index == self.include_dir_list.count() - 1:
            self.up_button.setEnabled(True)
            self.down_button.setEnabled(False)

        else:
            self.up_button.setEnabled(True)
            self.down_button.setEnabled(True)


    def add_button_clicked(self):
        index = self.path_tree_view.currentIndex()
        path = str(self.path_tree_view.model().filePath(index))
        self.logger.info("Adding path: %s" % path)
        self.include_dir_list.addItem(path)
        self.include_dir_list.update()

    def remove_button_clicked(self):
        self.logger.info("Remove")
        index = self.include_dir_list.currentRow()
        item = self.include_dir_list.takeItem(index)
        self.logger.info("removed: %s" % str(item.text()))
        index = self.include_dir_list.currentRow()
        self.path_item_changed(index)

    def clear_button_clicked(self):
        self.logger.info("Cleared")

