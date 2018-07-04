import os
from datetime import datetime

from PIL import Image

from demosys.conf import settings
from demosys import context


class Config:
    """Container for screenshot target"""
    target = None
    alignment = 1


def create(file_format='png', name=None):
    """
    Create a screenshot
    :param file_format: formats supported by PIL (png, jpeg etc)
    """
    dest = ""
    if settings.SCREENSHOT_PATH:
        if not os.path.exists(settings.SCREENSHOT_PATH):
            print("SCREENSHOT_PATH does not exist. creating: {}".format(settings.SCREENSHOT_PATH))
            os.makedirs(settings.SCREENSHOT_PATH)
        dest = settings.SCREENSHOT_PATH
    else:
        print("SCREENSHOT_PATH not defined in settings. Using cwd as fallback.")

    if not Config.target:
        Config.target = context.ctx().screen

    image = Image.frombytes(
        "RGB",
        (Config.target.width, Config.target.height), Config.target.read(alignment=Config.alignment)
    )
    image = image.transpose(Image.FLIP_TOP_BOTTOM)

    if not name:
        name = "{}.{}".format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f"), file_format)

    dest = os.path.join(dest, name)
    print("Creating screenshot:", dest)
    image.save(dest, format=file_format)
