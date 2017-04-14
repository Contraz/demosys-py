

def create(settings):
    """
    Return a string representation of the settings.
    This is an extremely ugly way of doing this, but it works for now!
    """
    # FIXME: Use a template system for generating settings file
    data = "# Auto generated settings file\n" \
           "import os\n" \
           "PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))\n\n"
    for name in settings.__ORDER__:
        value = getattr(settings, name)
        if isinstance(value, dict):
            value = ",\n".join('    "{}": {}'.format(k, to_s(v)) for k, v in value.items())
            data += "%s = {\n%s\n}\n\n" % (name, value)
        elif isinstance(value, tuple):
            value = ",\n".join("    {}".format(to_s(v)) for v in value)
            data += "{} = (\n{})\n\n".format(name, value)
        elif value is None:
            data += "{} = {}\n\n".format(name, value)

    return data


def to_s(t):
    if isinstance(t, str):
        return '"{}"'.format(t)
    else:
        return str(t)
