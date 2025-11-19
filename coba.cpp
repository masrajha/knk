#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <math.h>
#include <time.h>
#include <sys/time.h>
#include <iostream>
#include <vector>
#include <iomanip>
#include <string>
#include <sstream>

using namespace std;

// Struct untuk menyimpan hasil eksekusi paralel
struct ParallelResult {
    int num_thread;
    double num_sum;
    double total_time;
    unsigned long long total_sum;
    double average_thread_time;
};

// Struct untuk data thread dengan padding untuk menghindari false sharing
struct ThreadData {
    int thread_id;
    unsigned long long start_index;
    unsigned long long end_index;
    unsigned long long partial_sum;
    double thread_time;
    char padding[64]; // Padding untuk mencegah false sharing (typical cache line size)
};

// Variabel global untuk shared data - DIHAPUS, gunakan reduksi manual
vector<unsigned long long> partial_sums;

void *Sum(void *arg) {
    ThreadData* data = static_cast<ThreadData*>(arg);
    struct timeval start, end;
    
    gettimeofday(&start, NULL);
    data->partial_sum = 0;
    
    // Loop yang dioptimalkan - hindari operasi mahal dalam loop
    unsigned long long local_sum = 0;
    for (unsigned long long i = data->start_index; i < data->end_index; i++) {
        local_sum += i;
    }
    data->partial_sum = local_sum;
    
    gettimeofday(&end, NULL);
    
    // Hitung waktu eksekusi thread dalam detik
    data->thread_time = (end.tv_sec - start.tv_sec) + 
                       (end.tv_usec - start.tv_usec) / 1000000.0;
    
    // Simpan partial sum tanpa mutex - akan dikumpulkan nanti
    partial_sums[data->thread_id] = data->partial_sum;
    
    return nullptr;
}

// Fungsi parallel_sum yang dioptimalkan
ParallelResult parallel_sum_optimized(int num_thread, double num_sum) {
    // Reset partial sums
    partial_sums.clear();
    partial_sums.resize(num_thread, 0);
    
    // Konversi num_sum ke integer
    unsigned long long n = static_cast<unsigned long long>(num_sum);
    
    // Hitung range untuk setiap thread dengan pembagian yang lebih baik
    unsigned long long base_range = n / num_thread;
    unsigned long long remainder = n % num_thread;
    
    // Buat array untuk thread dan data thread
    pthread_t* threads = new pthread_t[num_thread];
    ThreadData* thread_data = new ThreadData[num_thread];
    
    // Waktu mulai eksekusi paralel
    struct timeval start_time, end_time;
    gettimeofday(&start_time, NULL);
    
    // Buat dan mulai thread
    unsigned long long current_start = 0;
    for (int i = 0; i < num_thread; i++) {
        thread_data[i].thread_id = i;
        thread_data[i].start_index = current_start;
        
        // Distribusikan remainder secara merata
        unsigned long long thread_range = base_range + (i < remainder ? 1 : 0);
        thread_data[i].end_index = current_start + thread_range;
        current_start = thread_data[i].end_index;
        
        pthread_create(&threads[i], NULL, &Sum, &thread_data[i]);
    }
    
    // Join semua thread
    for (int i = 0; i < num_thread; i++) {
        pthread_join(threads[i], NULL);
    }
    
    // Waktu selesai eksekusi paralel
    gettimeofday(&end_time, NULL);
    
    // Hitung total sum dari partial sums (reduksi serial - lebih efisien)
    unsigned long long total_sum = 0;
    for (int i = 0; i < num_thread; i++) {
        total_sum += partial_sums[i];
    }
    
    // Hitung total waktu dan rata-rata waktu thread
    double total_time = (end_time.tv_sec - start_time.tv_sec) + 
                       (end_time.tv_usec - start_time.tv_usec) / 1000000.0;
    
    double avg_thread_time = 0.0;
    for (int i = 0; i < num_thread; i++) {
        avg_thread_time += thread_data[i].thread_time;
    }
    avg_thread_time /= num_thread;
    
    // Buat hasil
    ParallelResult result;
    result.num_thread = num_thread;
    result.num_sum = num_sum;
    result.total_time = total_time;
    result.total_sum = total_sum;
    result.average_thread_time = avg_thread_time;
    
    // Bersihkan memori
    delete[] threads;
    delete[] thread_data;
    
    return result;
}

// Fungsi untuk menghitung sum secara serial yang dioptimalkan
pair<unsigned long long, double> serial_sum_optimized(double num_sum) {
    unsigned long long n = static_cast<unsigned long long>(num_sum);
    unsigned long long sum = 0;
    
    struct timeval start, end;
    gettimeofday(&start, NULL);
    
    // Loop yang dioptimalkan
    for (unsigned long long i = 0; i < n; i++) {
        sum += i;
    }
    
    gettimeofday(&end, NULL);
    double time_taken = (end.tv_sec - start.tv_sec) + 
                       (end.tv_usec - start.tv_usec) / 1000000.0;
    
    return make_pair(sum, time_taken);
}

