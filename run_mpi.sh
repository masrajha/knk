#!/bin/bash

# Nama file output
output_file="hasil_mpi.csv"

# Tulis header ke file CSV
echo "method,np,result,duration" > "$output_file"

# Loop untuk jumlah proses 1 sampai 6
for np in {1..6}; do
    # Loop untuk kedua metode (r dan s)
    for method in r s; do
        echo "Menjalankan mpirun -np $np integral $method"
        
        # Jalankan program dan tangkap output
        output=$(mpirun -np "$np" integral "$method" 2>/dev/null)
        
        # Ekstrak bagian yang diperlukan dari output
        # Format: [Method],[NP],[Result],[Duration]
        hasil=$(echo "$output" | grep -E "(MPI_Reduce|Send-Receive)" | head -1)
        
        # Simpan ke file CSV jika hasil tidak kosong
        if [ -n "$hasil" ]; then
            echo "$hasil" >> "$output_file"
        else
            echo "Peringatan: Tidak ada output untuk np=$np method=$method"
        fi
    done
done

echo "Selesai. Hasil disimpan di $output_file"

# Jalankan script python untuk plotting jika file ada
if [ -f "plot_mpi_result.py" ]; then
    echo "Menjalankan plot_mpi_result.py"
    python3 plot_mpi_result.py
else
    echo "File plot_mpi_result.py tidak ditemukan. Skipping plotting."
fi