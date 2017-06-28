#version 410

#if defined VERTEX_SHADER

in vec3 in_position;
uniform mat4 m_light;
uniform mat4 m_proj;
uniform float radius;

out vec3 viewRay;
out vec3 vs_lightpos;

void main() {
    vec4 pos = vec4(in_position.xyz * radius, 1.0);
    // Find the light position from the view matrix
    vs_lightpos = vec3(m_light[3][0], m_light[3][1], m_light[3][2]);
    // Rays for reconstructing view position from depth
    viewRay = (m_light * pos).xyz;
    gl_Position = m_proj * m_light * pos;
}

#elif defined FRAGMENT_SHADER

out vec4 out_light;

uniform sampler2D g_normal;
uniform sampler2D g_depth;
uniform vec2 screensize;
uniform vec2 proj_const;
uniform float radius;

in vec3 viewRay;
in vec3 vs_lightpos;

void main() {
    vec2 uv = vec2(gl_FragCoord.x / screensize.x, gl_FragCoord.y / screensize.y);
	vec3 normal = normalize(texture(g_normal, uv).rgb);

	// View position reconstruct from depth
	float depth = texture(g_depth, uv).r;
	vec3 ray = vec3(viewRay.xy / -viewRay.z, -1.0);
	float linear_depth = proj_const.y  / (depth - proj_const.x);
	vec3 pos = ray * linear_depth;

    // Discard fragments outside the light radius
    float dist = length(vs_lightpos - pos);
    if (dist > radius) {
        discard;
    }

    vec3 lightDir = normalize(vs_lightpos - pos);
    vec3 viewDir = normalize(-pos);
    vec3 halfwayDir = normalize(lightDir + viewDir);
//    vec3 reflectDir = reflect(-lightDir, normal);

    float diffuse = max(dot(normal, lightDir), 0.0);
    float spec = pow(max(dot(normal, halfwayDir), 0.0), 32.0);
//    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 8.0);

    float l = diffuse * 0.5 + spec;
    // l *= (1.0 - dist / radius);
    l *= clamp(1.0 - dist*dist/(radius*radius), 0.0, 1.0);
    out_light = vec4(l);
}

#endif
