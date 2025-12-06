#include <mpi.h>
#include <iostream>
#include <cstring>

int main(int argc, char** argv) {
    // Inisialisasi MPI
    MPI_Init(&argc, &argv);

    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

    // Dapatkan nama prosesor
    char processor_name[MPI_MAX_PROCESSOR_NAME];
    int name_len;
    MPI_Get_processor_name(processor_name, &name_len);

    // Contoh pertukaran pesan
    if (world_rank == 0) {
        // Process 0 mengirim pesan ke process 1
        char message[] = "Halo dari process 0!";
        MPI_Send(message, strlen(message)+1, MPI_CHAR, 1, 0, MPI_COMM_WORLD);
        std::cout << "Process 0 mengirim pesan: " << message << std::endl;
    }
    else if (world_rank == 1) {
        // Process 1 menerima pesan dari process 0
        char received_message[100];
        MPI_Recv(received_message, 100, MPI_CHAR, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        std::cout << "Process 1 menerima pesan: " << received_message << std::endl;
    }

    // Contoh penggunaan broadcast
    int data_broadcast;
    if (world_rank == 0) {
        data_broadcast = 100;
    }
    MPI_Bcast(&data_broadcast, 1, MPI_INT, 0, MPI_COMM_WORLD);
    std::cout << "Process " << world_rank << " menerima data broadcast: " << data_broadcast << std::endl;

    // Contoh penggunaan reduce (sum)
    int local_data = world_rank * 10;
    int global_sum;
    MPI_Reduce(&local_data, &global_sum, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);
    
    if (world_rank == 0) {
        std::cout << "Total sum dari semua process: " << global_sum << std::endl;
    }

    // Finalisasi MPI
    MPI_Finalize();
    return 0;
}