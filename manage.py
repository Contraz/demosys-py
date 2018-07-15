#!/usr/bin/env python3
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DEMOSYS_SETTINGS_MODULE", "examples.settings")

    from demosys.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
