#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec3 in_normal;
in vec2 in_uv;

uniform mat4 m_mv;
uniform mat4 m_proj;
uniform mat3 m_normal;

out vec3 normal;

void main() {
    normal = m_normal * in_normal;
    gl_Position = m_proj * m_mv * vec4(in_position, 1.0);
}

#elif defined FRAGMENT_SHADER

layout(location=0) out vec4 out_color;
layout(location=1) out vec3 out_normal;

uniform vec4 color;

in vec3 normal;

void main() {
    out_normal = normalize(normal);
    out_color = color;
}

#endif
