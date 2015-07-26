import os
import sys
import logging

import verilog_utils as vutils
import preprocessor
import utils
from utils import ModuleError
import networkx as nx


def find_module(path, user_paths, instance_name = None):
    module_tags = vutils.get_module_tags(filename = path, user_paths = user_paths)
    return Module(module_tags, path, user_paths, instance_name, is_include_file = False, depth = 0)

class Module (object):

    def __init__(self, module_tags, path, user_paths, instance_name = None, is_include_file = False, depth = 0):
        super (Module, self).__init__()
        self.depth = depth
        self.logger = logging.getLogger("verilogviz")
        self.instance_name = instance_name
        self.vpos = 0

        self.module_tags = module_tags
        self.path = path
        if self.path is not None:
            self.path = str(self.path)
        self.user_paths = user_paths
        self.include_file = is_include_file
        self.module_exists = True
        if path is None:
            self.module_exists = False
        self.graph = None
        self.refresh()

    def is_include_file(self):
        return self.include_file

    def exists(self):
        return self.module_exists

    def set_user_paths(self, user_paths):
        self.user_paths = user_paths
        self.refresh()

    def name(self):
        if self.instance_name is None:
            return self.module_tags["module"]
        return self.instance_name

    def get_type(self):
        return self.module_tags["module"]

    def get_module_tags(self):
        return self.module_tags

    def refresh(self):
        self.graph = nx.DiGraph()
        self.generate_dependency_graph()

    def get_path(self):
        return self.path

    def get_depth(self):
        return self.depth

    def set_vpos(self, pos):
        self.vpos = pos

    def get_vpos(self):
        return self.vpos

    def generate_dependency_graph(self):
        self.graph.add_node(id(self))
        self.graph.node[id(self)] = self
        if self.path is not None:
            self._resolve_dependency_for_module(self.path)

    def get_module_graph(self):
        return self.graph

    def _resolve_dependency_for_module(self, module_path):
        vpos = 0
        buf = ""
        try:
            filein = open(module_path)
            buf = str(filein.read())
            filein.close()
        except IOError as e:
            raise ModuleError("File %s not found" % module_path)

        buf = utils.remove_comments(buf)
        include_buf = buf
        while len(include_buf.partition("`include")[2]) > 0:
            ifname = include_buf.partition("`include")[2]
            ifname = ifname.splitlines()[0]
            ifname = ifname.strip()
            ifname = ifname.strip("\"")
            #self.logger.debug("Found ifname: %s" % ifname)
            module = None
            try:
                filename = utils.find_module_filename(ifname, self.user_paths)
                module_tags = vutils.get_module_tags(filename, self.user_paths)
                module = Module(module_tags, path = filename, user_paths = self.user_paths, instance_name = None, is_include_file = True, depth = self.depth + 1)
            except ModuleError:
                self.logger.debug("Didn't find verilog module with filename: %s" % ifname)
                module_tags = {}
                module_tags["module"] = ifname
                module = Module(module_tags, path = None, user_paths = self.user_paths, instance_name = None, is_include_file = True, depth = self.depth + 1)

            module.set_vpos(vpos)
            vpos + 1
            include_buf = include_buf.partition("`include")[2]
            for n in module.get_module_graph().nodes():
                #m = module.get_module_graph().node[n]
                #self.graph.add_node(n)
                #self.graph.node[n] = m
                #if n not in self.graph.nodes():
                m = module.get_module_graph().node[n]
                self.graph.add_node(id(m))
                self.graph.node[id(m)] = m



            self.graph.add_edges_from(module.get_module_graph().edges())
            self.graph.add_edge(id(self), id(module))

        self.logger.debug("Looking for actual modules...")
        module_dict = self.find_modules_within_buffer(buf.partition(")")[2])

        for instance in module_dict:
            module_type = module_dict[instance]
            self.logger.info("module_type: %s" % module_type)
            module = None
            #print "Module Type: %s" % module_type
            try:
                filename = utils.find_module_filename(module_type, self.user_paths)
                #print "Filename: %s" % filename
                module_tags = vutils.get_module_tags(filename, user_paths = self.user_paths)
                #print "got tags..."
                module = Module(module_tags, path = filename, user_paths = self.user_paths, instance_name = instance, is_include_file = False, depth = self.depth + 1)
            except ModuleError:
                #self.logger.debug("Didn't find verilog module with filename :%s" % module_type)
                module_tags = {}
                module_tags["module"] = module_type
                module = Module(module_tags, path = None, user_paths = self.user_paths, instance_name = instance, is_include_file = False, depth = self.depth + 1)

            for n in module.get_module_graph().nodes():
                m = module.get_module_graph().node[n]
                self.graph.add_node(id(m))
                self.graph.node[id(m)] = m

            module.set_vpos(vpos)
            vpos + 1
            #self.graph.add_nodes_from(module.get_module_graph().nodes())
            self.graph.add_edges_from(module.get_module_graph().edges())
            self.graph.add_edge(id(self), id(module))

    def find_modules_within_buffer(self, buf):
        buf = buf.strip()
        buf = buf.partition(";")[2]
        done = False
        module_dict = {}

        while not done:
            lines = buf.splitlines()
            module_token = ""
            parameter_found = False
            parameter_flag = False
            parameter_debt = None
            for line in lines:
                line = line.strip()
                if "#" in line:
                    if "<=" in line:
                        continue;
                    #print "Found #: %s" % line
                    line = line.partition("#")[2]
                    parameter_found = True

                if parameter_found:
                    #print "line: %s" % line
                    for c in line:
                        if c == "(":
                            #print "+1"
                            if parameter_debt is None:
                                parameter_debt = 1
                            else:
                                parameter_debt += 1
                        if c == ")":
                            #print "-1"
                            parameter_debt -= 1

                        if parameter_debt == 0:
                            parameter_found = False
                            parameter_flag = True
                            break

                    continue


                if line.startswith(".") and line.endswith(","):
                    module_token = line
                    break

            if len(module_token) == 0:
                done = True
                
            else:
                #Found a possible occurance of a module
                print "MODULE TOKEN: %s" % module_token
                module_buf = buf.partition(module_token)[0].strip()
                buf = buf.partition(module_token)[2]
                buf = buf.partition(";")[2]
                
                module_buf = module_buf[:module_buf.rfind("(")].strip()
                #print "module_buffer: %s" % module_buf
                if module_buf.startswith("`"):
                    continue
                
                module_type = ""
                module_instance = ""
                
                if parameter_flag:
                    #print "Parameter type: %s" % str(module_buf) 
                    module_type = module_buf.partition ("#")[0].strip("() ")
                    module_instance = module_buf.split()[-1].strip("() ")
                    #print "parameter type: %s" % module_type
                    #print "parameter instance: %s" % module_instance
                else:
                    module_buf = module_buf.splitlines()[-1]
                    module_type = module_buf.partition(" ")[0].strip("() ")
                    module_instance = module_buf.partition(" ")[2].strip("() ")
                    #print "non parameter type: %s" % module_type
                    #print "non parameter instance: %s" % module_instance
                    if len(module_type) > 50:
                        print "*** module type: %s" % module_type
                        print "*** module instance: %s" % module_instance
                
                
                self.logger.debug("Adding: %s to dictionary with instance name: %s" % (module_type, module_instance))
                module_dict[module_instance] = module_type

        return module_dict

    def _find_module_dependency(self, module_buffer):
        pass

