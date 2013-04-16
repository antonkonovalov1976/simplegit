#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "A.A.Konovalov"
__version__ = "0.2"


import sys
import os
import re
import subprocess

from simplegit import Git


class GitHook(Git):
    """ simple git hook for a client side 
    """
    def check_max_length(self, filename, default_line_length=80):
        """ check max length of source lines
        """
        # get a config
        max_line_length = self.get_param("pre-commit.max-line-length", default_line_length)
        
        try:
            max_line_length = int(max_line_length)
        except:
            max_line_length = default_line_length

        # get a lines and check
        for n,s in self.get_diff_rows(filename):
            length = len(s)
            if length > max_line_length:
                print "%s:%d:Line has length %d but %d is allowed" % (filename, n, length, max_line_length)
                print "%s[...]" % s[:80]
                return False

        return True

    def check_file(self, filename):
        if self.get_param("pre-commit.max-line-length.enabled") != "false":
            res = self.check_max_length(filename)
            if not res:
                return False
            
        # ... another check-routine place here...
        return True        

    def check(self):
        """ check all files in a commit
        """
        for filename in self.get_files():
            print filename
            if not self.check_file(filename):
                return False

        # ... otherwise check routines place here...
        return True        


if __name__ == "__main__":
    print "[PRE-COMMIT HOOK] CHECK a Files...."
    hook = GitHook()
    if hook.check():
        exit(0)
    else:
        exit(1)
