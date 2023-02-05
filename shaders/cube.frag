varying vec3 vNormal;

uniform vec3 uLightDirection;
uniform vec4 uColor;


void main(void)
{
    vec3 normal = normalize(vNormal);
    float light = dot(normal, -uLightDirection);

    // linear interpolation of first texture with second one
    // 30% indicates the amount of the presence of the second one
    gl_FragColor = vec4(uColor.rgb * light, uColor.a);
    //gl_FragColor = texture(myTexture2, TexCoord);
}
