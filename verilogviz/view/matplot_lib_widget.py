from PyQt4.Qt import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from matplotlib.backends import qt4_compat
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg 
from matplotlib.figure import Figure
#from matplotlib.pyplot import figure

import networkx as nx





class MatplotLibWidget(FigureCanvas):

    def __init__(self, parent = None):

        fig = Figure()
        self.sp = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.sp.hold(False)

        #layout = QVBoxLayout()

        #self.figure = figure()
        '''
        self.canvas = FigureCanvas(self.figure)

        self.toolbar = NavigationToolbar2QTAgg(self.canvas, self)
        '''

        #layout.addWidget(self.toolbar)
        #layout.addWidget(self.canvas)
        #self.setLayout(layout)


        '''
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        '''

        self.setParent(parent)
        self.setSizePolicy( QSizePolicy.Expanding,
                            QSizePolicy.Expanding)
        self.updateGeometry()

    def draw_graph(self, graph):
        value = nx.draw(graph, ax=self.sp)
        self.sp.draw(value)


    def compute_initial_figure(self):
        pass

