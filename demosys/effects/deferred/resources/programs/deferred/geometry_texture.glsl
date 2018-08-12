#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec3 in_normal;
in vec2 in_uv;

uniform mat4 m_mv;
uniform mat4 m_proj;
uniform mat3 m_normal;

out vec3 normal;
out vec2 uv;

void main() {
    normal = m_normal * in_normal;
    uv = in_uv;
    gl_Position = m_proj * m_mv * vec4(in_position, 1.0);
}

#elif defined FRAGMENT_SHADER

layout(location=0) out vec4 out_color;
layout(location=1) out vec3 out_normal;

uniform sampler2D texture0;

in vec3 normal;
in vec2 uv;

void main() {
    out_normal = normalize(normal);
    out_color = texture(texture0, uv);
}

#endif
