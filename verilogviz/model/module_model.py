import logging


class ModuleModel(object):

    def __init__(self, index, actions):
        super (ModuleModel, self).__init__()
        self.logger = logging.getLogger("verilogviz")
        self.actions = actions
        self.module = ""

    def set_verilog_module(self, module_path):
        self.logger.info("module path changed to: %s" % module_path)
        
        
        
