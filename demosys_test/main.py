"""Entrypoint from entrypoint in setup.py"""
import os
import sys


def main():
    os.environ["DEMOSYS_SETTINGS_MODULE"] = "demosys_test.settings"
    from demosys.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
