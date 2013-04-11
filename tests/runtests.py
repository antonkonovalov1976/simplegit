#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import unittest

# add path with main package
sys.path.insert(0, os.path.abspath(__file__ + "/../.."))


from simplegit import Git


class TestGitSimple(unittest.TestCase):

    def setUp(self):
        self.git = Git()

    def test1(self):
        self.git.set_param("foo.bar", "100500")
        ret = self.git.get_param("foo.bar")
        self.assertEqual(100500, int(ret))
        
    def test2(self):
        self.git.del_param("foo.bar") 
        ret = self.git.get_param("foo.bar", 100)
        self.assertEqual(100, ret)
        

if __name__ == "__main__":
    if Git().check_git():
        unittest.main() 
    else:
        print "ERROR: please, install git service!"    
