import os


def create(**kwargs):
    """
    Return a string representing a new default settings file for a project
    """
    template_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'default.py')
    data = ""
    with open(template_file, 'r') as fd:
        data = fd.read()

    header = (
        '"""\n'
        'Auto generated settings file for project {}\n'
        '"""\n'
    ).format(kwargs.get('name'))

    return header + data
