import os
from datetime import datetime
from PIL import Image
from OpenGL import GL
from demosys.conf import settings


def create(format='png'):
    """
    Create a screenshot
    :param format: formats supported by PIL (png, jpeg etc)
    """
    dest = ""
    if not settings.SCREENSHOT_PATH:
        print("SCREENSHOT_PATH not defined in settings. Using cwd as fallback.")

    if settings.SCREENSHOT_PATH:
        if os.path.exists(settings.SCREENSHOT_PATH):
            dest = settings.SCREENSHOT_PATH
        else:
            print("SCREENSHOT_PATH {} does not exist. Using cwd as fallback".format(settings.SCREENSHOT_PATH))

    x, y, width, height = GL.glGetIntegerv(GL.GL_VIEWPORT)
    print("Screenshot viewport:", x, y, width, height)
    GL.glPixelStorei(GL.GL_PACK_ALIGNMENT, 1)

    data = GL.glReadPixels(x, y, width, height, GL.GL_RGB, GL.GL_UNSIGNED_BYTE)

    image = Image.frombytes("RGB", (width, height), data)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    name = "{}.{}".format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"), format)
    image.save(os.path.join(dest, name), format=format)
