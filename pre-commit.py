#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "A.A.Konovalov"
__

import sys
import os
import re
import subprocess

from simplegit import Git


class GitHook(Git):
    """ Git hook actions 
    """

    def check_max_length(self, filename, default_line_length=80):
        """ check max length of source lines
        """
        # 1) get a config
        max_line_length = self.get_param("pre-commit.max-line-length", default_line_length)
        
        try:
            max_line_length = int(max_line_length)
        except:
            max_line_length = default_line_length

        # 2) get a lines and check
        for n,s in self.get_diff_rows(filename):
            length = len(s)
            if length > max_line_length:
                # TODO: return this message as result...
                print "%s:%d:Line has length %d but %d is allowed" % (filename, n, length, max_line_length)
                print "%s[...]" % s[:max_line_length]
                return False

        return True

    def check_file(self, filename):
        """ check one file
        """
        if self.get_param("pre-commit.max-line-length.enabled") != "false":
            res = self.check_max_length(filename)
            if not res:
                return False
            
        # ... otherwise check-routine place here...
        return True        

    def check(self):
        """ check all files in a commit
        """
        for filename in self.get_files():
            if not self.check_file(filename):
                return False

        # ... otherwise check routines place here...
        return True        


if __name__ == "__main__":
    print "CHECK a Files...."
    hook = GitHook()
    if hook.check():
        exit(0)
    else:
        exit(1)
