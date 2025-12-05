#include <iostream>
#include <math.h>
#include <cuda_runtime.h>

// Kernel function to add the elements of two arrays
__global__ void add1(int n, float *x, float *y)
{
  for (int i = 0; i < n; i++)
    y[i] = x[i] + y[i];
}

__global__ 	void add2(int n, float *x, float *y)
{			//data = 10, thread = 5, 
			//threadId = 0, 1, 2, 3, 4
			//blockDim = 5		-> 1 block isinya 5 thread
			//threadId[0] = data ke-0 dan 5
			//threadId[1] = data ke-1 dan 6
			//threadId[2] = data ke-2 dan 7
			//threadId[3] = data ke-3 dan 8
			//threadId[4] = data ke-4 dan 9
  int index = threadIdx.x;		
  int stride = blockDim.x;		//berapa thread yang ada di dalam block tersebut
  for (int i = index; i < n; i += stride)		//threadId[0], i = 0, 5, 10, ... >n  //threadId[1], i = 1, 6, 11, ... , >n
      y[i] = x[i] + y[i];
}	//data 103 dengan 10 thread, berapa thread yang menganggur? 7 thread

__global__	void add3(int n, float *x, float *y)
{
  int index = blockIdx.x * blockDim.x + threadIdx.x;
  int stride = blockDim.x * gridDim.x;
  for (int i = index; i < n; i += stride)
    y[i] = x[i] + y[i];
}

int main(void)
{
  int N = 1<<20;
  float *x, *y;

  // Allocate Unified Memory – accessible from CPU or GPU
  cudaMallocManaged(&x, N*sizeof(float));
  cudaMallocManaged(&y, N*sizeof(float));

  // initialize x and y arrays on the host
  for (int i = 0; i < N; i++) {		// masukkan nilai array X dan Y (boleh dianggap matriks X dan Y)
    x[i] = 1.0f;
    y[i] = 2.0f;
  }

  // Run kernel on 1M elements on the GPU
  //cara 1
  // add1<<<1, 1>>>(N, x, y);
  // //cara 2
  // add2<<<1, 256>>>(N, x, y);
  //cara 3
  int blockSize = 256;
  int numBlocks = (N + blockSize - 1) / blockSize;
  add3<<<numBlocks, blockSize>>>(N, x, y);

  // Wait for GPU to finish before accessing on host
  cudaDeviceSynchronize();

  // Check for errors (all values should be 3.0f)
  float maxError = 0.0f;
  for (int i = 0; i < N; i++)
    maxError = fmax(maxError, fabs(y[i]-3.0f));
  std::cout << "Max error: " << maxError << std::endl;

  // Free memory
  cudaFree(x);
  cudaFree(y);
  
  return 0;
}
