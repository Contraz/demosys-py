#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec2 in_uv;

uniform vec2 pos;
uniform float size;
uniform float yscale;

out vec2 uv;
// 
void main() {
    vec3 p = vec3(
        (in_position.x * size) - 1.0 + pos[0],
        (in_position.y * size) * yscale * 2.0 + 1.0 + pos[1],
        0.0
    );
    gl_Position = vec4(p, 1.0);
    uv = in_uv;
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
uniform sampler2D texture0;
in vec2 uv;

void main() {
    fragColor = texture(texture0, uv);
}

#endif
