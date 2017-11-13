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

import csv

class CSV:
  def __init__(self, path=None, stream=None):
    self.file = None
    self.writer = None

    if not path is None:
      self.file = open(path, 'w')
      stream = self.file
      
    if not stream is None:
      self.writer = csv.writer(stream, lineterminator='\n')
  
  def writerow(self, record):
    if self.writer is None: return
    self.writer.writerow(record)
  
  def close(self):
    if self.file is None: return
    self.file.close()