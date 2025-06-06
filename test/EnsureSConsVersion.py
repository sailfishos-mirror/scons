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

test = TestSCons.TestSCons()

import SCons

if SCons.__version__ != "__VERSION__":
    test.write('SConstruct', """\
DefaultEnvironment(tools=[])
env = Environment(tools=[])
env.EnsureSConsVersion(0, 0)
Exit(0)
""")
    test.run()

    test.write('SConstruct', """\
DefaultEnvironment(tools=[])
env = Environment(tools=[])
env.EnsureSConsVersion(1, 0)
Exit(0)
""")
    test.run()

    test.write('SConstruct', """\
DefaultEnvironment(tools=[])
env = Environment(tools=[])
env.EnsureSConsVersion(5, 0)
Exit(0)
""")
    test.run(status=2)

    test.write('SConstruct', """\
DefaultEnvironment(tools=[])
EnsureSConsVersion(2000, 0)
Exit(0)
""")
    test.run(status=2)

    test.write('SConstruct', """\
DefaultEnvironment(tools=[])
env = Environment(tools=[])
env.EnsureSConsVersion(*env.GetSConsVersion())
Exit(0)
""")
    test.run()

    test.write('SConstruct', """\
DefaultEnvironment(tools=[])
env = Environment(tools=[])
ver = env.GetSConsVersion()
env.EnsureSConsVersion(ver[0], ver[1], ver[2])
Exit(0)
""")
    test.run()


test.write('SConstruct', """\
import SCons

DefaultEnvironment(tools=[])
SCons.__version__ = '0.33.2'
EnsureSConsVersion(0, 33)
""")
test.run()

test.write('SConstruct', """\
import SCons

DefaultEnvironment(tools=[])
SCons.__version__ = '0.33.2'
EnsureSConsVersion(0, 33, 0)
""")
test.run()

test.write('SConstruct', """\
import SCons

DefaultEnvironment(tools=[])
SCons.__version__ = '0.33.2'
EnsureSConsVersion(0, 33, 1)
""")
test.run()

test.write('SConstruct', """\
import SCons

DefaultEnvironment(tools=[])
SCons.__version__ = '0.33.2'
EnsureSConsVersion(0, 33, 2)
""")
test.run()

test.write('SConstruct', """\
import SCons

DefaultEnvironment(tools=[])
SCons.__version__ = '0.33.2'
EnsureSConsVersion(0, 33, 3)
""")
test.run(status=2)

test.write('SConstruct', """\
import SCons

DefaultEnvironment(tools=[])
SCons.__version__ = '0.33.2'
EnsureSConsVersion(0, 34)
""")
test.run(status=2)

test.write('SConstruct', """\
import SCons

DefaultEnvironment(tools=[])
SCons.__version__ = '0.33.2'
EnsureSConsVersion(1, 0)
""")
test.run(status=2)

test.write('SConstruct', """\
import SCons

DefaultEnvironment(tools=[])
EnsureSConsVersion(*GetSConsVersion())
""")
test.run()

test.write('SConstruct', """\
import SCons

DefaultEnvironment(tools=[])
major, minor, patch = GetSConsVersion()
EnsureSConsVersion(major, minor, patch)
""")
test.run()

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
