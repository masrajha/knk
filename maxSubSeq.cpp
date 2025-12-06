#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <iomanip>

#include <chrono>
#include <thread>

using ll = long long;
using namespace std;
using namespace std::chrono;



vector<long long> generateArray(ll n) {
    vector<long long> arr;
    arr.reserve(n); 
    srand(time(0));
    
    for (ll i = 0; i < n; i++) {
        int random_num = rand() % 41 - 20;
        arr.push_back(random_num);
    }
    
    return arr;
}

ll maxSubSum(const vector <ll>&arr){
    ll thisSum = 0, maxSum=0;
    for (ll i=0;i<arr.size();++i){
        thisSum += arr[i];
        if (thisSum>maxSum)
            maxSum=thisSum;
        else if(thisSum<0) 
            thisSum = 0;
    }
    return maxSum;
}

int main(){

    int n = 1000000;
    cout<<"Eksperimen n = "<<n<<endl;
    cout<<"#"
        <<setw(10)
        <<"Result"
        <<setw(15)
        <<"Time (ms)"<<endl;
    double timeAverage=0;
    for (int i =0; i<5;i++){
        vector<ll> arr = generateArray(n);
        auto start = high_resolution_clock::now();
        ll hasil = maxSubSum(arr);
        auto end = high_resolution_clock::now();
        auto duration = duration_cast<microseconds>(end - start);
        cout<<i
        <<setw(10)
        <<hasil
        <<setw(10)
        <<duration.count()
        <<endl;
        this_thread::sleep_for(milliseconds(1000));
        timeAverage += (double) duration.count()/5;
    }
    cout<<"Time Averge: "<<timeAverage;
    return 0;
}