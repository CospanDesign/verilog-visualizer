import sys
import os
import logging

from PyQt4.Qt import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class IncludePathDialog(QDialog):



    def __init__(self, parent):
        super IncludePathDialog(self).__init__(parent)
        self.logger = logging.getLogger("verilogviz")
        layout = QVBoxLayout()

        path_layout = QHBoxLayout()
        self.tree_view = QLabel("HI")
        add_remove_button_layout = QVBoxLayout()
        self.add_button = QPushButton("+")
        self.remove_button = QPushButton("-")
        self.clear_button = QPushButton("Clear")

        add_remove_button_layout.addWidget(self.add_button)
        add_remove_button_layout.addWidget(self.remove_button)
        add_remove_button_layout.addWidget(self.clear_button)

        self.include_dir_list = QListView()

        self.priority_layout = QVerticalLayout()
        self.up_button = QPushButton("Move Up")
        self.up_button.setEnabled(False)
        self.down_button = QPushButton("Move Down")
        self.down_button.setEnabled(False)
        self.priority_layout.addWidget(self.up_button)
        self.priority_layout.addWidget(self.down_button)

        path_layout.addWidget(tree_view)
        path_layout.addLayout(add_remove_button_layout)
        path_layout.addWidget(include_dir_list)
        path_layout.addLayout(priority_layout)

        layout.addLayout(path_layout)
        self.setLayout(layout)
        self.include_paths = []
        self.path = os.path.curdir()
        self.logger.debug("Initial Path: %s" % self.path)

    def set_start_path(self, path):
        self.path = path

    def set_path_list(self, include_paths):
        self.include_paths = include_paths

    def get_path_list(self):
        return self.include_paths

        
