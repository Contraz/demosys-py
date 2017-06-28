#version 410

#if defined VERTEX_SHADER

in vec3 in_position;
in vec2 in_uv;

out vec2 uv;

void main() {
    uv = in_uv;
    gl_Position = vec4(in_position, 1.0);
}

#elif defined FRAGMENT_SHADER

out vec4 out_color;
uniform sampler2D diffuse_buffer;
uniform sampler2D light_buffer;
in vec2 uv;

void main() {
    out_color = texture(diffuse_buffer, uv) * (texture(light_buffer, uv));
}

#endif