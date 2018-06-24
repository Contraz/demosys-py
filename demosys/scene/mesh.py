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
        self.attributes = attributes or {}
        self.bbox_min = bbox_min
        self.bbox_max = bbox_max
        self.mesh_shader = None

    def draw(self, proj_mat, view_mat):
        """Draw the mesh using the assigned mesh shader"""
        if self.mesh_shader:
            self.mesh_shader.draw(self, proj_mat, view_mat)

    def draw_bbox(self, proj_matrix, view_matrix, shader, vao):
        shader.uniform("m_proj", proj_matrix.astype('f4').tobytes())
        shader.uniform("m_mv", view_matrix.astype('f4').tobytes())
        shader.uniform("bb_min", self.bbox_min.astype('f4').tobytes())
        shader.uniform("bb_max", self.bbox_max.astype('f4').tobytes())
        shader.uniform("color", (0.75, 0.75, 0.75))
        vao.draw(shader)

    def add_attribute(self, attr_type, name, components):
        """
        Add metadata about the mesh
        :param attr_type: POSITION, NORMAL ec
        :param name: The attribute name used in the shader
        :param components: Number of floats
        """
        self.attributes[attr_type] = {"name": name, "components": components}

    def calc_global_bbox(self, view_matrix, bbox_min, bbox_max):
        # Copy and extend to vec4
        bb1 = numpy.append(self.bbox_min[:], 1.0)
        bb2 = numpy.append(self.bbox_max[:], 1.0)

        # Transform the bbox values
        bmin = matrix44.apply_to_vector(view_matrix, bb1),
        bmax = matrix44.apply_to_vector(view_matrix, bb2),
        bmin = numpy.asarray(bmin)[0]
        bmax = numpy.asarray(bmax)[0]

        # If a rotation happened there is an axis change and we have to ensure max-min is positive
        for i in range(3):
            if bmax[i] - bmin[i] < 0:
                bmin[i], bmax[i] = bmax[i], bmin[i]

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
