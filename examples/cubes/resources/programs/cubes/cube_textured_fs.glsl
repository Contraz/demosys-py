#version 330

out vec4 fragColor;
uniform sampler2D wood;

in vec3 normal;
in vec2 uv;

void main()
{
    vec3 dir = vec3(0.0, 0.0, 1.0);
    float l = dot(dir, normalize(normal));
    fragColor = texture(wood, uv) * min(1.0, l + 0.25);
}

