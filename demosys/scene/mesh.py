"""
Mesh class containing geometry information
"""
from pyrr import matrix44
import numpy


class Mesh:
    """Mesh info and geometry"""

    def __init__(self, name, vao=None, material=None, attributes=None, bbox_min=None, bbox_max=None):
        """
        :param name: Name of the mesh
        :param vao: VAO
        :param material: Material
        :param attributes: Details info about each mesh attribute (dict)
            {
                "NORMAL": {"name": "in_normal", "components": 3, "type": GL_FLOAT},
                "POSITION": {"name": "in_position", "components": 3, "type": GL_FLOAT}
            }
        """
        self.name = name
        self.vao = vao
        self.material = material
        self.attributes = attributes
        self.bbox_min = bbox_min
        self.bbox_max = bbox_max
        self.mesh_shader = None

    def draw(self, proj_mat, view_mat):
        """Draw the mesh using the assigned mesh shader"""
        if self.mesh_shader:
            self.mesh_shader.draw(self, proj_mat, view_mat)

    def draw_bbox(self, proj_matrix, view_matrix, shader, vao):
        vao.bind(shader)
        shader.uniform_mat4("m_proj", proj_matrix)
        shader.uniform_mat4("m_mv", view_matrix)
        shader.uniform_3fv("bb_min", self.bbox_min)
        shader.uniform_3fv("bb_max", self.bbox_max)
        vao.draw()

    def calc_global_bbox(self, view_matrix, bbox_min, bbox_max):
        bb1 = self.bbox_min[:]
        bb1.append(1.0)
        bb2 = self.bbox_max[:]
        bb2.append(1.0)

        bmin = matrix44.apply_to_vector(view_matrix, bb1),
        bmax = matrix44.apply_to_vector(view_matrix, bb2),

        bmin = numpy.asarray(bmin)[0]
        bmax = numpy.asarray(bmax)[0]

        if bbox_min is None or bbox_max is None:
            return bmin[0:3], bmax[0:3]

        for i in range(3):
            bbox_min[i] = min(bbox_min[i], bmin[i])

        for i in range(3):
            bbox_max[i] = max(bbox_max[i], bmax[i])

        return bbox_min, bbox_max

    def has_normals(self):
        return "NORMAL" in self.attributes

    def has_uvs(self, layer=0):
        return "TEXCOORD_{}".format(layer) in self.attributes
