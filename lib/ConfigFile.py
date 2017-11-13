# coding: utf-8

# Copyright (c) 2017 Hitachi, Ltd. All Rights Reserved.
#
# Licensed under the MIT License.
# You may obtain a copy of the License at
#
#    https://opensource.org/licenses/MIT
#
# This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OF ANY KIND.

import os.path
from ConfigParser import SafeConfigParser as config_parser

class ConfigFile:
  
  def __init__(self, filename, defaults ={}, section="settings"):
    ini = config_parser()
    if os.path.isfile(filename):
      ini.read(filename)
    self.ini = ini
    self.defaults = defaults
    self.section = section


  def get(self, prop):
    ini = self.ini
    section = self.section
    if not ini.has_option(section, prop): 
      return self.defaults.get(prop, "")
    else:
      return ini.get(section, prop)


  def get_list(self, prop):
    item = self.get(prop)
    if item == '': return []
    items = item.split(",")
    items = [ item.strip() for item in items]
    return items