import collections
import logging
import os
import subprocess

PackageInfo = collections.namedtuple('PackageInfo',
                                     ['package', 'activity', 'cmdline_file', 'devtools_socket',
                                      'test_package'])
ERROR_EXIT_CODE = 1
WARNING_EXIT_CODE = 88
