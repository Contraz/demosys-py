import os
from datetime import datetime

from PIL import Image

from demosys import context
from demosys.conf import settings


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
        Config.target = context.window().fbo

    image = Image.frombytes(
        "RGB",
        (Config.target.viewport[2], Config.target.viewport[3]),
        Config.target.read(viewport=Config.target.viewport, alignment=Config.alignment),
    )
    image = image.transpose(Image.FLIP_TOP_BOTTOM)

    if not name:
        name = "{}.{}".format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f"), file_format)

    dest = os.path.join(dest, name)
    print("Creating screenshot:", dest)
    image.save(dest, format=file_format)
