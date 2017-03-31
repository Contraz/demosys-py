#version 410

#if defined VERTEX_SHADER

in vec3 in_Position;
in vec3 in_Normal;
in vec2 in_UV0;

uniform mat4 ProjM;
uniform mat4 ModelViewM;
uniform mat3 NormalM;

out vec3 normal;
out vec2 uv0;

void main() {
	gl_Position = ProjM * ModelViewM * vec4(in_Position, 1.0);
    normal = NormalM * in_Normal;
    uv0 = in_UV0;
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
uniform sampler2D texture0;
uniform sampler2D texture1;
uniform float time;

in vec3 normal;
in vec2 uv0;

void main()
{
    vec4 c1 = texture(texture0, uv0);
    vec4 c2 = texture(texture1, uv0);
    float m1 = sin(time * 1.0) / 2.0 + 0.5;
    float m2 = 1.0 - m1;

    vec3 dir = vec3(0.0, 0.0, 1.0);
    float d = dot(dir, normal);

    fragColor = (c1 * m1 + c2 * m2) * d;
}

#endif
