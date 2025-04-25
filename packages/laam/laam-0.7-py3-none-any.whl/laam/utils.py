# vim: set ts=4
#
# Copyright 2025-present Linaro Limited
#
# SPDX-License-Identifier: MIT

import contextlib
import sys


def print_error(ret, expected=200) -> bool:
    if ret.status_code == expected:
        return False

    print("Unable to call the appliance API", file=sys.stderr)
    print(f"Code: {ret.status_code}", file=sys.stderr)
    with contextlib.suppress(Exception):
        print(f"Error: {ret.json()['detail']}", file=sys.stderr)
    return True
