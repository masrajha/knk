#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <math.h>
#include <time.h>
#include <chrono>
#include <iostream>
#include <vector>

using namespace std;
// #define num_thread 2
// #define num_sum 1.e+9
struct ThreadData{
    int thread_id;
    int num_thread;
    unsigned long long num_sum;
};
// pthread_t tid2;


void *Sum(void *arg)	//Sum(0), Sum(1), Sum(2), Sum(3)
{
    ThreadData* data = (ThreadData*) arg;
    int myid = data->thread_id; 
    unsigned long long num_sum = data->num_sum;
    int num_thread=data->num_thread;
    // std::cout << "Thread ID: " << myid << ", num_sum: " << num_sum << ", num_thread: " << num_thread << std::endl;
    double time_dif=0;
	unsigned long int i;
	unsigned long int sum=0;
	unsigned long int range = floor(num_sum/num_thread);//jika ada 4 thread dan 10^7 data maka tiap thread sum(2.500.000)
	
    auto start = std::chrono::high_resolution_clock::now();
	for (i=myid*range; i< myid*range+range;i++)	//change this size and see the time execution in each thread.
												//compare to the serial summation.
		sum+=i;
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    // printf("Thread ID: %d, range=%ld, sum=%ld start:%ld end:%ld dif:%f\n", myid, range, sum, start, end, time_dif);
    // std::cout << "Thread ID: " << myid << ", range=" << range << ", sum=" << sum 
    //           << ", start=" << start.time_since_epoch().count()
    //           << ", end=" << end.time_since_epoch().count()
    //           << ", time=" << duration.count()/1000000.0 << " micro seconds" << std::endl;
    return NULL;
}
double run_paralel(int num_thread, unsigned long int num_sum){
    ThreadData thread_data[num_thread];
    pthread_t tid[num_thread];
    auto start = std::chrono::high_resolution_clock::now();
    
    for (int i = 0; i < num_thread; i++){
        thread_data[i].thread_id = i;
        thread_data[i].num_thread = num_thread;
        thread_data[i].num_sum = num_sum;
        pthread_create(&tid[i], NULL, &Sum, &thread_data[i]);		//Sum(0), Sum(1), Sum(2), Sum(3)
    }
    
    for (int i = 0; i < num_thread; i++){
		pthread_join(tid[i],NULL);
	}

    auto end = std::chrono::high_resolution_clock::now();
    auto paralel_duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    double paralel_time = paralel_duration.count()/1000000.0;
    return paralel_time;
}

int main(int argc, char* argv[]){

    // long int n[]={0,1,2,3};
    int num_thread=2; // Change this value to test with different number of threads
    unsigned long int num_sum=1.e+8; // Change this value to test with different sum sizes
    
    if (argc >= 3){
        num_thread = atoi(argv[1]);
        num_sum = strtoull(argv[2], NULL, 10);
    } else if (argc == 2){
        num_sum = strtoull(argv[1], NULL, 10);
    }
    
    // std::cout << "Paralel time summary: start=" << start.time_since_epoch().count()
    //           << ", end=" << end.time_since_epoch().count()
    //           << ", time=" << paralel_time << " micro seconds" << std::endl;
    
    auto start = std::chrono::high_resolution_clock::now();
    unsigned long int serial_sum =0;
    for (unsigned long int j=0; j< num_sum; j++){
        serial_sum+=j;
    }
    auto end = std::chrono::high_resolution_clock::now();
    auto serial_duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    double serial_time = serial_duration.count()/1000000.0;              
            
    // std::cout << "Serial time summary: start=" << start.time_since_epoch().count()
    //           << ", end=" << end.time_since_epoch().count()
    //           << ", time=" << serial_time<< " micro seconds" << std::endl;

    if (argc >= 3){
        double paralel_time = run_paralel(num_thread, num_sum);
        // std::cout<<(int) num_thread<<","<< (long long) num_sum<<","<<(double) paralel_time<<","<<(double) serial_time <<std::endl;
        printf("%d,%ld,%f,%f\n",num_thread,num_sum,paralel_time,serial_time);
    } else if(argc ==2){
        vector <double> paralel_times;
        int thread_counts[] = {2,4,5,8};
        for (int num_thread : thread_counts){
            double paralel_time = run_paralel(num_thread, num_sum);
            paralel_times.push_back(paralel_time);
        }
        // printf("num_sum,paralel_time_2,paralel_time_4,,paralel_time_5,paralel_time_8,paralel_time_10,serial_time\n");
        printf("%ld",num_sum);
        for (double t : paralel_times){
            printf(",%f",t);
        }
        printf(",%f\n",serial_time);
    }
    pthread_exit(NULL);
    return 0; 
}
