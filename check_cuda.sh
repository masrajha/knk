#!/bin/bash

echo "=== CUDA Environment Check ==="
echo "1. Checking NVIDIA Driver..."
nvidia-smi

echo -e "\n2. Checking CUDA Compiler..."
nvcc --version

echo -e "\n3. Checking CUDA Libraries..."
ldconfig -p | grep cuda

echo -e "\n4. Checking GPU Architecture..."
nvidia-smi --query-gpu=compute_cap --format=csv

echo -e "\n5. Checking CUDA Path..."
echo "CUDA_PATH: $CUDA_PATH"
echo "PATH: $PATH" | grep cuda

echo -e "\n6. Testing Simple CUDA Compilation..."
cat > test_simple.cu << 'EOF'
#include <cstdio>
int main() {
    int dev_count;
    cudaGetDeviceCount(&dev_count);
    printf("CUDA Devices: %d\n", dev_count);
    return 0;
}
EOF

nvcc -o test_simple test_simple.cu
if [ $? -eq 0 ]; then
    echo "COMPILATION: SUCCESS"
    ./test_simple
else
    echo "COMPILATION: FAILED"
fi

rm test_simple test_simple.cu