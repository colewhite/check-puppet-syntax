Check Puppet Syntax
===================

Multiprocessing Python tool for quickly checking Puppet .pp, .erb, and yaml file syntax using Puppet's built-in ```puppet parser validate``` and Ruby's ```erb | ruby```.

```
usage: check_puppet_syntax.py [-h] [-f FILE] [-d DIRECTORY]

Puppet .pp, .erb, and .yaml syntax checker.

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  File to be checked.
  -d DIRECTORY, --directory DIRECTORY
                        Directory to be checked. (Recursive)
```
