import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

_action_instance = None

#Singleton Magic
def Actions(*args, **kw):
    global _action_instance
    if _action_instance is None:
        _action_instance = _Actions(*args, **kw)
    return _action_instance

class _Actions(QtCore.QObject):

    #Host Actions
    #Control Signals
    test = QtCore.pyqtSignal(name = "test_signal")
    add_verilog_module = QtCore.pyqtSignal(int, str, name = "add_verilog_module")
    configure_include_paths = QtCore.pyqtSignal(name = "configure_include_paths")

