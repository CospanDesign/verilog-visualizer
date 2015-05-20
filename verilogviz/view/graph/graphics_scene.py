# Copyright (c) 2015 Dave McCoy (dave.mccoy@cospandesign.com)

# This file is part of Nysa (wiki.cospandesign.com/index.php?title=Nysa).
#
# Nysa is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# Nysa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Nysa; If not, see <http://www.gnu.org/licenses/>.


""" nysa interface
"""

__author__ = 'dave.mccoy@cospandesign.com (Dave McCoy)'

import sys
import os
import time
import logging

from PyQt4.Qt import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

p = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            os.pardir,
                                            os.pardir,
                                            os.pardir))

p = os.path.abspath(p)
#print "Visual Graph Path: %s" % p
sys.path.append(p)
from common.pvg.visual_graph.graphics_scene import GraphicsScene as gs

def enum(*sequential, **named):
  enums = dict(zip(sequential, range(len(sequential))), **named)
  return type('Enum', (), enums)

view_state = enum(  "normal",
                    "core_selected")





class GraphicsScene(gs):

    def __init__(self, view, actions, app):
        super (GraphicsScene, self).__init__(view, app)
        self.logger = logging.getLogger("verilogviz")
        self.actions = actions
        self.state = view_state.normal

        self.links = []

    #Parent Graphics Scene Overriden Functions
    def box_selected(self, data):
        self.logger.debug("Box Selected Not Implemented yet!")

    def box_deselected(self, data):
        self.logger.debug("Box Deselected Not Implemented yet!")

    def remove_selected(self, reference):
        self.logger.debug("Remove not implemented yet!")

    #Overriden PyQT4 Methods
    def mouseMoveEvent(self, event):
        super (GraphicsScene, self).mouseMoveEvent(event)
        self.auto_update_all_links()

    def mousePressEvent(self, event):
        super (GraphicsScene, self).mousePressEvent(event)
        self.auto_update_all_links()

    def dropEvent(self, event):
        self.logger("Drop Event: %s" % str(event))
        super (GraphicsScene, self).dropEvent(event)

    def startDrag(self, event):
        self.logger("start Drag Event: %s" % str(event))
        if self.dbg: print "GS: Drag start event"

    #States
    def get_state(self):
        return self.state

    def auto_update_all_links(self):
        for l in self.links:
            if l.is_center_track():
                l.auto_update_center()


