#! /usr/bin/python

import os
import sys
import logging
from PyQt4.Qt import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from view.main_form import MainForm

from verilog_viz_actions import Actions
from model.module import find_module

class VerilogViz(QObject):

    def __init__(self):
        super (VerilogViz, self).__init__()

        #Create a logger
        self.actions = Actions()
        self.logger = logging.getLogger('verilogviz')
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(filename)s:%(module)s:%(funcName)s: %(message)s')
        #formatter = logging.Formatter('%(pathname)s:%(module)s:%(funcName)s: %(message)s')

        #Create a Console Handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        ch.setLevel(logging.DEBUG)
        self.logger.addHandler(ch)

        QThread.currentThread().setObjectName("main")

        self.actions.add_verilog_module.connect(self.add_verilog_module)
        self.actions.configure_include_paths.connect(self.include_paths_dialog)

        app = QApplication(sys.argv)
        #Setup the view
        self.main_form = MainForm(self, self.actions)
        sys.exit(app.exec_())
        self.focused_module = None

    def add_verilog_module(self, index, path):
        module = find_module(path, self.main_form.get_include_paths())
        self.main_form.clear_graph()
        self.main_form.add_verilog_project_list_item(module)
        self.main_form.draw_module(module)

    def include_paths_dialog(self):
        if self.main_form.configure_include_paths_dialog():
            self.main_form.update_modules_user_paths(self.main_form.get_include_paths())

    def set_focused_module(self, module_name):
        self.focused_module = self.main_form.get_module(module_name)

    def create_module_graph(self):
        self.focused_module

