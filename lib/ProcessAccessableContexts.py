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

from seobject import fcontextRecords

from SEPolicyRules import SEPolicyRules
from FileContextMatcher import FileContextMatcher

class ProcessAccessableContexts:
  def __init__(self, domain, target, perms, klass):
    rule_manager = SEPolicyRules(source=domain, target=target, perms=perms, klass=klass)
    context_matcher = FileContextMatcher()
    context_map = fcontextRecords().get_all()
    for ((pattern, target_type), attr) in context_map.items():
      if attr == None: continue
      (user, role, domain, level) = attr
      if rule_manager.has_rule_with(domain, target_type):
        context_matcher.add(pattern, target_type, attr)
    self.matcher = context_matcher
    self.rules = rule_manager

  def match(self, path, file_type):
    return self.matcher.match(path, file_type)

  def isEmpty(self):
    return self.rules.isEmpty()

  def all(self):
    return self.matcher.store
    