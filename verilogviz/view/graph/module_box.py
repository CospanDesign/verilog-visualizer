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
import json

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


from common.pvg.visual_graph.box import Box
from common.pvg.visual_graph import graphics_utils as gu


class ModuleBox(Box):
    def __init__(self,
                 scene,
                 position,
                 module_name,
                 color,
                 data,
                 rect):

        super(ModuleBox, self).__init__(position = position,
                                         scene = scene,
                                         name = module_name,
                                         color = color,
                                         rect = rect,
                                         user_data = data)
        self.module_name = module_name
        self.logger = logging.getLogger("verilogviz")
        self.dragging = False

        md = {}
        md["name"] = module_name
        md["color"] = "color"
        md["data"] = data
        md["move_type"] = "move"
        self.mime_data = json.dumps(md)
        self.setAcceptDrops(False)
        #self.movable(False)

    def contextMenuEvent(self, event):

        menu_items = (("&Remove", self.view_module),)

        menu = QMenu(self.parentWidget())
        for text, func in menu_items:
            menu.addAction(text, func)
        menu.exec_(event.screenPos())

    def view_module(self):
        self.logger.debug("View Module!")

    def itemChange(self, a, b):
        if QGraphicsItem.ItemSelectedHasChanged == a:
            if b.toBool():
                #Tell the scene that we are selected
                #self.s.
                self.logger.debug("Item Selected")
                pass
            else:
                #Tell the scene that we are no longer selected
                self.logger.debug("Item Deselected")
                pass

        return super(ModuleBox, self).itemChange(a, b)

    def mouseMoveEvent(self, event):
        if not self.is_movable():
            return super(ModuleBox, self).mouseMoveEvent(event)

        if (Qt.LeftButton & event.buttons()) > 0:
            pos = event.pos()
            epos = event.buttonDownPos(Qt.LeftButton)
            l = QLineF(pos, epos)
            if (l.length() < QApplication.startDragDistance()):
                event.accept
                return

            elif not self.dragging:
                self.dragging = True
                self.hide()
                mime_data = QMimeData()
                mime_data.setData("application/flowchart-data", self.mime_data)
                 #Create and dispatch a move event
                drag = QDrag(event.widget())
                drag.start(Qt.MoveAction)
                drag.setMimeData(mime_data)

                #create an image for the drag
                size = QSize(self.start_rect.width(), self.start_rect.height())
                pixmap = QPixmap(size)
                pixmap.fill(QColor(self.color))
                painter = QPainter(pixmap)
                pen = QPen(self.style)
                pen.setColor(Qt.black)
                painter.setPen(pen)
                painter.setFont(self.text_font)
                gu.add_label_to_rect(painter, self.rect, self.box_name)
                painter.end()
                drag.setPixmap(pixmap)
                prev_pos = self.pos()
                drag.setHotSpot(epos.toPoint())
                value = drag.exec_(Qt.MoveAction)
                self.show()
                if value == 0:
                    event.accept
                else:
                    event.accept
                self.dragging = False

        super(ModuleBox, self).mouseMoveEvent(event)


    def mouseReleaseEvent(self, event):
        super (ModuleBox, self).mouseReleaseEvent(event)


