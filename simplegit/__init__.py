#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "A.A.Konovalov"
__version__ = "0.2"

 
import sys
import os
import re
import subprocess


class GitException(Exception): pass 


class Git(object):
    """ class for a GIT interface
    """
        
    def _call_git(self, *params):
        """ call a git command with params
        """
        p = subprocess.Popen(
            ["git"]+list(params),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False
            )
        exit_code = p.wait()
        if exit_code != 0:
            raise GitException("Error: git exit code = %s" % exit_code)

        return p.stdout.read().strip()

    def config(self, *options):
        """ run: git config <options>
        """
        return self._call_git("config", *options)

    def get_param(self, param, default=None):
        """ get one param from git config
        """
        try:
            res = self.config("--get", param)
            return res
        except GitException:
            return default    

    def set_param(self, param, value, filename=""):
        """ set one param
        """
        if filename:
            self.config("-f", filename, param, value)
        else:
            self.config(param, value)

    def del_param(self, param):
        """ remove parameter
        """
        self.config("--unset", param)

    def check_git(self):
        """ check: git is installed?
        """
        res = self.get_param("foofoo.strwgweefwtf", "error: invalid key:").lower()
        return res.startswith("error: invalid key:")

    def get_files(self):
        """ return a file list
        """
        return self._call_git('diff',
             '--cached',
             '--diff-filter=AM',
             '-U0',
             '--name-only').split("\n")

    def get_diff_rows(self, filename):
        """ search a newest/changed rows for <filename>
        """
        src = self._call_git("diff", "-U0", "--cached", filename).split("\n")[4:]
        rr = re.compile(r"^@@[^+]*\+(\d+)")
        res = []
        curr_pos = 0
        for s in src:
            if s.startswith('@@'):
                curr_pos = int(rr.findall(s)[0])
            if s.startswith('+'):
                res.append((curr_pos, s[1:]))
                curr_pos += 1   

        return res

