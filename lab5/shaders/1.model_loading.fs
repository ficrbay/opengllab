#version 330 core
out vec4 FragColor;

in vec2 TexCoords;

uniform sampler2D texture_diffuse1;
uniform sampler2D texture_specular1;

void main()
{    
    vec3 diffuse = texture(texture_diffuse1, TexCoords).rgb;
    vec3 specular = texture(texture_specular1, TexCoords).rgb;

    vec3 result = diffuse + specular;
    FragColor = vec4(result, 1.0);
}