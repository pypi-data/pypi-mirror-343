#version 330 core

layout (location = 0) out vec4 fragColor;
layout (location = 1) out vec4 bloomColor;
layout (location = 2) out vec4 normalTexture;


in vec4     color;
in vec2     imageIndex;
in vec2     uv;
in float    alpha;
flat in int usesImage;

struct textArray {
    sampler2DArray array;
};
uniform textArray textureArrays[5];

void main() {
    if (bool(usesImage)) {
        fragColor = texture(textureArrays[int(round(imageIndex.x))].array, vec3(uv, round(imageIndex.y))) * alpha;
    }
    else {
        fragColor = color;
    }
    normalTexture = vec4(0.0);
    bloomColor = vec4(0.0);
}