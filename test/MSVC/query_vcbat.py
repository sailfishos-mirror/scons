#!/usr/bin/python
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

import TestSCons

# TODO: this test seems to have been stripped to the basics...
#   is it still worth keeping?

test = TestSCons.TestSCons(match = TestSCons.match_re)
test.skip_if_not_msvc()

#####
# Test the basics

test.write('SConstruct', """
#from SCons.Tool.MSCommon.misc import FindMSVSBatFile, \\
#                                       ParseBatFile, \\
#                                       MergeMSVSBatFile
from SCons.Tool.MSCommon import query_versions
#env = Environment(tools=['mingw'])
DefaultEnvironment(tools=[])
#for v in [9, 8, 7.1, 7]:
#    print " ==== Testing for version %s ==== " % str(v)
#    bat = FindMSVSBatFile(v)
#    print bat
#    if bat:
#        d = ParseBatFile(bat)
#        for k, v in d.items():
#            print k, v
#MergeMSVSBatFile(env, 9.0)
#print(env['ENV']['PATH'])
print(query_versions(env=None))
""")

test.run(stderr=None)
test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
