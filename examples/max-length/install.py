#!/usr/bin/env python

from __future__ import print_function

"""Install util for git hook pre-commit."""

__author__ = "A.A.Konovalov"
__version__ = "0.3"


import sys
import os
import shutil


args = sys.argv

if len(args) == 1:
    print("usage: python install.py <path-to-repository> [max-line-length]")
    print("Example:\n  python install.py /home/projects/myprj 80")
    exit()

target_path = args[1] 

try:
    import simplegit
except ImportError:
    print("ERROR: module simplegit isn't installed")
    exit()

if len(args) > 2:
    max_line_length = int(args[2])
else:
    # setup default value
    max_line_length = 80

if not os.path.exists(target_path):
    print("ERROR: invalid repository path")
    exit()

if not os.path.exists(os.path.join(target_path, ".git")):
    print("ERROR: git repository folder not found")
    exit()

full_target_path = os.path.join(target_path, ".git", "hooks")

if not os.path.exists(full_target_path):
    os.makedirs(target_path2)

# copy python-script as git's hook
filename = os.path.join(full_target_path, "pre-commit")
shutil.copy("pre-commit.py", filename)

# set permissions to hook file
os.chmod(filename, 0o777)

# set up config
git = simplegit.Git()
git.set_param(
    "pre-commit.max-line-length",
    str(max_line_length),
    os.path.join(target_path, ".git", "config")
)

print("Install hook pre-commit: OK")
print("Attention: to disable max line length checking, please run:")
print("$ git config pre-commit.max-line-length.enabled false")


