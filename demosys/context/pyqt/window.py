import moderngl
from PyQt5 import QtCore, QtOpenGL, QtWidgets

from demosys.context.base import BaseWindow
from demosys import context

from .keys import Keys


class Window(BaseWindow):
    """
    Window using PyQt5.

    This is the recommended window if you want your project to work
    on most platforms out of the box without any binary dependecies.
    """
    keys = Keys

    def __init__(self):
        """
        Creates a pyqt application and window overriding the
        built in event loop. Sets up keyboard and mouse events
        and creates a ``monderngl.Context``.
        """
        super().__init__()
        self._closed = False

        # Specify OpenGL context parameters
        gl = QtOpenGL.QGLFormat()
        gl.setVersion(self.gl_version.major, self.gl_version.minor)
        gl.setProfile(QtOpenGL.QGLFormat.CoreProfile)
        gl.setDepthBufferSize(24)
        gl.setDoubleBuffer(True)
        gl.setSwapInterval(1 if self.vsync else 0)

        if self.samples > 1:
            gl.setSampleBuffers(True)
            gl.setSamples(self.samples)

        # We need an application object, but we are not using the event loop
        self.app = QtWidgets.QApplication([])

        # Create the OpenGL widget
        self.widget = QtOpenGL.QGLWidget(gl)
        self.widget.setWindowTitle(self.title)

        # Fetch desktop size
        if self.fullscreen:
            rect = QtWidgets.QDesktopWidget().screenGeometry()
            self.width = rect.width()
            self.height = rect.height()
            self.buffer_width = rect.width() * self.widget.devicePixelRatio()
            self.buffer_height = rect.height() * self.widget.devicePixelRatio()

        if self.resizable:
            size_policy = QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Expanding,
            )
            self.widget.setSizePolicy(size_policy)
            self.widget.resize(self.width, self.height)
        else:
            self.widget.setFixedSize(self.width, self.height)

        self.widget.move(QtWidgets.QDesktopWidget().rect().center() - self.widget.rect().center())
        self.widget.resizeGL = self.resize  # Needs to be set before show()
        self.widget.show()

        if not self.cursor:
            self.widget.setCursor(QtCore.Qt.BlankCursor)

        if self.fullscreen:
            self.widget.showFullScreen()

        # We want mouse position events
        self.widget.setMouseTracking(True)

        # Override event functions
        self.widget.keyPressEvent = self.keyPressEvent
        self.widget.keyReleaseEvent = self.keyReleaseEvent
        self.widget.mouseMoveEvent = self.mouseMoveEvent

        # Attach to the context
        self.ctx = moderngl.create_context(require=self.gl_version.code)
        context.WINDOW = self
        self.fbo = self.ctx.screen

        # Ensure retina and 4k displays get the right viewport
        self.buffer_width = self.width * self.widget.devicePixelRatio()
        self.buffer_height = self.height * self.widget.devicePixelRatio()

        self.set_default_viewport()

    def keyPressEvent(self, event):
        """
        Pyqt specific key press callback function.
        Translates and forwards events to :py:func:`keyboard_event`.
        """
        self.keyboard_event(event.key(), self.keys.ACTION_PRESS, 0)

    def keyReleaseEvent(self, event):
        """
        Pyqt specific key release callback function.
        Translates and forwards events to :py:func:`keyboard_event`.
        """
        self.keyboard_event(event.key(), self.keys.ACTION_RELEASE, 0)

    def mouseMoveEvent(self, event):
        """
        Pyqt specific mouse event callback
        Translates and forwards events to :py:func:`cursor_event`.
        """
        self.cursor_event(event.x(), event.y(), 0, 0)

    def resize(self, width, height):
        """
        Pyqt specific resize callback.
        """
        if not self.fbo:
            return

        # pyqt reports sizes in actual buffer size
        self.width = width // self.widget.devicePixelRatio()
        self.height = height // self.widget.devicePixelRatio()
        self.buffer_width = width
        self.buffer_height = height

        super().resize(width, height)

    def swap_buffers(self):
        """
        Swaps buffers, increments the frame counter and pulls events
        """
        self.frames += 1
        self.widget.swapBuffers()
        # We don't use standard event loop having to manually process events
        self.app.processEvents()

    def use(self):
        """
        Make the window's framebuffer the current render target
        """
        self.fbo.use()

    def should_close(self) -> bool:
        """
        Checks if the internal close state is set
        """
        return self._closed

    def close(self):
        """
        Set the internal close state
        """
        self._closed = True

    def terminate(self):
        """
        Quits the running qt application
        """
        QtCore.QCoreApplication.instance().quit()
