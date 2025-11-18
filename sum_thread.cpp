#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <math.h>
#include <time.h>
#include <sys/time.h>
#include <iostream>

// Struct untuk menyimpan hasil eksekusi paralel
struct ParallelResult {
    int num_thread;
    double num_sum;
    double total_time;
    unsigned long long total_sum;
};

// Struct untuk data thread
struct ThreadData {
    int thread_id;
    unsigned long long start_index;
    unsigned long long end_index;
    unsigned long long partial_sum;
    double thread_time;
};

// Variabel global untuk shared data
pthread_mutex_t mutex_sum;
unsigned long long global_total_sum = 0;

void *Sum(void *arg) {
    ThreadData* data = static_cast<ThreadData*>(arg);
    struct timeval start, end;
    
    gettimeofday(&start, NULL);
    data->partial_sum = 0;
    
    for (unsigned long long i = data->start_index; i < data->end_index; i++) {
        data->partial_sum += i;
    }
    
    gettimeofday(&end, NULL);
    
    // Hitung waktu eksekusi thread dalam detik
    data->thread_time = (end.tv_sec - start.tv_sec) + 
                       (end.tv_usec - start.tv_usec) / 1000000.0;
    
    // Update total global dengan proteksi mutex
    pthread_mutex_lock(&mutex_sum);
    global_total_sum += data->partial_sum;
    pthread_mutex_unlock(&mutex_sum);
    
    printf("Thread %d: partial_sum = %llu, time = %f seconds\n", 
           data->thread_id, data->partial_sum, data->thread_time);
    
    return nullptr;
}

// Fungsi parallel_sum yang diminta
ParallelResult parallel_sum(int num_thread, double num_sum) {
    // Inisialisasi mutex
    pthread_mutex_init(&mutex_sum, NULL);
    global_total_sum = 0;
    
    // Konversi num_sum ke integer
    unsigned long long n = static_cast<unsigned long long>(num_sum);
    
    // Hitung range untuk setiap thread
    unsigned long long range = n / num_thread;
    
    // Buat array untuk thread dan data thread
    pthread_t* threads = new pthread_t[num_thread];
    ThreadData* thread_data = new ThreadData[num_thread];
    
    // Waktu mulai eksekusi paralel
    struct timeval start_time, end_time;
    gettimeofday(&start_time, NULL);
    
    // Buat thread
    for (int i = 0; i < num_thread; i++) {
        thread_data[i].thread_id = i;
        thread_data[i].start_index = i * range;
        thread_data[i].end_index = (i == num_thread - 1) ? n : (i + 1) * range;
        
        pthread_create(&threads[i], NULL, &Sum, &thread_data[i]);
    }
    
    // Join semua thread
    for (int i = 0; i < num_thread; i++) {
        pthread_join(threads[i], NULL);
    }
    
    // Waktu selesai eksekusi paralel
    gettimeofday(&end_time, NULL);
    
    // Hitung total waktu
    double total_time = (end_time.tv_sec - start_time.tv_sec) + 
                       (end_time.tv_usec - start_time.tv_usec) / 1000000.0;
    
    // Buat hasil
    ParallelResult result;
    result.num_thread = num_thread;
    result.num_sum = num_sum;
    result.total_time = total_time;
    result.total_sum = global_total_sum;
    
    // Bersihkan memori
    delete[] threads;
    delete[] thread_data;
    pthread_mutex_destroy(&mutex_sum);
    
    return result;
}

// Fungsi untuk menghitung sum secara serial (untuk perbandingan)
unsigned long long serial_sum(double num_sum) {
    unsigned long long n = static_cast<unsigned long long>(num_sum);
    unsigned long long sum = 0;
    
    struct timeval start, end;
    gettimeofday(&start, NULL);
    
    for (unsigned long long i = 0; i < n; i++) {
        sum += i;
    }
    
    gettimeofday(&end, NULL);
    double time_taken = (end.tv_sec - start.tv_sec) + 
                       (end.tv_usec - start.tv_usec) / 1000000.0;
    
    printf("Serial sum: %llu, time = %f seconds\n", sum, time_taken);
    return sum;
}

int main() {
    // Test dengan berbagai konfigurasi
    int thread_counts[] = {2, 4, 8};
    double sum_sizes[] = {1.e+7, 1.e+8};
    
    for (double sum_size : sum_sizes) {
        for (int thread_count : thread_counts) {
            printf("\n=== Testing with num_thread=%d, num_sum=%.0f ===\n", 
                   thread_count, sum_size);
            
            // Eksekusi paralel
            ParallelResult result = parallel_sum(thread_count, sum_size);
            
            // Verifikasi dengan serial
            unsigned long long serial_result = serial_sum(sum_size);
            
            // Tampilkan hasil
            printf("\n--- PARALLEL RESULT ---\n");
            printf("Num Thread: %d\n", result.num_thread);
            printf("Num Sum: %.0f\n", result.num_sum);
            printf("Total Sum: %llu\n", result.total_sum);
            printf("Total Time: %f seconds\n", result.total_time);
            printf("Results match: %s\n", 
                   (result.total_sum == serial_result) ? "YES" : "NO");
            
            // Hitung speedup (bandingkan dengan serial time)
            double serial_time = 0.0;
            struct timeval start, end;
            gettimeofday(&start, NULL);
            serial_sum(sum_size); // Hitung ulang untuk mendapatkan waktu
            gettimeofday(&end, NULL);
            serial_time = (end.tv_sec - start.tv_sec) + 
                         (end.tv_usec - start.tv_usec) / 1000000.0;
            
            if (serial_time > 0) {
                printf("Speedup: %.2fx\n", serial_time / result.total_time);
                printf("Efficiency: %.2f%%\n", 
                       (serial_time / result.total_time) / thread_count * 100);
            }
            
            printf("=====================\n");
        }
    }
    
    return 0;
}