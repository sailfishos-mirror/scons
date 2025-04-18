# SPDX-License-Identifier: MIT
#
# Copyright The SCons Foundation

"""Command-line processing for building SCons."""

import os
import platform
import time

import SCons.Errors
from SCons.Script import ARGUMENTS


class BuildCommandLine:

    git = None

    def init_command_line_variables(self):
        self.command_line_variables = [
            (
                "BUILDDIR=",
                "The directory to build the packages in. "
                "The default is './build'."
            ),
            (
                "BUILD_ID=",
                "An identifier for the specific build. "
                "The default is to generate an id from 'git rev-parse'."
            ),
            (
                "BUILD_SYSTEM=",
                "The system on which the packages were built. "
                "The default is the inspected hostname. "
                "If env var SOURCE_DATE_EPOCH is set, "
                "defaults to '_reproducible'."
            ),
            (
                "CHECKPOINT=",
                "Indicates a checkpoint release, "
                "which will be appended to the VERSION string. "
                "A value of 'd' selects a date checkpoint "
                "(a string of 'd' plus today's date in the format YYYMMDD). "
                "A value of 'r' selects a revision checkpoint "
                "(string of 'r' plus the revision number). "
                "Any other value will be used as is. There is no default."
            ),
            (
                "DATE=",
                "The date string representing when the packaging "
                "build occurred.  The default is the day and time "
                "the SConstruct file was invoked, in the format "
                "YYYY/MM/DD HH:MM:SS. If env var SOURCE_DATE_EPOCH is set, "
                "its value (must be a UNIX-style timestamp) is used."
            ),
            (
                "DEVELOPER=",
                "The developer who created the packages. "
                "The default is the first set environment "
                "variable from the list $USERNAME, $LOGNAME, $USER."
                "If env var SOURCE_DATE_EPOCH is set, "
                "defaults to '_reproducible'."
            ),
            (
                "REVISION=",
                "The revision number of the source being built. "
                "The default is the git hash returned "
                "'git rev-parse HEAD', with an appended string of "
                "'[MODIFIED]' if there are any changes in the "
                "working copy."
            ),
            (
                "VERSION=",
                "The SCons version being packaged.  The default "
                f"is the hard-coded value '{self.default_version}' "
                "from this SConstruct file."
            ),
            (
                "SKIP_DOC=",
                "Skip building documents. The value can be 'pdf', 'api', "
                "''all' or 'none'. A comma-separated list is also allowed. "
                "Do not set this for an official release build. "
                "The default is 'none' (build all docs)"
            ),
        ]

    def __init__(self, default_version="99.99.99"):
        self.date = None
        self.default_version = default_version
        self.developer = None
        self.build_dir = None
        self.build_system = None
        self.version = None
        self.revision = None
        self.git_status_lines = []
        self.git_hash = None

        self.init_command_line_variables()

    def set_date(self):
        """
        Determine the release date and the pattern to match a date
        Mon, 05 Jun 2010 21:17:15 -0700
        NEW DATE WILL BE INSERTED HERE
        """

        min = (time.altzone if time.daylight else time.timezone) // 60
        hr = min // 60
        min = -(min % 60 + hr * 100)
        # TODO: is it better to take the date of last rev? Externally:
        #   SOURCE_DATE_EPOCH =`git log -1 --pretty=%ct`
        self.date = (
            time.strftime(
                '%a, %d %b %Y %X',
                time.localtime(int(os.environ.get('SOURCE_DATE_EPOCH', time.time()))),
            )
            + ' %+.4d' % min
        )
        # Alternate proposal:
        # from datetime import datetime, timezone
        # timestamp = int(os.environ.get('SOURCE_DATE_EPOCH', time.time()))
        # try:
        #     dt = datetime.fromtimestamp(timestamp, timezone.utc)
        # except (OverflowError, OSError):
        #     # SOURCE_DATE_EPOCH spec: If the value is malformed,
        #     #  the build process SHOULD exit with a non-zero error code.
        #     # Python: This may raise OverflowError, if the timestamp is out
        #     #  of the range of values supported by the platform C gmtime()
        #     #  function, and OSError on gmtime() failure. It’s common for
        #     #  this to be restricted to years in 1970 through 2038.
        #     raise SCons.Errors.UserError(
        #         "Invalid value for SOURCE_DATE_EPOCH environment var, "
        #         "please correct to a valid timestamp"
        #     )
        # self.date = dt.strftime("%a, %d %b %Y %X %Z")  # or %z for numeric

    def process_command_line_vars(self):
        #
        # Now grab the information that we "build" into the files.
        #
        self.date = ARGUMENTS.get('DATE')
        if not self.date:
            self.set_date()

        self.developer = ARGUMENTS.get('DEVELOPER')
        if not self.developer:
            for variable in ['USERNAME', 'LOGNAME', 'USER']:
                self.developer = os.environ.get(variable)
                if self.developer:
                    break
            if os.environ.get('SOURCE_DATE_EPOCH'):
                self.developer = '_reproducible'

        self.build_system = ARGUMENTS.get('BUILD_SYSTEM')
        if not self.build_system:
            if os.environ.get('SOURCE_DATE_EPOCH'):
                self.build_system = '_reproducible'
            else:
                self.build_system = platform.node().split('.')[0]

        self.version = ARGUMENTS.get('VERSION', '')
        if not self.version:
            self.version = self.default_version

        if BuildCommandLine.git:
            cmd = f"{BuildCommandLine.git} ls-files 2> /dev/null"
            with os.popen(cmd, "r") as p:
                self.git_status_lines = p.readlines()

        self.revision = ARGUMENTS.get('REVISION', '')

        def _generate_build_id(revision):
            return revision

        generate_build_id = _generate_build_id

        if not self.revision and BuildCommandLine.git:
            with os.popen(
                f"{BuildCommandLine.git} rev-parse HEAD 2> /dev/null", "r"
            ) as p:
                self.git_hash = p.read().strip()

            def _generate_build_id_git(revision):
                result = self.git_hash
                if [l for l in self.git_status_lines if 'modified' in l]:
                    result = result + '[MODIFIED]'
                return result

            generate_build_id = _generate_build_id_git
            self.revision = self.git_hash

        self.checkpoint = ARGUMENTS.get('CHECKPOINT', '')
        if self.checkpoint:
            if self.checkpoint == 'd':
                self.checkpoint = time.strftime('%Y%m%d', time.localtime(time.time()))
            elif self.checkpoint == 'r':
                self.checkpoint = 'r' + self.revision
            self.version = self.version + '.beta.' + self.checkpoint

        self.build_id = ARGUMENTS.get('BUILD_ID')
        if self.build_id is None:
            if self.revision:
                self.build_id = generate_build_id(self.revision)
            else:
                self.build_id = ''

        # Re-exporting LD_LIBRARY_PATH is necessary if the Python version was
        # built with the --enable-shared option.
        self.ENV = {'PATH': os.environ['PATH']}
        for key in ['LOGNAME', 'PYTHONPATH', 'LD_LIBRARY_PATH']:
            if key in os.environ:
                self.ENV[key] = os.environ[key]

        self.build_dir = ARGUMENTS.get('BUILDDIR', 'build')
        if not os.path.isabs(self.build_dir):
            self.build_dir = os.path.normpath(os.path.join(os.getcwd(), self.build_dir))
