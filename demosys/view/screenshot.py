import os
from datetime import datetime
from PIL import Image
from OpenGL import GL
from demosys.conf import settings


def create(format='png', name=None):
    """
    Create a screenshot
    :param format: formats supported by PIL (png, jpeg etc)
    """
    # Avoid circular import
    from demosys.view.controller import WINDOW

    dest = ""
    if settings.SCREENSHOT_PATH:
        if not os.path.exists(settings.SCREENSHOT_PATH):
            print("SCREENSHOT_PATH does not exist. creating: {}".format(settings.SCREENSHOT_PATH))
            os.makedirs(settings.SCREENSHOT_PATH)
        dest = settings.SCREENSHOT_PATH
    else:
        print("SCREENSHOT_PATH not defined in settings. Using cwd as fallback.")

    # x, y, width, height = GL.glGetIntegerv(GL.GL_VIEWPORT)
    x, y, width, height = 0, 0, WINDOW.buffer_width, WINDOW.buffer_height

    GL.glPixelStorei(GL.GL_PACK_ALIGNMENT, 1)

    data = GL.glReadPixels(x, y, width, height, GL.GL_RGB, GL.GL_UNSIGNED_BYTE)

    image = Image.frombytes("RGB", (width, height), data)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    if not name:
        name = "{}.{}".format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"), format)

    print("Creating screenshot:", name)
    image.save(os.path.join(dest, name), format=format)
