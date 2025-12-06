#include <pthread.h>
#include <iostream>

// Fungsi yang akan dijalankan oleh thread
void* printMessage(void* message) {
    char* msg = static_cast<char*>(message);
    std::cout << "Thread: " << msg << std::endl;
    return nullptr;
}

void program1() {
    pthread_t thread1, thread2;
    const char* message1 = "Hello from Thread 1!";
    const char* message2 = "Hello from Thread 2!";
    
    // Membuat thread
    pthread_create(&thread1, NULL, printMessage, (void*)message1);
    pthread_create(&thread2, NULL, printMessage, (void*)message2);
    
    // Menunggu thread selesai
    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);
    
    std::cout << "Main thread finished" << std::endl;
}

struct ThreadData {
    int id;
    int value;
};

void* workerThread(void* arg) {
    ThreadData* data = static_cast<ThreadData*>(arg);
    std::cout << "Thread " << data->id << " processing value: " 
              << data->value << std::endl;
    return nullptr;
}

void program2() {
    pthread_t threads[3];
    ThreadData data[3];
    
    for (int i = 0; i < 3; i++) {
        data[i].id = i;
        data[i].value = i * 100;
        pthread_create(&threads[i], NULL, workerThread, &data[i]);
    }
    
    for (int i = 0; i < 3; i++) {
        pthread_join(threads[i], NULL);
    }
}

int main() {
    std::cout << "Running Program 1:" << std::endl;
    program1();
    
    std::cout << "\nRunning Program 2:" << std::endl;
    program2();
    
    return 0;
}   