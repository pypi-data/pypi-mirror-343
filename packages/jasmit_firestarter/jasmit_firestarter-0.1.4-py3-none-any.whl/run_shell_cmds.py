'''
run_shell_cmds.py
Standard function for consistent method to run shell commands
'''
from subprocess import Popen, PIPE


def run_shell_cmds(cmds):
    process = Popen(
        cmds,
        shell=True,
        stdout=PIPE,
        stderr=PIPE
    )
#         universal_newlines=True

    try:
        stdout, stderr = process.communicate()
    finally:
        rc = process.returncode

    return rc, stdout, stderr
