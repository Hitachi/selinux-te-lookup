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

class SELabel:
  @staticmethod 
  def parse(label):
    vals = label.split(":")
    (user, role, domain), level = vals[:3], vals[4:]
    level = ":".join(level)
    return (user, role, domain, level)