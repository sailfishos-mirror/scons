#
# __COPYRIGHT__
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
#
# from typing import Dict, Any

__revision__ = "__FILE__ __REVISION__ __DATE__ __DEVELOPER__"

import os
import os.path
import unittest

import SCons.Node.FS
import SCons.Warnings
import SCons.Tool.MSCommon.vc

import TestCmd

original = os.getcwd()

test = TestCmd.TestCmd(workdir='')

os.chdir(test.workpath(''))

MSVCUnsupportedHostArch = SCons.Tool.MSCommon.vc.MSVCUnsupportedHostArch
MSVCUnsupportedTargetArch = SCons.Tool.MSCommon.vc.MSVCUnsupportedTargetArch

MS_TOOLS_VERSION='1.1.1'

class VswhereTestCase(unittest.TestCase):
    @staticmethod
    def _createVSWhere(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write("Created:%s"%f)

    def testDefaults(self):
        """
        Verify that msvc_find_vswhere() find's files in the specified paths
        """
        # import pdb; pdb.set_trace()
        vswhere_dirs = [os.path.splitdrive(p)[1] for p in SCons.Tool.MSCommon.vc.VSWHERE_PATHS]
        base_dir = test.workpath('fake_vswhere')
        test_vswhere_dirs = [os.path.join(base_dir,d[1:]) for d in  vswhere_dirs]

        SCons.Tool.MSCommon.vc.VSWHERE_PATHS = test_vswhere_dirs
        for vsw in test_vswhere_dirs:
            VswhereTestCase._createVSWhere(vsw)
            find_path = SCons.Tool.MSCommon.vc.msvc_find_vswhere()
            self.assertTrue(vsw == find_path, "Didn't find vswhere in %s found in %s"%(vsw, find_path))
            os.remove(vsw)

    # def specifiedVswherePathTest(self):
    #     "Verify that msvc.generate() respects VSWHERE Specified"


    


class MSVcTestCase(unittest.TestCase):

    @staticmethod
    def _createDummyCl(path, add_bin=True):
        """
        Creates a dummy cl.exe in the correct directory. 
        It will create all missing parent directories as well

        Args:
            path: Relative path to cl.exe for the version about to be tested.
        """

        # print("PATH:%s"%path)

        path = path.replace('\\', os.sep)
        if add_bin:
            create_path = os.path.join(path,'bin')
        else:
            create_path = path
        if create_path and not os.path.isdir(create_path):
            os.makedirs(create_path)
        
        create_this = os.path.join(create_path,'cl.exe')

        # print("Creating: %s"%create_this)
        with open(create_this,'w') as ct:
            ct.write('created')

        
    def runTest(self):
        """
        Check that all proper HOST_PLATFORM and TARGET_PLATFORM are handled.
        Verify that improper HOST_PLATFORM and/or TARGET_PLATFORM are properly handled.
        by SCons.Tool.MSCommon.vc._check_cl_exists_in_vc_dir()
        """

        check = SCons.Tool.MSCommon.vc._check_cl_exists_in_vc_dir

        env={'TARGET_ARCH':'x86'}
        _, clpathcomps = SCons.Tool.MSCommon.vc._LE2015_HOST_TARGET_BATCHARG_CLPATHCOMPS[('x86','x86')]
        path = os.path.join('.', *clpathcomps)
        MSVcTestCase._createDummyCl(path, add_bin=False)
 
        # print("retval:%s"%check(env, '.', '8.0'))


        # Setup for 14.1 (VS2017) and later tests

        # Create the VC minor/major version file
        tools_version_file = SCons.Tool.MSCommon.vc._VC_TOOLS_VERSION_FILE
        tools_dir = os.path.dirname(tools_version_file)
        if not os.path.isdir(tools_dir):
            os.makedirs(tools_dir)
        try:
            with open(tools_version_file, 'w') as tf:
                tf.write(MS_TOOLS_VERSION)
        except IOError as e:
            print("Failed trying to write :%s :%s"%(tools_version_file, e))


        # Now walk all the valid combinations of host/target for 14.1 (VS2017) and later
        vc_ge2017_list = SCons.Tool.MSCommon.vc._GE2017_HOST_TARGET_CFG.all_pairs

        for host, target in vc_ge2017_list:
            batfile, clpathcomps = SCons.Tool.MSCommon.vc._GE2017_HOST_TARGET_BATCHFILE_CLPATHCOMPS[(host,target)]
            # print("GT 14 Got: (%s, %s) -> (%s, %s)"%(host,target,batfile,clpathcomps))

            env={'TARGET_ARCH':target, 'HOST_ARCH':host}
            path = os.path.join('.', 'Tools', 'MSVC', MS_TOOLS_VERSION, *clpathcomps)
            MSVcTestCase._createDummyCl(path, add_bin=False)
            result=check(env, '.', '14.1')
            # print("for:(%s, %s) got :%s"%(host, target, result))
            self.assertTrue(result, "Checking host: %s target: %s" % (host, target))

        # Now test bogus value for HOST_ARCH
        env={'TARGET_ARCH':'x86', 'HOST_ARCH':'GARBAGE'}
        try:
            result=check(env, '.', '14.1')
            # print("for:%s got :%s"%(env, result))
            self.assertFalse(result, "Did not fail with bogus HOST_ARCH host: %s target: %s" % (env['HOST_ARCH'], env['TARGET_ARCH']))
        except MSVCUnsupportedHostArch:
            pass
        else:
            self.fail('Did not fail when HOST_ARCH specified as: %s'%env['HOST_ARCH'])

        # Now test bogus value for TARGET_ARCH
        env={'TARGET_ARCH':'GARBAGE', 'HOST_ARCH':'x86'}
        try:
            result=check(env, '.', '14.1')
            # print("for:%s got :%s"%(env, result))
            self.assertFalse(result, "Did not fail with bogus TARGET_ARCH host: %s target: %s" % (env['HOST_ARCH'], env['TARGET_ARCH']))
        except MSVCUnsupportedTargetArch:
            pass
        else:
            self.fail('Did not fail when TARGET_ARCH specified as: %s' % env['TARGET_ARCH'])

        # Test 14.0 (VS2015) to 8.0 (VS2005) versions
        vc_le2015_list = SCons.Tool.MSCommon.vc._LE2015_HOST_TARGET_CFG.all_pairs

        for host, target in vc_le2015_list:
            batarg, clpathcomps = SCons.Tool.MSCommon.vc._LE2015_HOST_TARGET_BATCHARG_CLPATHCOMPS[(host, target)]
            # print("LE 14 Got: (%s, %s) -> (%s, %s)"%(host,target,batarg,clpathcomps))
            env={'TARGET_ARCH':target, 'HOST_ARCH':host}
            path = os.path.join('.', *clpathcomps)
            MSVcTestCase._createDummyCl(path, add_bin=False)
            result=check(env, '.', '9.0')
            # print("for:(%s, %s) got :%s"%(host, target, result))
            self.assertTrue(result, "Checking host: %s target: %s" % (host, target))

        # Now test bogus value for HOST_ARCH
        env={'TARGET_ARCH':'x86', 'HOST_ARCH':'GARBAGE'}
        try:
            result=check(env, '.', '9.0')
            # print("for:%s got :%s"%(env, result))
            self.assertFalse(result, "Did not fail with bogus HOST_ARCH host: %s target: %s"%(env['HOST_ARCH'], env['TARGET_ARCH']))
        except MSVCUnsupportedHostArch:
            pass
        else:
            self.fail('Did not fail when HOST_ARCH specified as: %s' % env['HOST_ARCH'])

        # Now test bogus value for TARGET_ARCH
        env={'TARGET_ARCH':'GARBAGE', 'HOST_ARCH':'x86'}
        try:
            result=check(env, '.', '9.0')
            # print("for:%s got :%s"%(env, result))
            self.assertFalse(result, "Did not fail with bogus TARGET_ARCH host: %s target: %s"%(env['HOST_ARCH'], env['TARGET_ARCH']))
        except MSVCUnsupportedTargetArch:
            pass
        else:
            self.fail('Did not fail when TARGET_ARCH specified as: %s' % env['TARGET_ARCH'])

        # Test 7.1 (VS2003) and earlier
        vc_le2003_list = SCons.Tool.MSCommon.vc._LE2003_HOST_TARGET_CFG.all_pairs

        for host, target in vc_le2003_list:
            # print("LE 7.1 Got: (%s, %s)"%(host,target))
            env={'TARGET_ARCH':target, 'HOST_ARCH':host}
            path = os.path.join('.')
            MSVcTestCase._createDummyCl(path)
            result=check(env, '.', '6.0')
            # print("for:(%s, %s) got :%s"%(host, target, result))
            self.assertTrue(result, "Checking host: %s target: %s" % (host, target))

        # Now test bogus value for HOST_ARCH
        env={'TARGET_ARCH':'x86', 'HOST_ARCH':'GARBAGE'}
        try:
            result=check(env, '.', '6.0')
            # print("for:%s got :%s"%(env, result))
            self.assertFalse(result, "Did not fail with bogus HOST_ARCH host: %s target: %s" % (env['HOST_ARCH'], env['TARGET_ARCH']))
        except MSVCUnsupportedHostArch:
            pass
        else:
            self.fail('Did not fail when HOST_ARCH specified as: %s' % env['HOST_ARCH'])

        # Now test bogus value for TARGET_ARCH
        env={'TARGET_ARCH':'GARBAGE', 'HOST_ARCH':'x86'}
        try:
            result=check(env, '.', '6.0')
            # print("for:%s got :%s"%(env, result))
            self.assertFalse(result, "Did not fail with bogus TARGET_ARCH host: %s target: %s" % (env['HOST_ARCH'], env['TARGET_ARCH']))
        except MSVCUnsupportedTargetArch:
            pass
        else:
            self.fail('Did not fail when TARGET_ARCH specified as: %s' % env['TARGET_ARCH'])



if __name__ == "__main__":
    unittest.main()
