#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
uniform mat4 m_mv;
uniform mat4 m_proj;
uniform float size;

void main() {
    gl_Position = m_proj * m_mv * vec4(in_position * size, 1.0);
}

#elif defined FRAGMENT_SHADER

out vec4 out_color;

void main() {
    out_color = vec4(1.0, 0.0, 0.0, 0.5);
}

#endif
