#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec3 in_normal;

uniform mat4 m_proj;
uniform mat4 m_mv;
uniform mat3 m_normal;

out vec3 normal;
out vec3 pos;

void main() {
    vec4 p = m_mv * vec4(in_position, 1.0);
	gl_Position = m_proj * p;
    normal = m_normal * in_normal;
    pos = p.xyz;
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
uniform float time;
uniform vec4 color;

in vec3 normal;
in vec3 pos;

void main()
{
    vec3 dir = normalize(-pos); //vec3(0.0, 0.0, 1.0);
    float l = dot(dir, normalize(normal));
    fragColor = color * (0.25 + abs(l) * 0.75);
}

#endif
