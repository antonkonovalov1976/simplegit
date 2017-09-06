#!/usr/bin/env python
from __future__ import print_function

"""Example tool for check code length."""

__author__ = "A.A.Konovalov"
__version__ = "0.3"

from simplegit import Git


MAX_LINE_LENGTH_PARAM = "pre-commit.max-line-length"
MAX_LINE_LENGTH_PARAM_ENABLED = "pre-commit.max-line-length.enabled"


class GitHook(Git):

    """Simple git hook for a client side."""

    DEFAULT_SCREEN_WIDTH = 80

    def check_max_length(self, filename, default_line_length=80):
        """check max length of source lines."""
        # get a config
        max_line_length = self.get_param(
            MAX_LINE_LENGTH_PARAM,
            default_line_length
        )

        try:
            max_line_length = int(max_line_length)
        except ValueError:
            max_line_length = default_line_length

        # get a lines and check
        for n, s in self.get_diff_rows(filename):
            length = len(s)
            if length > max_line_length:
                print("%s:%d:Line has length %d but %d is allowed" %
                    (filename, n, length, max_line_length)
                )
                print("%s[...]" % s[:self.DEFAULT_SCREEN_WIDTH])
                return False

        return True

    def check_file(self, filename):
        """check one file."""
        if self.get_param(MAX_LINE_LENGTH_PARAM_ENABLED) != "false":
            res = self.check_max_length(
                filename,
                self.get_param(MAX_LINE_LENGTH_PARAM)
            )
            if not res:
                return False

        # ... another check-routine place here...
        return True

    def check(self):
        """check all files in a commit."""
        for filename in self.files:
            print(filename)
            if not self.check_file(filename):
                return False

        # ... otherwise check routines place here...
        return True


if __name__ == "__main__":
    print("[PRE-COMMIT HOOK] CHECK a files...")
    hook = GitHook()
    if hook.check():
        exit(0)
    else:
        exit(1)
