import sys
import os
import logging

from PyQt4.Qt import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from graph.verilog_graph import VerilogGraph


FORMAT = '%(asctime)-15s %(message)s'

VERILOG_EXTENSIONS = ["v"]
VERILOG_NAME_EXTENSION = [("Verilog (*.v)")]


def is_verilog_file(path):
    if not os.path.isfile(str(path)):
        return False
    fname, ext = os.path.splitext(path)
    ext = ext.strip(".")
    return ext in VERILOG_EXTENSIONS

class MainForm (QMainWindow):

    def __init__(self, app, actions):
        super (MainForm, self).__init__()
        self.settings = QSettings("Cospan Design", "verilog-visualizer")
        self.actions = actions
        self.logger = logging.getLogger("verilogviz")
        self.setWindowTitle("Verilog Visualizer")
        self.show()

        ## Actions
        exit_action = QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(quit)

        save_action = QAction("&Save", self)
        save_action.setShortcut('Ctrl+S')

        open_action = QAction("&Open", self)
        open_action.setShortcut('Ctrl+O')

        demo_action = QAction("&Demo", self)
        demo_action.setShortcut('Ctrl+D')

        save_action.triggered.connect(self.save_clicked)
        open_action.triggered.connect(self.open_clicked)
        demo_action.triggered.connect(self.demo_action)

        #Toolbar
        self.toolbar = self.addToolBar("main")
        self.toolbar.addAction(exit_action)
        self.toolbar.addAction(demo_action)

        #Menubar
        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(exit_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)

        #Custom Views
        self.verilog_graph = VerilogGraph(app, self.actions)

        #self.user_path = "."
        self.user_path = os.path.expanduser("~")
        if self.settings.contains("prev_dir"):
            self.user_path = self.settings.value("prev_dir", type=str)
            self.logger.info("Loading previous path: %s" % self.user_path)

        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(self.user_path)
        index = self.file_model.index(self.user_path)
        self.file_model.setNameFilters(VERILOG_EXTENSIONS)
        self.file_model.setNameFilterDisables(False)
        self.file_view = QTreeView()
        self.file_view.setModel(self.file_model)
        self.file_view.setCurrentIndex(index)

        self.file_view.clicked.connect(self.tree_clicked)
        self.file_model.directoryLoaded.connect(self.tree_directory_loaded)

        self.main_splitter = QSplitter(Qt.Horizontal)
        self.main_splitter.addWidget(self.file_view)
        self.main_splitter.addWidget(self.verilog_graph)

        self.setCentralWidget(self.main_splitter)

        self.show()
        self.logger.debug("Showing")

    def save_clicked(self):
        self.logger.debug("Save Clicked")

    def open_clicked(self):
        self.logger.debug("Open Clicked")

    def demo_action(self):
        self.logger.debug("Demo Action!")
        self.verilog_graph.add_verilog_module("test", {"test_data":"data"})

    def get_graph(self):
        return self.verilog_graph

    def tree_clicked(self):
        index = self.file_view.currentIndex()
        path = self.file_model.filePath(index)
        if os.path.isdir(str(path)):
            self.user_path = path
            self.logger.info("Start Path changed to: %s" % self.user_path)
        elif is_verilog_file(str(path)):
            self.logger.info("verilog path: %s" % path)
            self.actions.set_verilog_module.emit(0, path)

        for i in range(self.file_model.columnCount()):
            self.file_view.resizeColumnToContents(i)

    def tree_directory_loaded(self):
         for i in range(self.file_model.columnCount()):
            self.file_view.resizeColumnToContents(i)

    def closeEvent(self, event):
        self.logger.debug("Close Event")
        self.settings.setValue("prev_dir", self.user_path)
        quit()

