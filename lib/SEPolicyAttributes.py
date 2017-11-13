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

class SEPolicyAttributes:
  @staticmethod
  def get_all_attributes():
    return sepolicy.get_all_attributes()
  
  @staticmethod
  def get_types_from_attribute(attribute):
    return sepolicy.get_types_from_attribute(attribute)
  
  @staticmethod
  def get_attributes_with_over_members(threshold):
    results = []
    for attr in SEPolicyAttributes.get_all_attributes():
      members = SEPolicyAttributes.get_types_from_attribute(attr)
      if len(members) >= threshold:
        results.append(attr)
    return results