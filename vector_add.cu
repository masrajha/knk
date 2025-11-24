#include <iostream>
#include <cuda_runtime.h>

// Kernel CUDA untuk menjumlahkan dua vektor
__global__ void vectorAdd(const float *A, const float *B, float *C, int numElements) {
    int i = blockDim.x * blockIdx.x + threadIdx.x;
    
    if (i < numElements) {
        C[i] = A[i] + B[i];
    }
}

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
    
    cudaMalloc((void**)&d_A, size);
    cudaMalloc((void**)&d_B, size);
    cudaMalloc((void**)&d_C, size);

    // Salin data dari host ke device
    cudaMemcpy(d_A, h_A, size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B, size, cudaMemcpyHostToDevice);

    // Launch kernel CUDA
    int threadsPerBlock = 256;
    int blocksPerGrid = (numElements + threadsPerBlock - 1) / threadsPerBlock;
    
    std::cout << "Launching kernel dengan " << blocksPerGrid << " blocks x " 
              << threadsPerBlock << " threads" << std::endl;
    
    vectorAdd<<<blocksPerGrid, threadsPerBlock>>>(d_A, d_B, d_C, numElements);
    
    // Tunggu sampai kernel selesai
    cudaDeviceSynchronize();

    // Salin hasil dari device ke host
    cudaMemcpy(h_C, d_C, size, cudaMemcpyDeviceToHost);

    // Verifikasi hasil
    bool success = true;
    for (int i = 0; i < numElements; ++i) {
        if (fabs(h_A[i] + h_B[i] - h_C[i]) > 1e-5) {
            success = false;
            break;
        }
    }
    
    if (success) {
        std::cout << "SUKSES: Hasil perhitungan CUDA sesuai!" << std::endl;
    } else {
        std::cout << "GAGAL: Hasil tidak sesuai!" << std::endl;
    }

    // Tampilkan beberapa contoh hasil
    std::cout << "\nContoh hasil (10 elemen pertama):" << std::endl;
    std::cout << "A[i] + B[i] = C[i]" << std::endl;
    for (int i = 0; i < 10; ++i) {
        std::cout << h_A[i] << " + " << h_B[i] << " = " << h_C[i] << std::endl;
    }

    // Bersihkan memori
    delete[] h_A;
    delete[] h_B;
    delete[] h_C;
    
    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);
    
    std::cout << "\nProgram selesai!" << std::endl;
    
    return 0;
}