import os
from datetime import datetime

from PIL import Image

from demosys.conf import settings
from demosys import context


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

    fbo = context.ctx().screen
    image = Image.frombytes("RGB", (fbo.width, fbo.height), fbo.read())
    image = image.transpose(Image.FLIP_TOP_BOTTOM)

    if not name:
        name = "{}.{}".format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f"), file_format)

    print("Creating screenshot:", name)
    image.save(os.path.join(dest, name), format=file_format)
