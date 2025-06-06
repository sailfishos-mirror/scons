#!/usr/bin/env python
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

import os

import TestSCons
from TestCmd import IS_WINDOWS

test = TestSCons.TestSCons()

try:
    import ninja
except ImportError:
    test.skip_test("Could not find 'ninja'; skipping test.\n")

_python_ = TestSCons._python_
_exe = TestSCons._exe

ninja_bin = TestSCons.NINJA_BINARY

test.dir_fixture('ninja-fixture')

test.file_fixture('ninja_test_sconscripts/sconstruct_default_targets', 'SConstruct')

# this test has had some hangs on the GitHut Windows runner, add timeout.

# generate simple build
test.run(stdout=None, timeout=120)
test.must_contain_all_lines(test.stdout(), ['Generating: build.ninja'])
test.must_contain_all(test.stdout(), 'Executing:')
test.must_contain_all(test.stdout(), f'ninja{_exe} -f')
test.must_not_exist([test.workpath('out1.txt')])
test.must_exist([test.workpath('out2.txt')])

# clean build and ninja files
test.run(arguments='-c', stdout=None, timeout=120)
test.must_contain_all_lines(test.stdout(), ['Removed out2.txt', 'Removed build.ninja'])

# only generate the ninja file
test.run(arguments='--disable-execute-ninja', stdout=None, timeout=120)
test.must_contain_all_lines(test.stdout(), ['Generating: build.ninja'])
test.must_not_exist(test.workpath('out1.txt'))
test.must_not_exist(test.workpath('out2.txt'))

# run ninja independently
program = test.workpath('run_ninja_env.bat') if IS_WINDOWS else ninja_bin
test.run(program=program, stdout=None, timeout=120)
test.must_not_exist([test.workpath('out1.txt')])
test.must_exist(test.workpath('out2.txt'))

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
