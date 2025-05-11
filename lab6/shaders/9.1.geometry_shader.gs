#version 330 core
layout (points) in;
layout (triangle_strip, max_vertices = 24) out;  // 6 段 × 4 刀片

in  vec3 fColor_in[];   // 来自顶点着色器的颜色
out vec3 fColor;

const float H   = 0.6;   // 草高
const float W   = 0.08;  // 根部宽
const int   SEG = 6;     // 每刀片竖向分段数
const float AMP = 0.10;  // 波浪振幅

// 给定中心、相位，生成一片“波浪形”草叶
void emitBlade(vec4 center, float phase)
{
    // 分段三角形条带
    for (int i = 0; i <= SEG; ++i)
    {
        float t  = float(i) / float(SEG);   // 0 → 1
        float y  = H * t;                   // 当前高度
        float dx = AMP * sin(phase + 3.14159 * t); // 横向偏移 (静态波纹)

        vec4 left  = center + vec4(-W, y, 0.0, 0.0) + vec4(dx, 0.0, 0.0, 0.0);
        vec4 right = center + vec4( W, y, 0.0, 0.0) + vec4(dx, 0.0, 0.0, 0.0);

        fColor = fColor_in[0];
        gl_Position = left;  EmitVertex();
        gl_Position = right; EmitVertex();
    }
    EndPrimitive();
}

void main()
{
    vec4 c = gl_in[0].gl_Position;

    // 生成 4 片朝不同方向，静态波浪外形
    emitBlade(c, 0.0);
    emitBlade(c, 1.57);   // 90°
    emitBlade(c, 3.14);   // 180°
    emitBlade(c, 4.71);   // 270°
}
