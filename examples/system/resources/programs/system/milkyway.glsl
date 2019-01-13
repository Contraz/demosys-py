#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec2 in_uv;

uniform mat4 m_proj;
uniform mat4 m_mv;

out vec2 uv;

void main() {
	gl_Position = m_proj * m_mv * vec4(in_position, 1.0);
    uv = in_uv;
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
uniform sampler2D texture0;
in vec2 uv;

void main()
{
    fragColor = texture(texture0, uv);
}

#endif
