#version 330

in vec3 in_position;
in vec3 in_normal;
in vec2 in_uv;

uniform mat4 m_proj;
uniform mat4 m_mv;
uniform mat3 m_normal;

out vec3 normal;
out vec2 uv;

void main() {
	gl_Position = m_proj * m_mv * vec4(in_position, 1.0);
    normal = m_normal * in_normal;
    uv = in_uv;
}
