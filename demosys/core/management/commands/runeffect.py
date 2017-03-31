"""
Run a specific effect
"""
import demosys

HELP = "Runs an effect"


def print_usage():
    print("Usage:")
    print("  runeffect <effectname>")


def run(args):
    effect_name = args[0] if args else None
    if effect_name is None:
        print_usage()
        return

    demosys.setup()
    demosys.run(runeffect=effect_name)
