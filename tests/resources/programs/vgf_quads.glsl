#version 330

#if defined VERTEX_SHADER

layout (location = 0) in vec3 in_position;

void main() {
	gl_Position = vec4(in_position, 1.0);
}

#elif defined GEOMETRY_SHADER

layout (points) in;
layout (triangle_strip, max_vertices = 4) out;

uniform mat4 m_proj;
uniform mat4 m_mv;

void main() {
    //float size = gl_in[0].gl_PointSize;
    //color = size;
    const float size = 2.0;
    vec3 pos = gl_in[0].gl_Position.xyz;
    vec3 right = vec3(m_mv[0][0], m_mv[1][0], m_mv[2][0]);
    vec3 up = vec3(m_mv[0][1], m_mv[1][1], m_mv[2][1]);

    gl_Position = m_proj * m_mv * vec4(pos + (right + up) * size, 1.0);
    EmitVertex();

    gl_Position = m_proj * m_mv * vec4(pos + (-right + up) * size, 1.0);
    EmitVertex();

    gl_Position = m_proj * m_mv * vec4(pos + (right - up) * size, 1.0);
    EmitVertex();

    gl_Position = m_proj * m_mv * vec4(pos + (-right - up) * size, 1.0);
    EmitVertex();

    EndPrimitive();
}

#elif defined FRAGMENT_SHADER

out vec4 outColor;

void main() {
    outColor = vec4(1.0);
}

#endif
