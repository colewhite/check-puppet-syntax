Check Puppet Syntax
===================

Python tool for checking Puppet .pp and .erb file syntax using Puppet's built-in ```puppet parser validate``` and
Ruby's ```erb | ruby``.

```
usage: check_puppet_syntax.py [-h] [-f FILE] [-d DIRECTORY]

Puppet .pp and .erb syntax checker.

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  File to be checked.
  -d DIRECTORY, --directory DIRECTORY
                        Directory to be checked. (Recursive)
```
