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

import re

class FileContextMatcher:
  class Bucket:
    def __init__(self):
      self.contexts = []
      self.submap = {}


    def add_to_sub(self, context, key, pattern):
      sub = self.submap.get(key, FileContextMatcher.Bucket())
      sub.add(context, pattern)
      self.submap[key] = sub


    def add(self, context, pattern):
      pattern = pattern[1:]
      if len(pattern)  < 1:
        self.contexts.append(context)
        return

      for i, c in enumerate(pattern):
        if c in r'().+*\[]^$|':
          self.contexts.append(context)
          return

        elif c == '/':
          key = pattern[:i]
          pattern = pattern[i:]
          self.add_to_sub(context, key, pattern)
          return
      
      key = pattern
      pattern = "$"
      self.add_to_sub(context, key, pattern)


    def match(self, path):
      for context in self.contexts:
        yield context
      path = path[1:]
      index = path.find('/')
      if index == -1:
        key = path
        path = "$"
      else:
        key = path[:index]
        path = path[index:]

      sub = self.submap.get(key, None)
      if sub is None: return
      for context in sub.match(path):
        yield context


  def __init__(self):
    self.bucket = FileContextMatcher.Bucket()
    self.store = []
    self.counter = 0


  def add(self, pattern, target_type, label):
    self.counter += 1
    self.store.append((pattern, target_type, label))
    regex = re.compile("^"+pattern+"$")
    context = (pattern, regex, target_type, label)
    item = (self.counter, context)
    self.bucket.add(item, pattern)


  def match_type(self, file_type, context_type):
    if context_type == 'all files':
      return True
    
    elif context_type == "regular file":
      if file_type == "f": return True

    elif context_type == "directory":
      if file_type == "d": return True

    elif context_type == "symbolic link":
      if file_type == "l": return True

    elif context_type == "socket":
      if file_type == "s": return True

    elif context_type == "character device":
      if file_type == "c": return True
    
    elif context_type == "block device":
      if file_type == "b": return True

    elif context_type == "named pipe":
      if file_type == "p": return True
    
    else: return False


  def match(self, path, ftype):
    results = []
    for item in self.bucket.match(path):
      index, context = item
      (pattern, regex, target_type, label) = context
      if not self.match_type(ftype, target_type): continue
      if regex.match(path):
        context = (pattern, target_type, label)
        results.append((index, context))
    sorted(results, key=lambda (index, context): index)
    results = [ context for (index, context) in results ]
    results = reversed(results)
    return results