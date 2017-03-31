#version 410

#if defined VERTEX_SHADER

in vec3 in_Position;
in vec2 in_UV0;

out vec2 uv0;

void main() {
	gl_Position = vec4(in_Position, 1.0);
    uv0 = in_UV0;
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
uniform sampler2D texture0;

in vec2 uv0;

void main()
{
    fragColor = texture(texture0, uv0);
}

#endif
