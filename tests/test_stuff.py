from demosys.test import DemosysTestCase
from demosys.opengl import FBO


class SuffTest(DemosysTestCase):

    def test_stuff(self):
        FBO.create((10, 10), depth=True)

    def test_shader(self):
        self.create_shader(
            """#version 330
            #if defined VERTEX_SHADER
            in vec3 in_position;
            void main() {
            	gl_Position = vec4(in_position, 1.0);
            }
            #elif defined FRAGMENT_SHADER
            out vec4 fragColor;
            void main() {
                fragColor = vec4(1.0);
            }
            #endif
            """
        )
