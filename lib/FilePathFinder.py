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
import subprocess
import csv

class FilePathFinder:
  
  @staticmethod
  def file_class_to_type(file_class):
    if file_class == "file": return 'f'
    elif file_class == "dir": return 'd'
    elif file_class == "lnk_file": return 'l'
    elif file_class == "sock_file": return 's'
    elif file_class == "chr_file": return 'c'
    elif file_class == "blk_file": return 'b'
    elif file_class == "fifo_file": return 'p'
    return None


  @staticmethod
  def find(root="/", prunes=[], file_class="", results =["%p", "%Z", "%y"]):
    root = os.path.abspath(root)
    file_type = FilePathFinder.file_class_to_type(file_class)
    file_type_option = ""
    if not file_type is None:
      file_type_option = "-type {0}".format(file_type)
    prune_option = " ".join(["-path {0} -prune -o".format(dir) for dir in prunes])
    results_option = ",".join([r'"{0}"'.format(result) for result in results])
    FIND_FILE_LABEL_COMMAND = r'find {0} {1} {2} -printf "\"%p\",\" %Z\",\" %y\"\n"'
    find_cmd = FIND_FILE_LABEL_COMMAND.format(root, prune_option, file_type_option, results_option)
    devnull = open(os.devnull, 'wb')
    proc = subprocess.Popen(find_cmd, shell  = True, stdout = subprocess.PIPE, stderr = devnull)
    for line in proc.stdout:
      values = [ v.strip() for v in (list(csv.reader([line]))[0]) ]
      yield values