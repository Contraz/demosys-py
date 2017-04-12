#version 410

#if defined VERTEX_SHADER

in vec3 in_position;

uniform mat4 m_proj;
uniform mat4 m_mv;
uniform mat3 m_normal;

void main() {
	gl_Position = vec4(in_position, 1.0);
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
uniform sampler2D texture0;
uniform float time;

in vec3 normal;
in vec2 uv;
in vec3 lightdir;
in vec3 eyepos;

void main()
{
    vec4 diffuse = vec4(0.5, 0.5, 0.5, 1.0);
    vec4 ambient = vec4(0.2, 0.2, 0.2, 1.0);
    vec4 specular = vec4(1.0, 1.0, 1.0, 1.0);
    float shininess = 0.5;

    vec4 c = texture(texture0, uv);
    vec4 spec = vec4(0.0);

    vec3 n = normalize(normal);
    vec3 l = normalize(lightdir);
    vec3 e = normalize(eyepos);

    float intensity = max(dot(n,l), 0.0);
    if (intensity > 0.0) {
        vec3 h = normalize(l + e);
        float intSpec = max(dot(h, n), 0.0);
        spec = specular * pow(intSpec, shininess);
    }
    float att = clamp(1.0 - length(eyepos)/200.0, 0.0, 1.0);
    att *= att;
    fragColor = c * max(intensity * diffuse + spec, ambient) * att;
}


#elif defined GEOMETRY_SHADER

layout (points) in;
layout (triangle_strip, max_vertices = 24) out; // 4 vertices per side of the cube

uniform mat4 m_proj;
uniform mat4 m_mv;
uniform mat3 m_normal;
uniform vec3 lightpos;
uniform float time;

out vec2 uv;
out vec3 normal;
out vec3 lightdir;
out vec3 eyepos;

// Define the 8 corners of a cube (back plane, front plane (counter clockwise))
vec3 cube_corners[8] = vec3[]  (
	vec3( 1.0,  1.0, -1.0), // right top far
	vec3(-1.0,  1.0, -1.0), // left top far
	vec3(-1.0, -1.0, -1.0), // left bottom far
	vec3( 1.0, -1.0, -1.0), // right bottom far
	vec3( 1.0,  1.0,  1.0), // right top near
	vec3(-1.0,  1.0,  1.0), // left top near
	vec3(-1.0, -1.0,  1.0), // left bottom near
	vec3( 1.0, -1.0,  1.0)  // right bottom near
);

#define EMIT_V(POS, UV, NORMAL) \
	uv = UV; \
	normal = normalize(m_normal * NORMAL); \
	lightdir = lightpos - POS.xyz; \
	eyepos = -POS.xyz; \
	gl_Position = m_proj * vec4(POS, 1.0); \
	EmitVertex()

#define EMIT_QUAD(P1, P2, P3, P4, NORMAL) \
	EMIT_V(corners[P1], vec2(0.0, 0.0), NORMAL); \
	EMIT_V(corners[P2], vec2(1.0, 0.0), NORMAL); \
	EMIT_V(corners[P3], vec2(0.0, 1.0), NORMAL); \
	EMIT_V(corners[P4], vec2(1.0, 1.0), NORMAL); \
	EndPrimitive()

void main()
{
	// Calculate the 8 cube corners
	vec3 point = gl_in[0].gl_Position.xyz;
	vec3 corners[8];
	int i;
	for(i = 0; i < 8; i++)
	{
		vec3 pos = point.xyz + cube_corners[i] * 0.5;
		pos.y += sin(time + length(gl_in[0].gl_Position.xyz));
		pos.x += cos(time + gl_in[0].gl_Position.x);
		pos.z += cos(time + gl_in[0].gl_Position.z);

		corners[i] = (m_mv * vec4(pos, 1.0)).xyz;
	}
	EMIT_QUAD(3, 2, 0, 1, vec3( 0.0,  0.0, -1.0)); // back
	EMIT_QUAD(6, 7, 5, 4, vec3( 0.0,  0.0,  1.0)); // front
	EMIT_QUAD(7, 3, 4, 0, vec3( 1.0,  0.0,  0.0)); // right
	EMIT_QUAD(2, 6, 1, 5, vec3(-1.0,  0.0,  0.0)); // left
	EMIT_QUAD(5, 4, 1, 0, vec3( 0.0,  1.0,  0.0)); // top
	EMIT_QUAD(2, 3, 6, 7, vec3( 0.0, -1.0,  0.0)); // bottom
    EndPrimitive();
}

#endif
