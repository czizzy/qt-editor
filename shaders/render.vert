attribute vec3 aPos;
attribute vec3 aNormal;


varying vec3 vNormal;

uniform highp mat4 view;
uniform highp mat4 model;
uniform highp mat4 projection;


void main(void)
{
    vNormal = (model * vec4(aNormal, 0.0)).xyz;
    gl_Position = projection * view * model * vec4(aPos, 1.0);
}
