import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style untuk plot yang lebih menarik
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Baca data dari file CSV
df = pd.read_csv('hasil_mpi.csv')

# Tampilkan data untuk memastikan terbaca dengan benar
print("Data yang dibaca:")
print(df.head(12))

# Buat plot perbandingan running time
plt.figure(figsize=(12, 8))

# Plot untuk MPI_Reduce
mpi_reduce_data = df[df['method'] == 'MPI_Reduce']
plt.plot(mpi_reduce_data['np'], mpi_reduce_data['duration'], 
         marker='o', linewidth=2, markersize=8, label='MPI_Reduce')

# Plot untuk Send-Receive
send_receive_data = df[df['method'] == 'Send-Receive']
plt.plot(send_receive_data['np'], send_receive_data['duration'], 
         marker='s', linewidth=2, markersize=8, label='Send-Receive')

# Konfigurasi plot
plt.xlabel('Number of Processes (np)', fontsize=12, fontweight='bold')
plt.ylabel('Duration (seconds)', fontsize=12, fontweight='bold')
plt.title('Perbandingan Running Time MPI Methods\nBerdasarkan Number of Processes', 
          fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)

# Set ticks untuk sumbu x (karena np dari 1-6)
plt.xticks(range(1, 7))

# Tambahkan annotasi nilai pada setiap titik
for i, row in mpi_reduce_data.iterrows():
    plt.annotate(f"{row['duration']:.4f}", 
                (row['np'], row['duration']), 
                textcoords="offset points", 
                xytext=(0,10), 
                ha='center', 
                fontsize=8)

for i, row in send_receive_data.iterrows():
    plt.annotate(f"{row['duration']:.4f}", 
                (row['np'], row['duration']), 
                textcoords="offset points", 
                xytext=(0,10), 
                ha='center', 
                fontsize=8)

plt.tight_layout()
plt.show()

# Buat plot alternatif menggunakan seaborn untuk visualisasi yang berbeda
plt.figure(figsize=(12, 8))
sns.lineplot(data=df, x='np', y='duration', hue='method', 
             marker='o', markersize=8, linewidth=2.5)

plt.xlabel('Number of Processes (np)', fontsize=12, fontweight='bold')
plt.ylabel('Duration (seconds)', fontsize=12, fontweight='bold')
plt.title('Perbandingan Running Time MPI Methods\n(Bentuk Alternatif)', 
          fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.xticks(range(1, 7))
plt.tight_layout()
plt.show()

# Buat bar plot untuk perbandingan yang lebih jelas
plt.figure(figsize=(12, 8))
sns.barplot(data=df, x='np', y='duration', hue='method')

plt.xlabel('Number of Processes (np)', fontsize=12, fontweight='bold')
plt.ylabel('Duration (seconds)', fontsize=12, fontweight='bold')
plt.title('Perbandingan Running Time MPI Methods\n(Bar Chart)', 
          fontsize=14, fontweight='bold')
plt.legend(title='Method')
plt.tight_layout()
plt.show()

# Tampilkan statistik deskriptif
print("\nStatistik Deskriptif Duration per Method:")
stats = df.groupby('method')['duration'].describe()
print(stats)

# Hitung speedup relatif terhadap single process
single_mpi = df[(df['method'] == 'MPI_Reduce') & (df['np'] == 1)]['duration'].values[0]
single_send = df[(df['method'] == 'Send-Receive') & (df['np'] == 1)]['duration'].values[0]

df['speedup'] = df.apply(lambda row: single_mpi/row['duration'] if row['method'] == 'MPI_Reduce' 
                        else single_send/row['duration'], axis=1)

print("\nSpeedup relatif terhadap single process:")
print(df[['method', 'np', 'duration', 'speedup']])