// Fungsi untuk menjalankan eksperimen
vector<vector<string>> run_experiments_optimized(const vector<int>& thread_counts, const vector<double>& sum_sizes) {
    vector<vector<string>> results;
    
    // Header tabel
    vector<string> header = {
        "Threads", "Num Sum", "Avg Thread Time(s)", "Parallel Time(s)", 
        "Serial Time(s)", "Sum Result", "Correct", "SpeedUp", "Efficiency(%)"
    };
    results.push_back(header);
    
    for (double sum_size : sum_sizes) {
        // Hitung serial time sekali untuk setiap sum_size
        auto serial_result = serial_sum_optimized(sum_size);
        unsigned long long serial_sum_value = serial_result.first;
        double serial_time = serial_result.second;
        
        for (int thread_count : thread_counts) {
            cout << "Running: " << thread_count << " threads, " << sum_size << " elements..." << endl;
            
            // Eksekusi paralel
            ParallelResult parallel_result = parallel_sum_optimized(thread_count, sum_size);
            
            // Hitung speedup dan efficiency
            double speedup = (serial_time > 0) ? serial_time / parallel_result.total_time : 0;
            double efficiency = (speedup > 0) ? (speedup / thread_count) * 100 : 0;
            bool correct = (parallel_result.total_sum == serial_sum_value);
            
            // Simpan hasil dalam vector
            vector<string> row;
            row.push_back(to_string(thread_count));
            row.push_back(to_string(static_cast<long long>(sum_size)));
            row.push_back(to_string(parallel_result.average_thread_time));
            row.push_back(to_string(parallel_result.total_time));
            row.push_back(to_string(serial_time));
            row.push_back(to_string(parallel_result.total_sum));
            row.push_back(correct ? "YES" : "NO");
            row.push_back(to_string(speedup));
            row.push_back(to_string(efficiency));
            
            results.push_back(row);
        }
    }
    
    return results;
}

// Fungsi untuk menampilkan tabel
void print_table(const vector<vector<string>>& data) {
    if (data.empty()) return;
    
    // Hitung lebar maksimum untuk setiap kolom
    vector<size_t> column_widths(data[0].size(), 0);
    for (const auto& row : data) {
        for (size_t i = 0; i < row.size(); i++) {
            if (row[i].length() > column_widths[i]) {
                column_widths[i] = row[i].length();
            }
        }
    }
    
    // Tambahkan padding
    for (size_t i = 0; i < column_widths.size(); i++) {
        column_widths[i] += 2;
    }
    
    // Cetak garis pemisah
    auto print_line = [&]() {
        cout << "+";
        for (size_t width : column_widths) {
            cout << string(width + 2, '-') << "+";
        }
        cout << endl;
    };
    
    // Cetak header
    print_line();
    cout << "|";
    for (size_t i = 0; i < data[0].size(); i++) {
        cout << " " << setw(column_widths[i]) << left << data[0][i] << " |";
    }
    cout << endl;
    print_line();
    
    // Cetak data
    for (size_t i = 1; i < data.size(); i++) {
        cout << "|";
        for (size_t j = 0; j < data[i].size(); j++) {
            string value = data[i][j];
            // Format angka
            if (j >= 2 && j <= 8 && j != 5 && j != 6) {
                try {
                    double num = stod(value);
                    stringstream ss;
                    if (num < 10) {
                        ss << fixed << setprecision(4) << num;
                    } else {
                        ss << fixed << setprecision(2) << num;
                    }
                    value = ss.str();
                } catch (...) {
                    // Biarkan sebagai string
                }
            }
            cout << " " << setw(column_widths[j]) << left << value << " |";
        }
        cout << endl;
    }
    print_line();
}

int main() {
    // Konfigurasi eksperimen - gunakan workload yang lebih besar
    vector<int> thread_counts = {1, 2, 4, 8};  // Tambah 1 thread untuk baseline
    vector<double> sum_sizes = {1.e+7, 1.e+8, 1.e+9};  // Tambah workload lebih besar
    
    cout << "OPTIMIZED PARALLEL SUMMATION EXPERIMENT RESULTS" << endl;
    cout << "==============================================" << endl;
    cout << "Key Optimizations:" << endl;
    cout << "1. Removed mutex from computation" << endl;
    cout << "2. Added padding to prevent false sharing" << endl;
    cout << "3. Better workload distribution" << endl;
    cout << "4. Manual reduction after thread completion" << endl;
    cout << "==============================================" << endl << endl;
    
    // Jalankan eksperimen
    vector<vector<string>> results_table = run_experiments_optimized(thread_counts, sum_sizes);
    
    // Tampilkan tabel
    print_table(results_table);
    
    // Analisis hasil
    cout << endl << "PERFORMANCE ANALYSIS:" << endl;
    cout << "====================" << endl;
    
    for (size_t i = 1; i < results_table.size(); i++) {
        int threads = stoi(results_table[i][0]);
        double num_sum = stod(results_table[i][1]);
        double speedup = stod(results_table[i][7]);
        
        if (threads == 1) {
            cout << "Baseline (1 thread) for " << num_sum << " elements: " 
                 << results_table[i][3] << " seconds" << endl;
        } else if (speedup > 1.0) {
            cout << "✓ GOOD: " << threads << " threads with " << num_sum 
                 << " elements - Speedup: " << speedup << "x" << endl;
        } else {
            cout << "✗ POOR: " << threads << " threads with " << num_sum 
                 << " elements - Speedup: " << speedup << "x (overhead too high)" << endl;
        }
    }
    
    return 0;
}