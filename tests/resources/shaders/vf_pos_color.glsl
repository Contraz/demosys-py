#version 330

#if defined VERTEX_SHADER
in vec3 in_position;

void main() {
    gl_Position = vec4(in_position, 1.0);
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
uniform vec4 color;

void main() {
    fragColor = color;
}
#endif
