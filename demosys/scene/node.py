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

    def draw(self, m_mv, m_proj, shader):
        if self.matrix is not None:
            m_mv = matrix44.multiply(self.matrix, m_mv)

        if self.mesh:
            self.mesh.draw(m_mv, m_proj, shader)

        for child in self.children:
            child.draw(m_mv, m_proj, shader)
