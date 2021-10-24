import json
import re
from flask import jsonify
import subprocess


class Utils:
    def __init__(self) -> None:
        pass

    def _validate_package_name(self, package_name: str):
        """Returns whether package_name is installed.

        Checks whether package_name is installed. package_name could be a
        partial name. Returns the full package name if only one entry matches.
        if more than one matches, it exits with an error.

        To avoid using partial name matches, -f should be used from command
        line.

        Args:
            package_name: A string representing the name of the application to
                be targeted.

        Returns:
            A string representing a validated full package name.
        """
        cmd = ('adb', 'shell', 'pm', 'list', 'packages')
        outstr = subprocess.run(cmd, check=True, encoding='utf-8',
                                capture_output=True).stdout.strip()

        partial_pkg_regexp = fr'^package:(.*{re.escape(package_name)}.*)$'

        regexp = partial_pkg_regexp

        # IGNORECASE is needed because some package names use uppercase letters.
        matches = re.findall(regexp, outstr, re.MULTILINE | re.IGNORECASE)
        if len(matches) == 0:
            return jsonify([f'No installed package matches "{package_name}"'])

        if len(matches) >= 1:
            return jsonify(matches)
