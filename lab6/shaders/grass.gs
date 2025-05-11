#version 330 core
layout (points) in;
layout (triangle_strip, max_vertices = 4) out;

in VS_OUT {
    vec3 color;
} gs_in[];

out vec3 fColor;

void buildGrass(vec4 center)
{
    float h = 0.6;       // 草高度
    float w = 0.3;       // 草底宽

    vec4 up    = center + vec4(0.0, h, 0.0, 0.0);
    vec4 left  = center + vec4(-w, 0.0, 0.0, 0.0);
    vec4 right = center + vec4( w, 0.0, 0.0, 0.0);

    fColor = gs_in[0].color;
    gl_Position = center; EmitVertex();
    gl_Position = left;   EmitVertex();
    gl_Position = up;     EmitVertex();
    gl_Position = right;  EmitVertex();
    EndPrimitive();
}

void main()
{
    buildGrass(gl_in[0].gl_Position);
}
