#!/usr/bin/env python
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

"""
Template for end-to-end test file.
Replace this with a description of the test.
"""

import TestSCons

test = TestSCons.TestSCons()

test.skip_if_not_msvc()

# include all of msvc_fixture's files
test.dir_fixture('../msvc_fixture','src')

# Then we'll replace the SConstruct with one specific to this test.
test.file_fixture('fixture/SConstruct',
                  'SConstruct')

test.run(arguments='.')

test.must_exist(test.workpath('output1/test.exe'))
test.must_exist(test.workpath('output1/test.res'))
test.must_exist(test.workpath('output1/test.pdb'))
test.must_exist(test.workpath('output1/StdAfx-1.pch'))
test.must_exist(test.workpath('output1/StdAfx-1.obj'))

test.run(arguments="-c .")
test.run(arguments="DISABLE_PCH=1 .")

test.must_exist(test.workpath('output1/test.exe'))
test.must_exist(test.workpath('output1/test.res'))
test.must_exist(test.workpath('output1/test.pdb'))
test.fail_test(condition = ('/Yuoutput1/StdAfx.h' in test.stdout()), message="Shouldn't have output1/YuStdAfx.h in compile line when PCH is disabled")

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
