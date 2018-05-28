"""
Wrapper for a loaded mesh / vao with properties
"""
from pyrr import matrix44


class Node:
    def __init__(self, camera=None, mesh=None, matrix=None):
        self.camera = camera
        self.mesh = mesh
        self.matrix = matrix
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def draw(self, m_proj, m_mv):
        if self.matrix is not None:
            m_mv = matrix44.multiply(self.matrix, m_mv)

        if self.mesh:
            self.mesh.draw(m_proj, m_mv)

        for child in self.children:
            child.draw(m_proj, m_mv)

    def draw_bbox(self, m_proj, m_mv, shader, vao):
        if self.matrix is not None:
            m_mv = matrix44.multiply(self.matrix, m_mv)

        if self.mesh:
            self.mesh.draw_bbox(m_proj, m_mv, shader, vao)

        for child in self.children:
            child.draw_bbox(m_proj, m_mv, shader, vao)

    def calc_global_bbox(self, view_matrix, bbox_min, bbox_max):
        """Recursive calculation of scene bbox"""
        if self.matrix is not None:
            view_matrix = matrix44.multiply(self.matrix, view_matrix)

        if self.mesh:
            bbox_min, bbox_max = self.mesh.calc_global_bbox(view_matrix, bbox_min, bbox_max)

        for child in self.children:
            bbox_min, bbox_max = child.calc_global_bbox(view_matrix, bbox_min, bbox_max)

        return bbox_min, bbox_max
