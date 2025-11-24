#include <iostream>
#include <thread> // Required for std::thread

int main() {
    unsigned int num_threads = std::thread::hardware_concurrency();

    if (num_threads > 0) {
        std::cout << "The system can run approximately " << num_threads 
                  << " concurrent threads." << std::endl;
    } else {
        std::cout << "The number of concurrent threads is not computable or well-defined on this system." << std::endl;
    }

    return 0;
}