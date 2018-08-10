#!/usr/bin/env python3
import os
import sys


if __name__ == "__main__":
    os.environ.setdefault("DEMOSYS_SETTINGS_MODULE", "{project_name}.settings")

    from demosys.management import execute_from_command_line
    execute_from_command_line(sys.argv)
