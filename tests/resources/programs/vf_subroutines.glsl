#version 410

#if defined VERTEX_SHADER
in vec3 in_position;

void main() {
    gl_Position = vec4(in_position, 1.0);
}

#elif defined FRAGMENT_SHADER

subroutine vec4 colorFunc ();

subroutine (colorFunc) vec4 redColor() { 
    return vec4(1.0, 0.0, 0.0, 1.0);
} 
 
subroutine (colorFunc) vec4 blueColor() {
    return vec4(0.0, 0.0, 1.0, 1.0);
}

out vec4 fragColor;
subroutine uniform colorFunc color;

void main() {
    fragColor = color();
}
#endif
