import sys
import os
import logging

p = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
p = os.path.abspath(p)
sys.path.append(p)

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from graphics_view import GraphicsView
from graphics_scene import GraphicsScene

from common.pvg.visual_graph.graphics_widget import GraphicsWidget

from module_box import ModuleBox

from graphical_defines import MODULE_RECT
from graphical_defines import MODULE_COLOR
from graphical_defines import MODULE_POS


class VerilogGraph(GraphicsWidget):

    def __init__(self, app, actions):
        self.actions = actions
        self.logger = logging.getLogger("verilogviz")
        self.view = GraphicsView(self)
        self.scene = GraphicsScene(self.view, self.actions, app)
        super (VerilogGraph, self).__init__(self.view, self.scene)
        self.boxes = {}
        self.app = app

    def fit_in_view(self):
        self.view.fit_in_view()
        self.logger.debug("fit in view")

    def clear(self):
        self.scene.clear()
        self.boxes = {}
        self.scene.clear_links()

    def update(self):
        super (FPGABusView, self).update()
        self.scene.auto_update_all_links()
        self.view._scale_fit()

    def sizeHint (self):
        size = QSize()
        size.setWidth(600)
        return size

    def add_verilog_module(self, module_name, module_data):
        mb = ModuleBox( self.scene,
                        MODULE_POS,
                        module_name,
                        MODULE_COLOR,
                        module_data,
                        MODULE_RECT)

        self.boxes["module_name"] = mb
        return mb

    def set_verilog_module_position(name, position):
        box = self.boxes[name]
        box.setPos(position)

    def clear(self):
        self.boxes = {}
        self.scene.clear()
        self.scene.clear_links()

    def get_box_data(self, name):
        return self.boxes[name]

    def is_box_in_graph(self, name):
        return name in self.boxes.keys()

    def drag_enter(self, event):
        self.logger.debug("Module Drag Enter")

    def drag_leave(self, event):
        self.logger.debug("Module Drag Leave")

    def drag_move(self, event):
        self.logger.debug("Module Drag Move")

    def drop_event(self, event):
        self.logger.debug("Drop Event")


