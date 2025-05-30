#! /usr/bin/env python
#
# SCons - a Software Constructor
#
# MIT License
#
# Copyright The SCons Foundation
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""Show or convert the configuration of an SCons cache directory.

A cache of derived files is stored by file signature.
The files are split into directories named by the first few
digits of the signature. The prefix length used for directory
names can be changed by this script.
"""
__revision__ = "__FILE__ __REVISION__ __DATE__ __DEVELOPER__"

__version__ = "__VERSION__"

__build__ = "__BUILD__"

__buildsys__ = "__BUILDSYS__"

__date__ = "__DATE__"

__developer__ = "__DEVELOPER__"


import os
import sys

# python compatibility check
if sys.version_info < (3, 7, 0):
    msg = "scons: *** SCons version %s does not run under Python version %s.\n\
Python >= 3.7.0 is required.\n"
    sys.stderr.write(msg % (__version__, sys.version.split()[0]))
    sys.exit(1)

# Strip the script directory from sys.path so on case-insensitive
# (WIN32) systems Python doesn't think that the "scons" script is the
# "SCons" package.
script_dir = os.path.dirname(os.path.realpath(__file__))
script_path = os.path.realpath(os.path.dirname(__file__))
if script_path in sys.path:
    sys.path.remove(script_path)

libs = []

if "SCONS_LIB_DIR" in os.environ:
    libs.append(os.environ["SCONS_LIB_DIR"])

# running from source takes 2nd priority (since 2.3.2), following SCONS_LIB_DIR
source_path = os.path.join(script_path, os.pardir)
if os.path.isdir(source_path):
    libs.append(source_path)

# add local-install locations
local_version = 'scons-local-' + __version__
local = 'scons-local'
if script_dir:
    local_version = os.path.join(script_dir, local_version)
    local = os.path.join(script_dir, local)
if os.path.isdir(local_version):
    libs.append(os.path.abspath(local_version))
if os.path.isdir(local):
    libs.append(os.path.abspath(local))

scons_version = 'scons-%s' % __version__

sys.path = libs + sys.path

##############################################################################
# END STANDARD SCons SCRIPT HEADER
##############################################################################
from SCons.Utilities.ConfigureCache import main

if __name__ == "__main__":
    main()
