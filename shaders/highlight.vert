attribute vec3 aPos;
attribute vec3 aNormal;

uniform highp mat4 view;
uniform highp mat4 model;
uniform highp mat4 projection;


void main(void)
{
    mat4 scaleMatrix = mat4(
        1.01, 0.0, 0.0, 0.0,
        0.0, 1.01, 0.0, 0.0,
        0.0, 0.0, 1.01, 0.0,
        0.0, 0.0, 0.0, 1.0
        );
    // vec3 extrudePos = aPos + aNormal * 0.01;
    gl_Position = projection * view * model * scaleMatrix * vec4(aPos, 1.0);
}
