#version 330

#if defined VERTEX_SHADER

in vec4 in_position;
in vec2 in_uv;

out vec4 uv0;

void main()
{ 
	uv0 = vec4(in_uv, 0.0, 1.0);
	gl_Position = in_position;
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;

uniform sampler2D tex;
uniform sampler2D tex2;
uniform float scroll;
uniform float intensity;
uniform float zangle;
uniform float speedlayer_alpha;
uniform float accelerate;

in vec4 uv0;

vec4 screen(vec4 color0, vec4 color1) 
{
    vec4 white = vec4(1.0, 1.0, 1.0, 1.0);
    return white - ((white - color0) * (white - color1));
}

void main()
{
	// Rotating texture layers
	mat4 RotationMatrix0 = mat4(cos(zangle), -sin(zangle), 0.0, 0.0,
                              sin(zangle),  cos(zangle), 0.0, 0.0,
                                      0.0,          0.0, 1.0, 0.0,
                                      0.0,          0.0, 0.0, 1.0);

	mat4 RotationMatrix1 = mat4(cos(-zangle * 0.75), -sin(-zangle * 0.75), 0.0, 0.0,
                              sin(-zangle * 0.75),  cos(-zangle * 0.75), 0.0, 0.0,
                                              0.0,                  0.0, 1.0, 0.0,
								                              0.0,                  0.0, 0.0, 1.0);

	mat4 RotationMatrix2 = mat4(cos(zangle * 0.5), -sin(zangle * 0.5), 0.0, 0.0,
                              sin(zangle * 0.5),  cos(zangle * 0.5), 0.0, 0.0,
                                            0.0,                0.0, 1.0, 0.0,
								                            0.0,                0.0, 0.0, 1.0);

	mat4 RotationMatrix3 = mat4(cos(-zangle * 0.25), -sin(-zangle * 0.25), 0.0, 0.0,
                              sin(-zangle * 0.25),  cos(-zangle * 0.25), 0.0, 0.0,
                                              0.0,                  0.0, 1.0, 0.0,
                                              0.0,                  0.0, 0.0, 1.0);
     
	mat4 translationMatrix = mat4(1.0, 0.0, 0.0, -0.5,
                                0.0, 1.0, 0.0, -0.5,
                                0.0, 0.0, 1.0,  0.0,
                                0.0, 0.0, 0.0,  1.0);

	mat4 tm0 = translationMatrix * RotationMatrix0;
	mat4 tm1 = translationMatrix * RotationMatrix1;
	mat4 tm2 = translationMatrix * RotationMatrix2;
	mat4 tm3 = translationMatrix * RotationMatrix3;

	float scale0 = mod(2.0 - scroll, 2.0);
	float scale1 = mod(2.0 - scroll + 0.5, 2.0);
	float scale2 = mod(2.0 - scroll + 1.0, 2.0);
	float scale3 = mod(2.0 - scroll + 1.5, 2.0);

	vec2 texcoord0 = (uv0*tm0).xy;
	vec2 texcoord1 = (uv0*tm1).xy;
	vec2 texcoord2 = (uv0*tm2).xy;
	vec2 texcoord3 = (uv0*tm3).xy;

	vec3 tcol0 = texture(tex2, vec2( 0.0,  0.0) + (texcoord0 * scale0)).rgb * (2.0 - scale0);
	vec3 tcol1 = texture(tex2, vec2(-0.2,  0.1) + (texcoord1 * scale1)).rgb * (2.0 - scale1);
	vec3 tcol2 = texture(tex2, vec2( 0.0, -0.4) + (texcoord2 * scale2)).rgb * (2.0 - scale2);
	vec3 tcol3 = texture(tex2, vec2( 0.5, -0.8) + (texcoord3 * scale3)).rgb * (2.0 - scale3);

	vec4 tcol_final = vec4(tcol0 + tcol1 + tcol2 + tcol3, 1.0) / 2.0;
  
	// Tunnel layer
	float PI = 3.14159265358979323846264;

	float x = (uv0.x - 0.5) * (16.0 / 9.0);
	float y = uv0.y - 0.5;

	float distance = sqrt(pow(x, 2.0) + pow(y, 2.0));
	float angle = (1.0 + (atan(x, y) / PI)) / 2.0;

	x = (1.0 * 0.2) / distance;
	y = angle;

	vec4 col0 = texture(tex2, vec2(x + mod((scroll / 2.0) + accelerate, 1.0), y)) + vec4((1.0 - distance) * (intensity * 1.5));
	vec4 col1 = texture(tex, vec2((x * 2.0) + mod((scroll * 2.0) + accelerate, 1.0), y * 2.0)) + vec4((1.0 - distance) * intensity);
	vec4 col2 = texture(tex, vec2((x * 4.0) + mod((scroll * 4.0) + accelerate, 1.0), y * 4.0)) + vec4((1.0 - distance) * intensity);

	fragColor = screen(mix(col0, col1 * col2, speedlayer_alpha), tcol_final);
}
#endif
