import moderngl
from PyQt5 import QtCore, QtOpenGL, QtWidgets

from demosys.context.base import BaseWindow
from demosys import context

from .keys import Keys


class Window(BaseWindow):
    keys = Keys

    def __init__(self):
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

        self.widget.setFixedSize(self.width, self.height)

        self.widget.move(QtWidgets.QDesktopWidget().rect().center() - self.widget.rect().center())
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
        self.widget.resizeGL = self.resizeGL

        # Attach to the context
        self.ctx = moderngl.create_context(require=self.gl_version.code)
        context.WINDOW = self
        self.fbo = self.ctx.screen

        # Ensure retina and 4k displays get the right viewport
        self.buffer_width = self.width * self.widget.devicePixelRatio()
        self.buffer_height = self.height * self.widget.devicePixelRatio()

        self.set_default_viewport()

    def keyPressEvent(self, event):
        self.keyboard_event(event.key(), self.keys.ACTION_PRESS, 0)

    def keyReleaseEvent(self, event):
        self.keyboard_event(event.key(), self.keys.ACTION_RELEASE, 0)

    def mouseMoveEvent(self, event):
        self.cursor_event(event.x(), event.y(), 0, 0)

    def resizeGL(self, width, height):
        print("Resize", width, height)

    def swap_buffers(self):
        self.frames += 1
        self.widget.swapBuffers()
        # We don't use standard event loop having to manually process events
        self.app.processEvents()

    def use(self):
        self.fbo.use()

    def should_close(self):
        return self._closed

    def close(self):
        self._closed = True

    def terminate(self):
        QtCore.QCoreApplication.instance().quit()
