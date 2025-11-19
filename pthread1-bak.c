#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <math.h>
#include <time.h>
#include <iostream>

#define num_thread 8  // Bisa diubah sesuai kebutuhan
#define num_sum 1.e+10  // Diperbesar untuk melihat efek paralelisasi lebih jelas

pthread_t threads[num_thread];
pthread_mutex_t mutex_sum;
unsigned long long total_sum = 0;  // Variabel global untuk menyimpan total

struct ThreadResult {
    unsigned long long partial_sum;
    double time_taken;
    int thread_id;
};

void *Sum(void *arg)
{
    int myid = (int)(long)arg;
    clock_t start, end;
    double time_dif = 0;
    unsigned long long partial_sum = 0;
    unsigned long long range = floor(num_sum/num_thread);
    
    // Hitung start dan end untuk thread ini
    unsigned long long start_index = myid * range;
    unsigned long long end_index = (myid == num_thread - 1) ? num_sum : start_index + range;
    
    start = clock();
    for (unsigned long long i = start_index; i < end_index; i++) {
        partial_sum += i;
    }
    end = clock();
    
    time_dif = (double)(end - start) / CLOCKS_PER_SEC;
    
    // Menggunakan mutex untuk menghindari race condition saat update total
    pthread_mutex_lock(&mutex_sum);
    total_sum += partial_sum;
    pthread_mutex_unlock(&mutex_sum);
    
    // Alokasi memori untuk hasil thread
    ThreadResult* result = new ThreadResult;
    result->partial_sum = partial_sum;
    result->time_taken = time_dif;
    result->thread_id = myid;
    
    // printf("Thread ID: %d, range=%llu-%llu, partial_sum=%llu, time=%f seconds\n", 
    //        myid, start_index, end_index-1, partial_sum, time_dif);
    
    return result;
}

int main()
{
    pthread_mutex_init(&mutex_sum, NULL);
    ThreadResult* results[num_thread];
    
    printf("Starting parallel summation with %.0f elements using %d threads...\n", 
           num_sum, num_thread);
    
    // Hitung total secara serial untuk perbandingan
    clock_t serial_start = clock();
    unsigned long long serial_sum = 0;
    for (unsigned long long i = 0; i < num_sum; i++) {
        serial_sum += i;
    }
    clock_t serial_end = clock();
    double serial_time = (double)(serial_end - serial_start) / CLOCKS_PER_SEC;
    
    // Mulai thread paralel dengan LOOP
    clock_t parallel_start = clock();
    
    for (int i = 0; i < num_thread; i++) {
        pthread_create(&threads[i], NULL, &Sum, (void*)(long)i);
    }
    
    // Join semua thread dan kumpulkan hasil
    for (int i = 0; i < num_thread; i++) {
        pthread_join(threads[i], (void**)&results[i]);
    }
    
    clock_t parallel_end = clock();
    double parallel_time = (double)(parallel_end - parallel_start) / CLOCKS_PER_SEC;
    
    // Tampilkan hasil
    printf("\n=== PARALLEL RESULTS ===\n");
    for (int i = 0; i < num_thread; i++) {
        printf("Thread %d: partial_sum = %llu, time = %f seconds\n", 
               results[i]->thread_id, results[i]->partial_sum, results[i]->time_taken);
    }
    
    printf("\n=== SUMMARY ===\n");
    printf("Total parallel sum: %llu\n", total_sum);
    printf("Parallel execution time: %f seconds\n", parallel_time);
    
    printf("\nSerial sum: %llu\n", serial_sum);
    printf("Serial execution time: %f seconds\n", serial_time);
    
    printf("\nSpeedup: %.2fx\n", serial_time/parallel_time);
    printf("Results match: %s\n", (total_sum == serial_sum) ? "YES" : "NO");
    
    double efficiency = (serial_time/parallel_time) / num_thread * 100;
    printf("Efficiency: %.2f%%\n", efficiency);
    
    // Bersihkan memori
    for (int i = 0; i < num_thread; i++) {
        delete results[i];
    }
    pthread_mutex_destroy(&mutex_sum);
    
    pthread_exit(NULL);
    return 0; 
}