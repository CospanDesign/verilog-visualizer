#Distributed under the MIT licesnse.
#Copyright (c) 2012 Cospan Design (dave.mccoy@cospandesign.com)

#Permission is hereby granted, free of charge, to any person obtaining a copy of
#this software and associated documentation files (the "Software"), to deal in
#the Software without restriction, including without limitation the rights to
#use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
#of the Software, and to permit persons to whom the Software is furnished to do
#so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import os
import string
from string import Template

"""Arbiter Factory

Analyzes the project tags and determine if one or many arbiters are required
"""

__author__ = 'dave.mccoy@cospandesign.com (Dave McCoy)'

"""Changes:
  06/12/2012
    -Added Documentation and licsense
"""


def get_number_of_arbiter_hosts(module_tags = {}, debug = False):
    """get_number_of_arbiter_hosts

    returns the number of arbiter hosts found inside the module

    Args:
      module_tags: the tags for this module
        can be obtained with vutils.get_module_tags

    Return:
      the number of arbiter hosts associated with this module

    Raises:
      Nothing
    """

    #go through all the ports and verify that after the first
    #'_' there is a a wbm and the wbm has all the arbiter
    #host components
    #debug = False

    if debug:
        print "Module Name: %s" % (module_tags["module"])
        print "ports: "

    wb_bus = [  "o_we",
                "i_dat",
                "i_int",
                "i_ack",
                "o_adr",
                "o_stb",
                "o_cyc",
                "o_dat",
                "o_sel"
              ]
    possible_prefix = {}
    prefixes = []
    #debug = True
    for io_ports in module_tags["ports"]:
        if debug:
            print "\tio_ports: " + io_ports
        for name in module_tags["ports"][io_ports]:
            if debug:
                print "\t\t: " + str(name)
            #throw out obvious false
            if "_" not in name:
                continue

            for wbm_wire in wb_bus:
                if wbm_wire in name:
                    #io      = name.partition("_")[0]
                    #if io not in wbm_wire[0]:
                    #  continue

                    #prefix = name.partition("_")[2]
                    prefix = name.partition("_")[0]
                    #wbm_post = prefix.partition("_")[1] + prefix.partition("_")[2]
                    wbm_post = wbm_wire
                    prefix = prefix.partition(wbm_wire)[0]
                    if prefix not in possible_prefix.keys():
                        possible_prefix[prefix] = list(wb_bus)
                        if debug:
                            print "found a possible arbiter: %s" % (prefix)

                    #wbm_post = name.partition("_")[2]
                    if wbm_post in possible_prefix[prefix]:
                        possible_prefix[prefix].remove(wbm_post)

    for prefix in possible_prefix.keys():
        if debug:
            print "examining: %s" % (prefix)
            print "\tlength of prefix list: %s" % (str(possible_prefix[prefix]))
        if len (possible_prefix[prefix]) == 0:
            if debug:
                print "%s is an arbiter host" % (prefix)
            prefixes.append(prefix)

    #debug = True
    return prefixes


def is_arbiter_host(module_tags = {}, debug = False):
    """is_arbiter_host

    Determins if a slave can be an arbiter host

    Args:
      module_tags: The tags that are associated with this modue
        can be obtained with vutils.get_module_tags

    Return:
      True: Slave is an arbiter host
      False: Slave is not an arbiter host

    Raises:
      Nothing
    """
    return (len(get_number_of_arbiter_hosts(module_tags, debug)) > 0)

def is_arbiter_required(tags = {}, debug = False):
    """is_arbiter_required

    Analyzes the project tags and determines if an arbiter is requried

    Args:
      tags: Project tags

    Return:
      True: An arbiter is required
      False: An arbiter is not required

    Raises:
      Nothing
    """
    if debug:
      print "in is_arbiter_required()"
    #count the number of times a device is referenced

    #SLAVES
    slave_tags = tags["SLAVES"]
    for slave in slave_tags:
        if debug: print "found slave " + str(slave)
        if ("BUS" in slave_tags[slave]):
            if (len(slave_tags[slave]["BUS"]) > 0):
                return True
    #XXX: FOR THIS FIRST ONE YOU MUST SPECIFIY THE PARTICULAR MEMORY SLAVE AS APPOSED TO JUST MEMORY WHICH IS THAT ACTUAL MEMORY INTERCONNECT

    return False

def generate_arbiter_tags(tags = {}, debug = False):
    """generate_arbiter_tags

    generate a dictionary (tags) that is required to generate all the
    arbiters and how and where to connect all the arbiters

    Args:
      tags: Project tags

    Return:
      dictionary of arbiters to generating

    Raises:
      Nothing
    """
    arb_tags = {}
    if (not is_arbiter_required(tags)):
        return {}

    if debug:
        print "arbitration is required"

    slave_tags = tags["SLAVES"]
    for slave in slave_tags:
        if ("BUS" in slave_tags[slave]):
            if (len(slave_tags[slave]["BUS"]) == 0):
                continue
            if debug:
                print "slave: " + slave + " is an arbtrator master"
            for bus in slave_tags[slave]["BUS"].keys():
                if debug:
                    print "bus for " + slave + " is " + bus
                arb_slave = slave_tags[slave]["BUS"][bus]
                if debug:
                    print "adding: " + arb_slave + " to the arb_tags for " + bus

                if (not already_existing_arb_bus(arb_tags, arb_slave)):
                    #create a new list
                    arb_tags[arb_slave] = {}

                arb_tags[arb_slave][slave] = bus

    return arb_tags

def already_existing_arb_bus(arb_tags = {}, arb_slave = "", debug = False):
    """already_existing_arb_bus

    Check if the arbitrated slave already exists in the arbiter tags

    Args:
        arb_tags: arbiter tags
        arb_slave: possible arbiter slave

    Return:
        True: There is already an arbiter bus associated with this slave
        False: There is not already an arbiter bus associated with this slave

    Raises:
        Nothing
    """
    for arb_item in arb_tags.keys():
        if (arb_item == arb_slave):
            return True
    return False

