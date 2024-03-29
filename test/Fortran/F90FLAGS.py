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

import TestSCons

_python_ = TestSCons._python_

test = TestSCons.TestSCons()
_exe = TestSCons._exe

test.file_fixture('mylink.py')
test.file_fixture(['fixture', 'myfortran_flags.py'])

test.write('SConstruct', """
env = Environment(LINK = r'%(_python_)s mylink.py',
                  LINKFLAGS = [],
                  F90 = r'%(_python_)s myfortran_flags.py g90',
                  F90FLAGS = '-x',
                  FORTRAN = r'%(_python_)s myfortran_flags.py fortran',
                  FORTRANFLAGS = '-y')
env.Program(target = 'test01', source = 'test01.f')
env.Program(target = 'test02', source = 'test02.F')
env.Program(target = 'test03', source = 'test03.for')
env.Program(target = 'test04', source = 'test04.FOR')
env.Program(target = 'test05', source = 'test05.ftn')
env.Program(target = 'test06', source = 'test06.FTN')
env.Program(target = 'test07', source = 'test07.fpp')
env.Program(target = 'test08', source = 'test08.FPP')
env.Program(target = 'test11', source = 'test11.f90')
env.Program(target = 'test12', source = 'test12.F90')
""" % locals())

test.write('test01.f',   "This is a .f file.\n#link\n#fortran\n")
test.write('test02.F',   "This is a .F file.\n#link\n#fortran\n")
test.write('test03.for', "This is a .for file.\n#link\n#fortran\n")
test.write('test04.FOR', "This is a .FOR file.\n#link\n#fortran\n")
test.write('test05.ftn', "This is a .ftn file.\n#link\n#fortran\n")
test.write('test06.FTN', "This is a .FTN file.\n#link\n#fortran\n")
test.write('test07.fpp', "This is a .fpp file.\n#link\n#fortran\n")
test.write('test08.FPP', "This is a .FPP file.\n#link\n#fortran\n")
test.write('test11.f90', "This is a .f90 file.\n#link\n#g90\n")
test.write('test12.F90', "This is a .F90 file.\n#link\n#g90\n")

test.run(arguments = '.', stderr = None)

test.must_match('test01' + _exe, " -c -y\nThis is a .f file.\n")
test.must_match('test02' + _exe, " -c -y\nThis is a .F file.\n")
test.must_match('test03' + _exe, " -c -y\nThis is a .for file.\n")
test.must_match('test04' + _exe, " -c -y\nThis is a .FOR file.\n")
test.must_match('test05' + _exe, " -c -y\nThis is a .ftn file.\n")
test.must_match('test06' + _exe, " -c -y\nThis is a .FTN file.\n")
test.must_match('test07' + _exe, " -c -y\nThis is a .fpp file.\n")
test.must_match('test08' + _exe, " -c -y\nThis is a .FPP file.\n")
test.must_match('test11' + _exe, " -c -x\nThis is a .f90 file.\n")
test.must_match('test12' + _exe, " -c -x\nThis is a .F90 file.\n")



fc = 'f90'
g90 = test.detect_tool(fc)

if g90:

    test.file_fixture('wrapper.py')

    test.write('SConstruct', """
foo = Environment(F90 = '%(fc)s')
f90 = foo.Dictionary('F90')
bar = foo.Clone(F90 = r'%(_python_)s wrapper.py ' + f90)
foo.Program(target = 'foo', source = 'foo.f90')
bar.Program(target = 'bar', source = 'bar.f90')
""" % locals())

    test.write('foo.f90', r"""
      PROGRAM FOO
      PRINT *,'foo.f90'
      END
""")

    test.write('bar.f90', r"""
      PROGRAM BAR
      PRINT *,'bar.f90'
      END
""")

    test.run(arguments = 'foo' + _exe, stderr = None)

    test.run(program = test.workpath('foo'), stdout =  " foo.f90\n")

    test.must_not_exist('wrapper.out')

    import sys
    if sys.platform[:5] == 'sunos':
        test.run(arguments = 'bar' + _exe, stderr = None)
    else:
        test.run(arguments = 'bar' + _exe)

    test.run(program = test.workpath('bar'), stdout =  " bar.f90\n")

    test.must_match('wrapper.out', "wrapper.py\n")

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
