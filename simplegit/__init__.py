__author__ = "A.A.Konovalov"
__version__ = "0.3"


import re
import subprocess


__all__ = ('Git', 'GitException')


class GitException(Exception):
    pass


class Git(object):

    """Wrapper class for a GIT interface."""

    reg_range = re.compile(r"^@@[^+]*\+(\d+)")

    def __init__(self):
        try:
            self._version_str = self._call_git("--version")
        except OSError:
            raise GitException('git is currently not installed')

    @staticmethod
    def _call_git(*params):
        """ call a git command with params
        """
        p = subprocess.Popen(
            ["git"] + list(params),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False)
        exit_code = p.wait()
        if exit_code != 0:
            raise GitException("Error: git exit code = %s" % exit_code)

        return p.stdout.read().strip()

    @staticmethod
    def config(*options):
        """ run: git config <options>
        """
        return Git._call_git("config", *options)

    @staticmethod
    def get_param(param, default=None):
        """ get one param from git config
        """
        try:
            res = Git.config("--get", param)
            return res
        except GitException:
            return default

    @staticmethod
    def set_param(param, value, filename=""):
        """ set one parameter
        """
        if filename:
            Git.config("-f", filename, param, value)
        else:
            Git.config(param, value)

    @staticmethod
    def del_param(param):
        """ remove parameter
        """
        Git.config("--unset", param)

    @property
    def files(self):
        """ return a file list... or empty list
        """
        ret = self._call_git(
            'diff',
            '--cached',
            '--diff-filter=AM',
            '-U0',
            '--name-only')
        if ret:
            return ret.split('\n')
        else:
            return []

    def get_diff_rows(self, filename):
        """ search a newest/changed rows for <filename>
        """
        src = Git._call_git(
            'diff',
            '-U0',
            '--cached',
            filename).split('\n')[4:]

        result = []
        curr_pos = 0
        for s in src:
            if s.startswith('@@'):
                curr_pos = int(self.reg_range.findall(s)[0])
            if s.startswith('+'):
                result.append((curr_pos, s[1:]))
                curr_pos += 1

        return result

    @property
    def version_str(self):
        """Git version."""
        return self._version_str

