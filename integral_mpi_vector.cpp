/* C++ MPI Example with Full Vector Communication */
#include <mpi.h>
#include <math.h>
#include <stdio.h>
#include <time.h>
#include <vector>
#include <iostream>
#include <numeric>

using namespace std;

double fct(double x)
{
    return cos(x);
}

vector<double> integral(double a, int n, double h);

// Function to send vector using MPI
void send_vector(const vector<double>& vec, int dest, int tag) {
    int size = vec.size();
    // First send the size
    MPI_Send(&size, 1, MPI_INT, dest, tag, MPI_COMM_WORLD);
    // Then send the data if size > 0
    if (size > 0) {
        MPI_Send(vec.data(), size, MPI_DOUBLE, dest, tag + 1, MPI_COMM_WORLD);
    }
}

// Function to receive vector using MPI
vector<double> receive_vector(int source, int tag) {
    MPI_Status status;
    int size;
    
    // First receive the size
    MPI_Recv(&size, 1, MPI_INT, source, tag, MPI_COMM_WORLD, &status);
    
    vector<double> result(size);
    // Then receive the data if size > 0
    if (size > 0) {
        MPI_Recv(result.data(), size, MPI_DOUBLE, source, tag + 1, 
                MPI_COMM_WORLD, &status);
    }
    
    return result;
}

int main(int argc, char *argv[])
{
    long int n, i, num;
    double h, a, b, pi;
    double my_a, my_range;
    time_t start, end;

    if (argc < 2)
    {
        printf("Usage: mpirun -np <num_processes> %s <method: r or sr>\n", argv[0]);
        return 0;
    }

    int myid, p;
    double duration;

    pi = acos(-1.0);
    a = 0.;
    b = pi * 1. / 2.;
    n = 100000;  // Reduced for vector communication demo

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &myid);
    MPI_Comm_size(MPI_COMM_WORLD, &p);

    h = (b - a) / n;
    num = n / p;
    my_range = (b - a) / p;
    my_a = a + myid * my_range;

    start = clock();
    
    // Each process computes its portion as vector
    vector<double> local_vector = integral(my_a, num, h);
    
    double result = 0.0;
    vector<double> all_results;

    if (argc >= 2 && argv[1][0] == 'r')
    {
        // Method 1: Reduce only the sum
        double local_sum = accumulate(local_vector.begin(), local_vector.end(), 0.0);
        MPI_Reduce(&local_sum, &result, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);
        
        if (myid == 0) {
            all_results.push_back(result);
        }
    }
    else
    {
        // Method 2: Send-Receive full vectors
        if (myid == 0)
        {
            // Root process collects all vectors
            all_results = local_vector;
            
            for (int i = 1; i < p; i++)
            {
                vector<double> received_vec = receive_vector(i, 100);
                all_results.insert(all_results.end(), 
                                 received_vec.begin(), received_vec.end());
            }
            
            // Calculate final result from all vectors
            result = accumulate(all_results.begin(), all_results.end(), 0.0);
            
            // Optional: Print vector statistics
            // printf("Collected %lu elements from all processes\n", all_results.size());
        }
        else
        {
            // Worker processes send their vectors to root
            send_vector(local_vector, 0, 100);
        }
    }
    
    if (myid == 0)
    {
        end = clock();
        duration = (end - start)/(CLOCKS_PER_SEC*1.0);
        
        // printf("The total integral result = %.15f\n", result);
        // printf("Total time taken = %f seconds\n", duration);
        // printf("Method used: %s\n", (argc >= 2 && argv[1][0] == 'r') ? "MPI_Reduce" : "Send-Receive-Vector");
        // printf("Error: %.15f\n", fabs(result - 1.0));
        
        // // For data analysis
        // printf("Processes: %d, Elements per process: %ld\n", p, num);

        //Print as row data
        printf("%s,%d,%f,%f\n", (argc >= 2 && argv[1][0] == 'r') ? "MPI_Reduce" : "Send-Receive-Vector", p, result, duration);
    }
    
    MPI_Finalize();
    return 0;
}

vector<double> integral(double a, int n, double h)
{
    vector<double> integ;
    double h2 = h / 2.0;
    
    for (int j = 0; j < n; j++)
    {
        double aij = a + j * h;
        integ.push_back(fct(aij + h2) * h);
    }
    return integ;
}