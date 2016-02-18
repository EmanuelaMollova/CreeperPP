import subprocess
from subprocess import check_output

class ShellService(object):
    @classmethod
    def execute(self, command, working_dir):
        return check_output(command.split(), cwd = working_dir)
