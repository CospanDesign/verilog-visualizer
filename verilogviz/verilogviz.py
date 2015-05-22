#! /usr/bin/python

import os
import sys
import logging
from PyQt4.Qt import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from view.main_form import MainForm

from verilog_viz_actions import Actions
from model.module_model import ModuleModel

class VerilogViz(QObject):

    def __init__(self):
        super (VerilogViz, self).__init__()

        #Create a logger
        self.actions = Actions()
        logger = logging.getLogger('verilogviz')
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(filename)s:%(module)s:%(funcName)s: %(message)s')
        #formatter = logging.Formatter('%(pathname)s:%(module)s:%(funcName)s: %(message)s')

        #Create a Console Handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        ch.setLevel(logging.DEBUG)
        logger.addHandler(ch)

        #logger.debug('Initialize')
        QThread.currentThread().setObjectName("main")

        self.actions.set_verilog_module.connect(self.set_verilog_module)

        app = QApplication(sys.argv)
        #Setup the view
        self.main_form = MainForm(self, self.actions)
        self.module_models = [ModuleModel(0, self.actions)]

        sys.exit(app.exec_())

    def set_verilog_module(self, index, path):
        self.module_models[index].set_verilog_module(path)
        self.main_form.add_verilog_project_list_item("name")

