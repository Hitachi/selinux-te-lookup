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

"""SELinux Type Enforcement Lookup"""
import sys

from lib.ConfigFile import ConfigFile
from lib.ArgumentManager import ArgumentManager
from lib.SELabel import SELabel
from lib.SEPolicyAttributes import SEPolicyAttributes
from lib.ProcessAccessableContexts import ProcessAccessableContexts
from lib.FilePathFinder import FilePathFinder
from lib.CSV import CSV
from lib.Progress import Progress


class SELinuxLookup:
  def __init__(self, domain, target = None, perms = [], klass = None):
    self.contexts = ProcessAccessableContexts(domain=domain, 
                      target=target, perms=perms, klass=klass)
    self.klass = klass
  
  def find(self, root, prune=[], all_contexts=False):
    contexts = self.contexts
    for file_info in FilePathFinder.find(root, prune, self.klass):
      real_path, real_label, real_type = file_info
      for context in contexts.match(real_path, real_type):
        yield (context, file_info)
        if not all_contexts:
          break


if __name__ == "__main__":
  ini = ConfigFile("config.ini")
  argument_manager = ArgumentManager(ini, description='SELINUX LOOKUP')
  argument_manager.add('domain', help='specify process domain')
  argument_manager.add_option_list('prune', help='pruned folders for find command')
  argument_manager.add_option('result-file', default="result.csv", help='result file name: output only file that has same SELinux label between fContext and file')
  argument_manager.add_option('ok-file', default=None, help='result file name: output only file that has same SELinux label between fContext and file')
  argument_manager.add_option('ng-file', default=None, help='result file name: output only file that has diffrent SELinux label between fContext and file')
  argument_manager.add_option('root', default='/', help='specify root directory for search')
  argument_manager.add_option('target', help='target domain of search condition')
  argument_manager.add_option_list('perm', help='permits list of search condition')
  argument_manager.add_option('class', dest='klass', help='file object class of search condition')
  argument_manager.add_option('print-summary', action='store_true', default=False, help='print summary')
  argument_manager.add_option('warning-attribute-threshold', default="20", help='threshold of attribute members whether warning')
  argument_manager.add_option('only-file-path', action='store_true', default=False, help='output only file path')
  argument_manager.add_option('only-file-context', action='store_true', default=False, help='output only file context')
  argument_manager.add_option('only-ok', action='store_true', default=False, help='output only file path that has same SELinux label between fContext and file')
  argument_manager.add_option('only-ng', action='store_true', default=False, help='output only file path that has diffrent SELinux label between fContext and file')
  argument_manager.add_option('stdout', action='store_true', default=False, help='output stdout')
  argument_manager.add_option('all-contexts', action='store_true', default=False, help='output all matched contexts')
  args = argument_manager.args()

  process_domain = args.domain
  warning_attribute_threshold = int(args.warning_attribute_threshold)

  lookup = SELinuxLookup(domain=process_domain, target=args.target, perms=args.perm, klass=args.klass)

  if lookup.contexts.isEmpty():
    sys.stderr.write("There is no rules on the conditions.\n")
    sys.exit(-1)

  csv_header=['File-Context-Pattern', 'File-Context-Target-Type', 'File-Context-Label', 'Matched-File-Path', "File-Type", 'File-Label', "SAME-SELinux-Type"]
  if args.only_file_path:
    csv_header=['Matched-File-Path']
  elif args.only_file_context:
    csv_header=['File-Context-Pattern', 'File-Context-Target-Type',  'File-Context-Label']

  result_csv_writer = None
  if args.stdout:
    result_csv_writer = CSV(stream=sys.stdout)
  else:
    result_csv_writer = CSV(args.result_file)
  
  result_csv_writer.writerow(csv_header) 

  if args.only_file_context:
    for pattern, target_type, attr in lookup.contexts.all():
      record = [pattern, target_type, ":".join(attr)]
      result_csv_writer.writerow(record)
    result_csv_writer.close()
    sys.exit(0)

  ok_csv_writer = CSV(args.ok_file)
  ok_csv_writer.writerow(csv_header)

  ng_csv_writer = CSV(args.ng_file)
  ng_csv_writer.writerow(csv_header)
  

  true_count = 0
  false_count = 0

  progress = Progress()
  if args.stdout: progress.silent()
  progress.start()

  for (context, file) in lookup.find(args.root, args.prune, args.all_contexts):
    real_path, real_label, real_type = file
    real_user, real_role, real_domain, real_level = SELabel.parse(real_label)
    pattern, target_type, attr = context
    user, role, domain, level = attr
    same_domain = (real_domain == domain)
    record = [
      pattern, 
      target_type,
       ":".join(attr), 
       real_path, 
       real_type, 
       real_label, 
       ("OK" if same_domain else "NG")
    ]

    if args.only_file_path:
      record = [real_path]
    
    if args.only_ok and same_domain:
      result_csv_writer.writerow(record)
    elif args.only_ng and not same_domain:
      result_csv_writer.writerow(record)
    elif not args.only_ok and not args.only_ng:
      result_csv_writer.writerow(record)

    if same_domain:
      true_count += 1
      ok_csv_writer.writerow(record)
    else:
      false_count += 1
      ng_csv_writer.writerow(record)
    
  progress.stop()
  
  result_csv_writer.close()
  ok_csv_writer.close()
  ng_csv_writer.close()

  if args.print_summary:
    print
    print
    
    print "Process Domain: {0}".format(process_domain)
    print "Valid domain between path and file context: {0}".format(true_count)
    print "Invalid domain between path and file context: {0}".format(false_count)
    print "Targeted file contexts by the process domain: {0}".format(lookup.contexts.matcher.counter)
    print "Targeted domain by the process domain: {0}".format(len(lookup.contexts.rules.all_target_domains()))

    warning_attrs = SEPolicyAttributes.get_attributes_with_over_members(warning_attribute_threshold)
    for domain in contexts.rules.target_domains():
      if domain in warning_attrs:
        print "[Warning] The process domain has permission to: {0}".format(domain)

  print