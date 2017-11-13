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

import sepolicy
from SEPolicyAttributes import SEPolicyAttributes

class SEPolicyRules:
  @staticmethod
  def options(source=None, target =None, perms = [] ,klass =None):
    options = {}
    if not source is None:
      options[sepolicy.SOURCE] = source

    if not target is None:
      options[sepolicy.TARGET] = target

    if len(perms) > 0 :
      options[sepolicy.PERMS] = perms

    if not klass is None:
      options[sepolicy.CLASS] = klass
    return options
  
  @staticmethod
  def search_rules(types=[sepolicy.ALLOW], source="", target ="", perms = [] ,klass =""):
    options = SEPolicyRules.options(source, target, perms, klass)
    rules = sepolicy.search(types, options)
    return rules

  @staticmethod
  def target_to_classes_map(rules):
    target_to_classes_map = {}
    attributes = SEPolicyAttributes.get_all_attributes()
    for rule in rules:
      rule_target = rule[sepolicy.TARGET]
      rule_class = rule[sepolicy.CLASS]
      targets = [rule_target]
      if rule_target in attributes:
        members = SEPolicyAttributes.get_types_from_attribute(rule_target)
        targets.extend(members)
      for target in targets:
        classes = target_to_classes_map.get(target, set())
        classes.add(rule_class)
        target_to_classes_map[target] = classes
    return target_to_classes_map

  def __init__(self, types = [sepolicy.ALLOW],
                source="", target="", perms=[] ,klass =""):
    rules = SEPolicyRules.search_rules(types, source, target, perms, klass)
    if rules is None: rules = []
    rules = [ rule for rule in rules if rule['enabled']]
    self.rules = rules
    self.target_to_classes_map = SEPolicyRules.target_to_classes_map(rules)

  def target_domains(self):
    return sorted(list(set([rule[sepolicy.TARGET] for rule in self.rules])), key=str)

  def all_target_domains(self):
    return sorted(self.target_to_classes_map.keys(), key=str)

  def has_rule_with(self, target, context_type):
    map = self.target_to_classes_map
    if not target in map: return False
    classes = map.get(target)
    if context_type in ["regular file", "all files"] and 'file' in classes: return True
    elif context_type in ["directory", "all files"] and 'dir' in classes: return True
    elif context_type in ["symbolic link", "all files"] and 'lnk_link' in classes: return True
    elif context_type in ["socket", "all files"] and 'sock_file' in classes: return True
    elif context_type in ["character device", "all files"] and 'chr_file' in classes: return True
    elif context_type in ["block device", "all files"] and 'blk_file' in classes: return True
    elif context_type in ["named pipe", "all files"] and 'fifo_file' in classes: return True
    return False
  
  def size(self):
    return len(self.rules)

  def isEmpty(self):
    return (self.size()==0)
