#version 330 core

layout (location = 0) in vec3 in_position;

layout (location = 5) in vec3  obj_position;
layout (location = 6) in vec4  obj_rotation;
layout (location = 7) in vec3  obj_scale;

// Uniforms
uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;

// Function to get the model matrix from node position, rotation, and scale
mat4 getModelMatrix(vec3 pos, vec4 rot, vec3 scl) {
    mat4 translation = mat4(
        1    , 0    , 0    , 0,
        0    , 1    , 0    , 0,
        0    , 0    , 1    , 0,
        pos.x, pos.y, pos.z, 1
    );
    mat4 rotation = mat4(
        1 - 2 * (rot.z * rot.z + rot.w * rot.w), 2 * (rot.y * rot.z - rot.w * rot.x), 2 * (rot.y * rot.w + rot.z * rot.x), 0,
        2 * (rot.y * rot.z + rot.w * rot.x), 1 - 2 * (rot.y * rot.y + rot.w * rot.w), 2 * (rot.z * rot.w - rot.y * rot.x), 0,
        2 * (rot.y * rot.w - rot.z * rot.x), 2 * (rot.z * rot.w + rot.y * rot.x), 1 - 2 * (rot.y * rot.y + rot.z * rot.z), 0,
        0, 0, 0, 1
    );
    mat4 scale = mat4(
        scl.x, 0    , 0    , 0,
        0    , scl.y, 0    , 0,
        0    , 0    , scl.z, 0,
        0    , 0    , 0    , 1
    );
    return translation * rotation * scale;
}


void main() {
    // Set the model matrix
    mat4 modelMatrix = getModelMatrix(obj_position, obj_rotation, obj_scale);
    // Set the fragment position
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(in_position, 1.0);
}