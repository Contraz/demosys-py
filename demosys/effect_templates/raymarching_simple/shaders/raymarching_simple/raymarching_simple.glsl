#version 410

#if defined VERTEX_SHADER

in vec3 in_position;
in vec3 in_normal;

uniform mat4 m_proj;
uniform mat4 m_mv;

out vec3 normal;
out vec2 uv;

void main() {
	gl_Position = m_proj * m_mv * vec4(in_position, 1.0);
}

#elif defined FRAGMENT_SHADER

uniform vec2 resolution;
uniform float fov;
uniform float alpha;
uniform float modifier;
uniform vec3 cPosition;
uniform vec3 cLookAt;
uniform vec3 lPosition;
uniform float lIntensity;
uniform vec3 color;

out vec4 fragColor;

const int maxSteps = 64;
const float maxDistance = 60.0;
const float distanceThreshold = 0.0005;

struct Hit {
    vec3 normal;
    vec3 path;
    float steps;
    float dist;
};

float sdMandleBox(vec3 pos, float size)
{
    const int Iterations = 10;
    const float Scale = 2.0;
    const float FoldingLimit = 100.0;
    const float MinRad2 = 0.15;
    vec4 scale = vec4(size) / MinRad2;
    float AbsScalem1 = abs(Scale - 1.0);
    float AbsScaleRaisedTo1mIters = pow(abs(Scale), float(1 - Iterations));
    vec4 p = vec4(pos, 1.0), p0 = p;  // p.w is the distance estimate
    
  for (int i=0; i<Iterations; i++)
    {
        p.xyz = clamp(p.xyz, -1.3, 1.3) * 2.0 + (modifier) - p.xyz;
        float r2 = dot(p.xyz, p.xyz);
        p *= clamp(max(MinRad2 / r2, MinRad2), 0.19, 1.0);
        p = p * scale + p0;
        if (r2>FoldingLimit) break;
    }
    return ((length(p.xyz) - AbsScalem1) / p.w - AbsScaleRaisedTo1mIters);
}

Hit raymarch(vec3 rayOrigin, vec3 rayDirection) {
    const vec2 eps = vec2(0.001, 0.001);
    float size = 1.8;
    Hit h;
    for(int i = 0; i < maxSteps; i++) {
        h.path = rayOrigin + rayDirection * h.dist;
        float d = sdMandleBox(h.path, size);
        h.steps += 1.0;
        if(d < distanceThreshold) {
            h.normal = normalize(vec3(
                sdMandleBox(h.path + eps.xyy, size) - sdMandleBox(h.path - eps.xyy, size),
                sdMandleBox(h.path + eps.yxy, size) - sdMandleBox(h.path - eps.yxy, size),
                sdMandleBox(h.path + eps.yyx, size) - sdMandleBox(h.path - eps.yyx, size)
            ));
            break;
        }
        h.dist += d;

    }
    return h;
}

vec4 processColor(Hit h, vec3 rd, vec3 ro, vec2 uv, vec3 li)
{
    vec3 c = color * (1.0 - (h.steps / float(maxSteps)));
    c *= (1.0 - (h.dist > maxDistance ? 0.0 : h.dist / maxDistance));

    float light = max(0.0, dot(-normalize(h.path - li), h.normal));

    c *= light * lIntensity * vec3(0.4, 0.4, 0.4);
    return vec4(c, alpha);
}

void main(void)
{
    float aspectRatio = resolution.y / resolution.x;
    vec2 uv = (2.0 * gl_FragCoord.xy / resolution - 1.0) * aspectRatio;

    vec3 forward = normalize(cLookAt - cPosition); 
    vec3 right = normalize(vec3(forward.z, 0.0, -forward.x)); 
    vec3 up = normalize(cross(forward, right)); 

    vec3 rd = normalize(forward + fov * uv.x * right + fov * uv.y * up);
    vec3 ro = vec3(cPosition.x, cPosition.y, cPosition.z);
    Hit tt = raymarch(ro, rd);
 
    fragColor = processColor(tt, rd, ro, uv, lPosition); 

}

#endif
