#version 330

#if defined VERTEX_SHADER

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
	uv = in_uv;
    normal = m_normal * in_normal;
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
uniform float time;
uniform sampler2D texture0;

in vec3 normal;
in vec2 uv;

void main()
{
    vec3 dir = vec3(0.0, 0.0, 1.0);
    float l = dot(dir, normal);
    fragColor = texture(texture0, uv) * l;
//    fragColor = vec4(l);
//    fragColor = vec4(1.0);
}

#endif
