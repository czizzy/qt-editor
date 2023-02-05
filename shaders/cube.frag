varying vec3 vNormal;

uniform vec3 uLightDirection;

void main(void)
{
    vec3 normal = normalize(vNormal);
    float light = dot(normal, -uLightDirection);

    // linear interpolation of first texture with second one
    // 30% indicates the amount of the presence of the second one
    gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
    gl_FragColor.rgb *= light;
    //gl_FragColor = texture(myTexture2, TexCoord);
}
