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
    normal = m_normal * in_normal;
    uv = in_uv;
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
uniform sampler2D texture0;
uniform sampler2D texture1;
uniform float time;

in vec3 normal;
in vec2 uv;

void main()
{
    vec4 c1 = texture(texture0, uv);
    vec4 c2 = texture(texture1, uv);
    float m1 = sin(time * 1.0) / 2.0 + 0.5;
    float m2 = 1.0 - m1;

    vec3 dir = vec3(0.0, 0.0, 1.0);
    float d = dot(dir, normal);

    fragColor = (c1 * m1 + c2 * m2) * d;
}

#endif
