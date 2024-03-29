# SPDX-License-Identifier: MIT
#
# Copyright The SCons Foundation

"""
Command wrapper taking arguments, for testing SCons.

Writes the command name and argument list to file "wrapper.out",
then passes the command line on to subprocess.
No checking is done.
"""
import os
import sys
import subprocess

if __name__ == '__main__':
    path = os.path.join(os.path.dirname(os.path.relpath(__file__)), 'wrapper.out')
    with open(path, 'a') as f:
        f.write("wrapper_with_args.py %s\n" % " ".join(sys.argv[1:]))
    subprocess.run(sys.argv[1:], check=False)
