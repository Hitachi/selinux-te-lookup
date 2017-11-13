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


import sys
import time
import threading


class Progress(threading.Thread):
  def __init__(self):
    super(Progress, self).__init__()
    self.setDaemon(True)
    self.out = sys.stdout
    self.time = 0
    self.count = 0
    self.active = True

  def tick(self):
    next_time = time.time()
    if next_time - self.time > 0.25:
      self.time = next_time
      self.count = (self.count + 1 ) % 10
      if self.count == 0:
        self.out.write('\r\033[K')
      else:
        self.out.write("+")
      self.out.flush()

  def stop(self):
    self.active = False
    self.join()

  def silent(self):
    self.out = open('/dev/null', 'w')
  
  def run(self):
    while self.active:
      self.tick()
      time.sleep(0.1)
    self.out.write('\r\033[K')
    self.out.flush()