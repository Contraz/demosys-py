#version 410

#if defined VERTEX_SHADER

in vec3 in_position;

uniform mat4 m_proj;
uniform mat4 m_mv;

void main() {
	gl_Position = m_proj * m_mv * vec4(in_position, 1.0);
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;

void main()
{
    fragColor = vec4(1.0);
}

#endif
