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

import argparse

class ArgumentManager:
  def __init__(self, ini, description=None):
    self.ini = ini
    params = {}
    if not description is None:
      params['description'] = description

    self.parser = argparse.ArgumentParser(**params)

  def add(self, prop, dest = None, help=None):
    self.parser.add_argument(prop, action='store', help=help)
  
  def add_option(self, prop, dest = None, default=None, help=None, action='store'):
    ini_default = self.ini.get(prop)
    if ini_default != "":
      default = ini_default
      
    params = {
      'action': action,
      'default': default
    }

    if not dest is None:
      params['dest'] = dest

    if not help is None:
      params['help'] = help
      
    self.parser.add_argument("--"+ prop, **params)
  
  def add_option_list(self, prop, dest=None, default=[], help=None):
    ini_default = self.ini.get_list(prop)
    if(len(ini_default)>0):
      default = ini_default
    
    params = {
      'action': 'store',
      'nargs': '*',
      'default': default
    }

    if not dest is None:
      params['dest'] = dest

    if not help is None:
      params['help'] = help

    self.parser.add_argument("--"+ prop, **params)


  def args(self):
    return self.parser.parse_args()
