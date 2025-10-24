#include <iostream>
#include <vector>
#include <random>
#include <algorithm>
#include <iomanip>
#include <ctime>

using namespace std;

bool bs(vector<long long> data, long long n, long long key, int &times){
   int left=0,right=n-1,mid;
   while (left < right){
     times++;
     mid = (left+right)/2;
    //  cout<<left<<" "<<mid<<" "<<right<<"|";
     if (data[mid]==key) return 1;
     else if(key < data[mid]){
         right = mid-1;
     } else {
         left = mid+1;
     }
   }
   return 0;
}

vector<long long> generateSortedArrayRandomStep(int n, int start = 1, int minStep = 1, int maxStep = 10) {
    std::vector<long long> arr;
    
    // Random number generator
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<int> stepDist(minStep, maxStep);
    
    int current = start;
    for (int i = 0; i < n; i++) {
        arr.push_back(current);
        int step = stepDist(gen); // Generate random step
        current += step;
        // cout<<arr[i]<<" ";
    }
    
    return arr;
}


int main(){
    vector<long long> sizes = {10,1000,10000,100000,1000000,10000000};
    
    cout << left
         << setw(12) << "n"
         << setw(12) << "T(n)"
         << setw(10) << "Key"
         << setw(10) << "Test Index" << endl;
    for (auto n : sizes) {
        // long long n = 100000000;
        vector<long long> data = generateSortedArrayRandomStep(n);
        srand(static_cast<unsigned int>(time(NULL)));
        long long random_index =  (long long) (((double) rand() / RAND_MAX) * n) ;
        // cout << "Random number: " << random_index<< std::endl;
        long long key = random_index;
        int times=0;
        bool found = bs(data, n, key, times);
        cout << left
             << setw(12) << n
             << setw(12) << times
             << setw(10) << key
            //  << setw(10) << random_index<<endl;
             << setw(10) << (found ? "Found" : "Not Found") << endl;
    }
}