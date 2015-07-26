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

import networkx as nx

SCALE_X = 200.0
SCALE_Y = 100.0


class VerilogGraph(GraphicsWidget):

    def __init__(self, app, actions):
        self.actions = actions
        self.logger = logging.getLogger("verilogviz")
        self.view = GraphicsView(self)
        self.scene = GraphicsScene(self.view, self.actions, app)
        super (VerilogGraph, self).__init__(self.view, self.scene)
        self.boxes = {}
        self.app = app
        self.vpos = 0

    def fit_in_view(self):
        self.view.fit_in_view()
        self.logger.debug("fit in view")

    def clear(self):
        self.scene.clear_links()
        self.scene.clear()
        self.boxes = {}

    def update(self):
        super (VerilogGraph, self).update()
        self.scene.auto_update_all_links()
        self.view._scale_fit()

    def sizeHint (self):
        size = QSize()
        size.setWidth(600)
        return size

    def add_verilog_module(self,  module, position):
        mb = ModuleBox( self.scene,
                        MODULE_POS,
                        module.name(),
                        MODULE_COLOR,
                        module,
                        MODULE_RECT)

        self.boxes[id(module)] = mb

        mb.setPos(position)
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


    def _tree_layout_creator(self, node_id, tree, graph, depth = 0, position_depth_list = [0], layout = {}, vpos = 0):

        self.vpos = vpos
        #layout[node_id] = [depth * SCALE_X, position_depth_list[depth] * SCALE_Y]
        layout[node_id] = [depth * SCALE_X, vpos * SCALE_Y]
        position_depth_list[depth] += 1
        successors = tree.successors(node_id)
        '''
        for e in tree.edges():
            if e[0] == node_name:
                if e[1] not in successors:
                    successors.append(e[1])
        '''

        sub_position = 0

        if len(successors) > 0 and len(position_depth_list) <= depth + 1:
            position_depth_list.append(0)

        for s in successors:
            #print "successor :%d"  % s
            self._tree_layout_creator(s, tree, graph, depth + 1, position_depth_list, layout, self.vpos)
            if successors.index(s) > 0:
                self.vpos += 1

        return layout
        

    def draw_module(self, module):
        graph = module.get_module_graph()
        #Find the depth of the modules
        #layout = nx.layout.fruchterman_reingold_layout(graph, scale = 1000.0)
        #layout = nx.layout.spring_layout(graph, scale = 1000.0)
        #import matplotlib.pyplot as plt
        bfs_tree = nx.bfs_tree(graph, source = id(module))
        #print "BFS Tree: %s" % str(dir(bfs_tree))
        #print "nodes: %s" % str(bfs_tree.successors(module.name()))
        #print "edges: %s" % str(bfs_tree.edges())
        layout = self._tree_layout_creator(id(module), bfs_tree, graph)
        
        #nx.draw(layout)
        #plt.show()
        #print "layout: %s" % str(layout)
        for n in graph.nodes():
            #print "N: %d" % n
            module = graph.node[n]
            p = QPointF(layout[n][0], layout[n][1])
            self.add_verilog_module(module, p)

        for e in graph.edges():
            #print "e: %s" % str(e)
            #print "\t%s %s" % (e[0], e[1])
            x1 = layout[e[0]][0]
            x2 = layout[e[1]][0]
            self.boxes[e[0]].add_link(self.boxes[e[1]], from_side = "right", to_side = "left")
            #self.boxes[e[0]].add_link(self.boxes[e[1]], from_side = "left", to_side = "right")
            #if x2 > x1:
            #else:
            

