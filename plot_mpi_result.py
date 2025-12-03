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

# Buat figure dengan 2 subplot horizontal
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Subplot 1 (kiri): Line plot dengan annotasi
# Plot untuk MPI_Reduce
mpi_reduce_data = df[df['method'] == 'MPI_Reduce']
axes[0].plot(mpi_reduce_data['np'], mpi_reduce_data['duration'], 
         marker='o', linewidth=2, markersize=8, label='MPI_Reduce')

# Plot untuk Send-Receive
send_receive_data = df[df['method'] == 'Send-Receive']
axes[0].plot(send_receive_data['np'], send_receive_data['duration'], 
         marker='s', linewidth=2, markersize=8, label='Send-Receive')

# Konfigurasi subplot kiri
axes[0].set_xlabel('Number of Processes (np)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Duration (seconds)', fontsize=12, fontweight='bold')
axes[0].set_title('Perbandingan Running Time MPI Methods\nBerdasarkan Number of Processes', 
          fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(True, alpha=0.3)
axes[0].set_xticks(range(1, 7))

# Tambahkan annotasi nilai pada setiap titik
for i, row in mpi_reduce_data.iterrows():
    axes[0].annotate(f"{row['duration']:.4f}", 
                (row['np'], row['duration']), 
                textcoords="offset points", 
                xytext=(0,10), 
                ha='center', 
                fontsize=8)

for i, row in send_receive_data.iterrows():
    axes[0].annotate(f"{row['duration']:.4f}", 
                (row['np'], row['duration']), 
                textcoords="offset points", 
                xytext=(0,10), 
                ha='center', 
                fontsize=8)

# Subplot 2 (kanan): Bar plot
sns.barplot(data=df, x='np', y='duration', hue='method', ax=axes[1])

axes[1].set_xlabel('Number of Processes (np)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Duration (seconds)', fontsize=12, fontweight='bold')
axes[1].set_title('Perbandingan Running Time MPI Methods\n(Bar Chart)', 
          fontsize=14, fontweight='bold')
axes[1].legend(title='Method')

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