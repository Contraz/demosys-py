#version 330

#if defined VERTEX_SHADER

in uint in_val;
out uint out_val;

void main() {
    out_val = in_val + 1u;
}
#endif
