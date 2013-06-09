#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import unittest

# add path with main package
p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, p)

from simplegit import Git, GitException


class TestGitSimple(unittest.TestCase):

    def setUp(self):
        self.git = Git()

    def test0(self):
        # test GitException
        self.assertRaises(
            GitException,
            lambda: self.git.set_param("foobar", "1234"))

    def test1(self):
        # test basic actions
        self.git.set_param("foo.bar", "100500")
        ret = self.git.get_param("foo.bar")
        self.assertEqual(100500, int(ret))
        self.git.del_param("foo.bar")
        ret = self.git.get_param("foo.bar", 100)
        self.assertEqual(100, ret)


if __name__ == "__main__":
    if Git().check_git():
        unittest.main()
    else:
        print "ERROR: please, install git service!"
