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

# Nama file output untuk data vector
output_file="hasil_mpi_vector.csv"

# Tulis header ke file CSV
echo "method,np,result,duration,data_size" > "$output_file"

# Compile program MPI jika diperlukan
echo "Compiling program MPI..."
mpic++ integral_mpi_vector.cpp -o integral_vector

# Periksa apakah kompilasi berhasil
if [ $? -ne 0 ]; then
    echo "Error: Kompilasi gagal!"
    exit 1
fi

echo "Kompilasi berhasil. Menjalankan benchmark..."

# Loop untuk jumlah proses 1 sampai 6
for np in {1..6}; do
    # Loop untuk kedua metode (r dan s)
    for method in r s; do
        echo "Menjalankan mpirun -np $np integral_vector $method"
        
        # Jalankan program dan tangkap output
        output=$(mpirun -np "$np" integral_vector "$method" 2>/dev/null)
        
        # Ekstrak bagian yang diperlukan dari output
        # Format: [Method],[NP],[Result],[Duration],[Data_Size]
        hasil=$(echo "$output" | grep -E "(MPI_Reduce|Send-Receive-Vector)" | head -1)
        
        # Simpan ke file CSV jika hasil tidak kosong
        if [ -n "$hasil" ]; then
            echo "$hasil" >> "$output_file"
            echo "  -> $hasil"
        else
            echo "Peringatan: Tidak ada output untuk np=$np method=$method"
        fi
    done
done

echo "Selesai. Hasil disimpan di $output_file"

if [ -f "plot_mpi_result.py" ]; then
    echo "Menjalankan plot_mpi_result.py"
    python3 plot_mpi_result.py
else
    echo "File plot_mpi_result.py tidak ditemukan. Skipping plotting."
fi

if [ -f "plot_mpi_vector.py" ]; then
    echo "Menjalankan plot_mpi_vector.py"
    python3 plot_mpi_vector.py
else
    echo "File plot_mpi_vector.py tidak ditemukan. Skipping plotting."
fi


echo "Proses selesai. Check file:"
echo "- hasil_mpi_vector.csv (data mentah)"
echo "- hasil_mpi_vector_analysis.csv (data analisis lengkap)"
echo "- mpi_vector_performance.png (plot komprehensif)"
echo "- mpi_vector_detailed.png (plot detail)"
echo "- data_size_vs_duration.png (plot data size vs duration)"
echo "- speedup_vs_data_size.png (plot speedup vs data size)"