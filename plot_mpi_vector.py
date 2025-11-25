import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style untuk plot yang lebih menarik
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Baca data dari file CSV
df = pd.read_csv('hasil_mpi_vector.csv')

# Normalisasi nama method untuk konsistensi
df['method'] = df['method'].replace({'Send-Receive-Vector': 'Send-Receive'})

# Tampilkan data untuk memastikan terbaca dengan benar
print("Data MPI Vector yang dibaca:")
print(df.head(12))

# Buat plot perbandingan running time
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Perbandingan Performa MPI: Reduce vs Send-Receive (Vector Data)', 
             fontsize=16, fontweight='bold')

# Plot 1: Line plot comparison
ax1 = axes[0, 0]
for method in df['method'].unique():
    method_data = df[df['method'] == method]
    ax1.plot(method_data['np'], method_data['duration'], 
             marker='o', linewidth=2, markersize=8, label=method)

ax1.set_xlabel('Number of Processes (np)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Duration (seconds)', fontsize=12, fontweight='bold')
ax1.set_title('Line Plot: Running Time Comparison', fontsize=13, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_xticks(range(1, 7))

# Plot 2: Bar plot comparison
ax2 = axes[0, 1]
sns.barplot(data=df, x='np', y='duration', hue='method', ax=ax2)
ax2.set_xlabel('Number of Processes (np)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Duration (seconds)', fontsize=12, fontweight='bold')
ax2.set_title('Bar Plot: Running Time Comparison', fontsize=13, fontweight='bold')
ax2.legend(title='Method')

# Plot 3: Speedup calculation
ax3 = axes[1, 0]
# Hitung speedup relatif terhadap single process
single_mpi = df[(df['method'] == 'MPI_Reduce') & (df['np'] == 1)]['duration'].values[0]
single_send = df[(df['method'] == 'Send-Receive') & (df['np'] == 1)]['duration'].values[0]

df['speedup'] = df.apply(lambda row: single_mpi/row['duration'] if row['method'] == 'MPI_Reduce' 
                        else single_send/row['duration'], axis=1)

for method in df['method'].unique():
    method_data = df[df['method'] == method]
    ax3.plot(method_data['np'], method_data['speedup'], 
             marker='s', linewidth=2, markersize=8, label=method)

ax3.axhline(y=1, color='r', linestyle='--', alpha=0.7, label='Baseline (np=1)')
ax3.set_xlabel('Number of Processes (np)', fontsize=12, fontweight='bold')
ax3.set_ylabel('Speedup', fontsize=12, fontweight='bold')
ax3.set_title('Speedup Relative to Single Process', fontsize=13, fontweight='bold')
ax3.legend()
ax3.grid(True, alpha=0.3)
ax3.set_xticks(range(1, 7))

# Plot 4: Efficiency calculation
ax4 = axes[1, 1]
df['efficiency'] = df['speedup'] / df['np']

for method in df['method'].unique():
    method_data = df[df['method'] == method]
    ax4.plot(method_data['np'], method_data['efficiency'], 
             marker='^', linewidth=2, markersize=8, label=method)

ax4.set_xlabel('Number of Processes (np)', fontsize=12, fontweight='bold')
ax4.set_ylabel('Efficiency', fontsize=12, fontweight='bold')
ax4.set_title('Parallel Efficiency', fontsize=13, fontweight='bold')
ax4.legend()
ax4.grid(True, alpha=0.3)
ax4.set_xticks(range(1, 7))

plt.tight_layout()
plt.savefig('mpi_vector_performance.png', dpi=300, bbox_inches='tight')
plt.show()

# Buat plot terpisah untuk analisis lebih detail
plt.figure(figsize=(12, 8))

# Plot perbandingan detail
for method in df['method'].unique():
    method_data = df[df['method'] == method]
    plt.plot(method_data['np'], method_data['duration'], 
             marker='o', linewidth=3, markersize=10, label=method, linestyle='-')

plt.xlabel('Number of Processes (np)', fontsize=14, fontweight='bold')
plt.ylabel('Duration (seconds)', fontsize=14, fontweight='bold')
plt.title('MPI Performance Comparison: Reduce vs Send-Receive (Vector Data)', 
          fontsize=16, fontweight='bold')
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.xticks(range(1, 7))

# Tambahkan annotasi nilai
for i, row in df.iterrows():
    plt.annotate(f"{row['duration']:.4f}s", 
                (row['np'], row['duration']), 
                textcoords="offset points", 
                xytext=(0,10), 
                ha='center', 
                fontsize=9,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7))

plt.tight_layout()
plt.savefig('mpi_vector_detailed.png', dpi=300, bbox_inches='tight')
plt.show()

# Tampilkan statistik deskriptif
print("\n" + "="*50)
print("STATISTIK DESKRIPTIF")
print("="*50)
print("\nDuration per Method:")
stats = df.groupby('method')['duration'].describe()
print(stats)

print("\nSpeedup per Method:")
speedup_stats = df.groupby('method')['speedup'].describe()
print(speedup_stats)

print("\nEfficiency per Method:")
efficiency_stats = df.groupby('method')['efficiency'].describe()
print(efficiency_stats)

# Simpan data lengkap dengan speedup dan efficiency
df.to_csv('hasil_mpi_vector_analysis.csv', index=False)
print("\nData analisis lengkap disimpan di 'hasil_mpi_vector_analysis.csv'")

# Analisis performa terbaik
best_mpi = df[df['method'] == 'MPI_Reduce'].loc[df[df['method'] == 'MPI_Reduce']['duration'].idxmin()]
best_send = df[df['method'] == 'Send-Receive'].loc[df[df['method'] == 'Send-Receive']['duration'].idxmin()]

print("\n" + "="*50)
print("PERFORMA TERBAIK")
print("="*50)
print(f"MPI_Reduce tercepat: np={best_mpi['np']}, duration={best_mpi['duration']:.6f}s")
print(f"Send-Receive tercepat: np={best_send['np']}, duration={best_send['duration']:.6f}s")

# Hitung improvement
if best_mpi['duration'] < best_send['duration']:
    improvement = ((best_send['duration'] - best_mpi['duration']) / best_send['duration']) * 100
    print(f"MPI_Reduce {improvement:.2f}% lebih cepat dari Send-Receive")
else:
    improvement = ((best_mpi['duration'] - best_send['duration']) / best_mpi['duration']) * 100
    print(f"Send-Receive {improvement:.2f}% lebih cepat dari MPI_Reduce")
