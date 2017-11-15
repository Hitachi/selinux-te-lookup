SELinux Type Enforcement Lookup (Ver 0.1.1)
===

On SELinux Type Enforcement, this tool looks up files which a process has permissions with. 

When there was no this tool, it was too much of a bother surveying that which file could be accessed by target processes.

But now, you could get it easily and fastly!

# Description
In the case of troubleshooting on SELinux, how do you survey status on your system?
If you want to know that what files your process can access,
you may use some tools: sesearch, seinfo and semanage.
You need to check below:
1) What sepolicy rules have your process as a source?
1) What file contexts have targets of the rules?
1) What files are matched with the file contexts?

In addition, you may need to consider below:
1) Which each domain is attributes or types?
1) What dose the attributes has types as members?
1) What attributes does the types belong to ?
1) How are attributes and types related with sepolicy rules and file contexts?

Our tool will make you free from the complexity!!
You only give a domain of a target process and some options.
Then, It is looked up to:
1) Policy rules which have the specified domain as a source domain.
1) File contexts which have the rules' target types as labels.
1) Files which are matched with the contexts' patterns.

Of course, attributes are considered.

This way, you could look up files which processes have permission with under SELinux Type Enforcement.

# DEMO
Try get file list which 'httpd_t' domain process be able to read and write.
```
$ sudo python selinux-te-lookup.py httpd_t --perm read write --stdout
File-Context-Pattern,File-Context-Target-Type,File-Context-Label,Matched-File-Path,File-Type,File-Label,SAME-SELinux-Type
/dev/shm,directory,system_u:object_r:tmpfs_t:s0,/dev/shm,d,system_u:object_r:tmpfs_t:s0,OK
/dev/tty,character device,system_u:object_r:devtty_t:s0,/dev/tty,c,system_u:object_r:devtty_t:s0,OK
/dev/full,character device,system_u:object_r:null_device_t:s0,/dev/full,c,system_u:object_r:null_device_t:s0,OK
/dev/zero,character device,system_u:object_r:zero_device_t:s0,/dev/zero,c,system_u:object_r:zero_device_t:s0,OK
--omit--
```

# OUTPUT
##FILE 
Without --stdout option, the result is outputted into "result.csv" file. 

## CSV COLUMNS
One record has a set of a file context and a file which be matced file context pattern.

- File-Context-Pattern
   - File context's patterns which match to file pathes

- File-Context-Target-Type
  - File context's target types which match to file types

- File-Context-Label
  - File context's label.

- Matched-File-Path
  - File pathes which are matched file context's patterns

- File-Type
  - File types: file(f), directory(d), synbolic link(l) or so on

- File-Label
  - File's SELinux security context label

- SAME-SELinux-Type
  - wheather it is same that file context's SELinux type and file's one

# Requirements
- policycoreutils-python
- python2


# INSTALL
 Download and unpack the compressed file to an arbitrary directory.
 

# Usage
- Find path that 'httpd_t' domain has permissions with.
```
sudo python selinux-te-lookup.py 'httpd_t'
```

- Find path that 'httpd_t' domain is able to read and write to.
  - Use --perm option.
  - --perm option allows multipule arguments.
```
sudo python selinux-te-lookup.py 'httpd_t' --perm write read
``` 

- Find path in /usr that 'httpd_t' domain is able to access to.
  - Use --root option.
```
sudo python selinux-te-lookup.py 'httpd_t' --root /usr
```

- Igonore /proc direcotry for search.
  - Use --prune option.
```
sudo python selinux-te-lookup.py 'httpd_t' --prune /proc
```

- Find 'tmp_t' type path that 'httpd_t' domain is able to access to.
  - Use --target option.
```
sudo python selinux-te-lookup.py 'httpd_t' --target 'tmp_t'
```

- Find directory path that 'httpd_t' domain is able to access to.
  - Use --class option.
  - --class allows below arguments
    - file: file
    - dir: directory
    - lnk_file: synbolic link
    - sock_file: socket
    - etc.
```
sudo python selinux-te-lookup.py 'httpd_t' --class 'dir'
```

 

- Find path that 'httpd_t' domain is able to access to. In addtion, it is same that a file context SELinux type and a file's one.
  - Use --only-ok option.
```
sudo python selinux-te-lookup.py 'httpd_t' --only-ok
```

- Find path that 'httpd_t' domain is not able to access to because the type is changed from the file context's type.
  - Use --only-ng option.
```
sudo python selinux-te-lookup.py 'httpd_t' --only-ng
```

- Output results into stdout.
  - Use --stdout option.
```
sudo python selinux-te-lookup.py 'httpd_t' --stdout
```

- Output all matched contexts (only source domain has permission to).
  - Use --all-contexts option.
```
sudo python selinux-te-lookup.py 'httpd_t' --all-contexts
```

## INI FILE
In the config.ini file, you can put above options. For instance, if you want to exclude /proc directory at all time, you can put:
```
[settings]
prune = /proc
```

If settings duplicate between config.ini and command-line arguments, command-line arguments is prefered.

# Contributing
We are grateful for contributing bug reports, bugfixes and improvements.
## Bug Report
Please open a new issue.

## Bugfixes and Improvements
Please open a new pull request.

# License
Copyright (c) 2017 Hitachi, Ltd. All Rights Reserved.

Licensed under the MIT License.
You may obtain a copy of the License at

* https://opensource.org/licenses/MIT

This file is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OF ANY KIND.
