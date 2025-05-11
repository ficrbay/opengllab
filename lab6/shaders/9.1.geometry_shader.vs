#version 330 core
layout (location = 0) in vec3 aPos;   // 草根位置
layout (location = 1) in vec3 aColor;

out VS_OUT {
    vec3 color;
} vs_out;

void main()
{
    gl_Position = vec4(aPos, 1.0);  // 几何着色器里再做 MVP
    vs_out.color = aColor;
}
