#include <iostream>
#include <cuda_runtime.h>
#include <cmath>

// Kernel CUDA untuk menjumlahkan dua vektor
__global__ void vectorAdd(const float *A, const float *B, float *C, int numElements) {
    int i = blockDim.x * blockIdx.x + threadIdx.x;
    
    if (i < numElements) {
        C[i] = A[i] + B[i];
        // Debug: print beberapa nilai pertama dari setiap block
        if (i < 10 && threadIdx.x == 0) {
            printf("Device: A[%d]=%.6f, B[%d]=%.6f, C[%d]=%.6f\n", i, A[i], i, B[i], i, C[i]);
        }
    }
}

// Error checking macro untuk CUDA
#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            std::cerr << "CUDA error at " << __FILE__ << ":" << __LINE__ \
                     << " - " << cudaGetErrorString(err) << std::endl; \
            exit(1); \
        } \
    } while(0)

int main() {
    // Jumlah elemen dalam vektor
    int numElements = 50000;
    size_t size = numElements * sizeof(float);
    
    std::cout << "Menjalankan CUDA Vector Addition..." << std::endl;
    std::cout << "Jumlah elemen vektor: " << numElements << std::endl;

    // Alokasi memori host (CPU)
    float *h_A = new float[numElements];
    float *h_B = new float[numElements];
    float *h_C = new float[numElements];

    // Inisialisasi vektor input
    for (int i = 0; i < numElements; ++i) {
        h_A[i] = rand() / (float)RAND_MAX;
        h_B[i] = rand() / (float)RAND_MAX;
    }

    // Alokasi memori device (GPU)
    float *d_A = nullptr;
    float *d_B = nullptr;
    float *d_C = nullptr;
    
    CUDA_CHECK(cudaMalloc((void**)&d_A, size));
    CUDA_CHECK(cudaMalloc((void**)&d_B, size));
    CUDA_CHECK(cudaMalloc((void**)&d_C, size));

    // Salin data dari host ke device
    CUDA_CHECK(cudaMemcpy(d_A, h_A, size, cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_B, h_B, size, cudaMemcpyHostToDevice));

    // Launch kernel CUDA
    int threadsPerBlock = 256;
    int blocksPerGrid = (numElements + threadsPerBlock - 1) / threadsPerBlock;
    
    std::cout << "Launching kernel dengan " << blocksPerGrid << " blocks x " 
              << threadsPerBlock << " threads" << std::endl;
    
    vectorAdd<<<blocksPerGrid, threadsPerBlock>>>(d_A, d_B, d_C, numElements);
    
    // Cek error kernel
    cudaError_t kernelError = cudaGetLastError();
    if (kernelError != cudaSuccess) {
        std::cerr << "Kernel launch error: " << cudaGetErrorString(kernelError) << std::endl;
        return 1;
    }
    
    // Tunggu sampai kernel selesai
    CUDA_CHECK(cudaDeviceSynchronize());

    // Salin hasil dari device ke host
    CUDA_CHECK(cudaMemcpy(h_C, d_C, size, cudaMemcpyDeviceToHost));

    // Verifikasi hasil
    bool success = true;
    int firstErrorIndex = -1;
    for (int i = 0; i < numElements; ++i) {
        float expected = h_A[i] + h_B[i];
        if (fabs(expected - h_C[i]) > 1e-5) {
            success = false;
            firstErrorIndex = i;
            break;
        }
    }
    
    if (success) {
        std::cout << "SUKSES: Hasil perhitungan CUDA sesuai!" << std::endl;
    } else {
        std::cout << "GAGAL: Hasil tidak sesuai!" << std::endl;
        std::cout << "Contoh error pada index " << firstErrorIndex << ":" << std::endl;
        std::cout << "A[" << firstErrorIndex << "] = " << h_A[firstErrorIndex] << std::endl;
        std::cout << "B[" << firstErrorIndex << "] = " << h_B[firstErrorIndex] << std::endl;
        std::cout << "Expected: " << h_A[firstErrorIndex] + h_B[firstErrorIndex] << std::endl;
        std::cout << "Actual: " << h_C[firstErrorIndex] << std::endl;
    }

    // Tampilkan beberapa contoh hasil
    std::cout << "\nContoh hasil (10 elemen pertama):" << std::endl;
    std::cout << "A[i] + B[i] = C[i]" << std::endl;
    for (int i = 0; i < 10; ++i) {
        std::cout << h_A[i] << " + " << h_B[i] << " = " << h_C[i] 
                  << " (expected: " << h_A[i] + h_B[i] << ")" << std::endl;
    }

    // Bersihkan memori
    delete[] h_A;
    delete[] h_B;
    delete[] h_C;
    
    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);
    
    // Reset device
    cudaDeviceReset();
    
    std::cout << "\nProgram selesai!" << std::endl;
    
    return success ? 0 : 1;
}