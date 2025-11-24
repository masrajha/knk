import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Style settings
plt.style.use('default')
plt.rcParams['figure.figsize'] = [15, 10]
plt.rcParams['font.size'] = 10

def format_size_label(size):
    """Memformat label ukuran menjadi format eksponen yang benar"""
    # Konversi ke notasi eksponen dan ambil bagian eksponennya
    if size == 10000:
        return '1e+4'
    elif size == 100000:
        return '1e+5'
    elif size == 1000000:
        return '1e+6'
    elif size == 10000000:
        return '1e+7'
    elif size == 100000000:
        return '1e+8'
    elif size == 1000000000:
        return '1e+9'
    else:
        # Fallback untuk ukuran lain
        exp = int(np.log10(size))
        return f'1e+{exp}'

def format_config_label(threads, size):
    """Memformat label konfigurasi menjadi format Threads_Size"""
    return f'{int(threads)}_{format_size_label(size)}'

def read_and_process_data(filename):
    """Membaca dan memproses data dari CSV dengan struktur baru"""
    if not os.path.exists(filename):
        print(f"Error: File {filename} tidak ditemukan!")
        return None
    
    df = pd.read_csv(filename)
    
    # Clean column names (remove trailing/leading spaces)
    df.columns = df.columns.str.strip()
    
    print(f"Kolom yang ditemukan: {list(df.columns)}")
    
    # Transform data dari wide format ke long format
    # Kolom: size, nt1_time, nt2_time, nt4_time, nt8_time, serial_time
    # Menjadi: size, threads, parallel_time, serial_time
    
    melted_data = []
    
    # Iterasi melalui setiap baris data
    for _, row in df.iterrows():
        size = row['size']
        serial_time = row['serial_time']
        
        # Untuk setiap konfigurasi thread
        for thread_col in [ 'nt2_time', 'nt4_time','nt5_time', 'nt8_time','nt10_time']:
            if thread_col in row:
                # Ekstrak jumlah thread dari nama kolom
                threads = int(thread_col.replace('nt', '').replace('_time', ''))
                parallel_time = row[thread_col]
                
                # Tambahkan ke dataset baru
                melted_data.append({
                    'size': size,
                    'threads': threads,
                    'parallel_time': parallel_time,
                    'serial_time': serial_time
                })
    
    # Buat DataFrame baru
    df_long = pd.DataFrame(melted_data)
    
    # Hitung speedup
    print("Menghitung speedup...")
    df_long['speedup'] = df_long.apply(lambda row: row['serial_time'] / row['parallel_time'] 
                            if row['parallel_time'] > 0 and row['serial_time'] > 0 else 0, axis=1)
    
    # Handle kasus dimana serial_time = 0
    df_long['speedup'] = df_long.apply(lambda row: 0 if row['serial_time'] == 0 else row['speedup'], axis=1)
    
    # Replace infinite values dengan 0
    df_long['speedup'] = df_long['speedup'].replace([np.inf, -np.inf], 0)
    
    print(f"Data berhasil diubah format: {len(df_long)} baris")
    print(f"Kolom baru: {list(df_long.columns)}")
    print("\n5 baris pertama data setelah transformasi:")
    print(df_long.head())
    
    return df_long

def create_comprehensive_plots(df):
    """Membuat visualisasi komprehensif dari data benchmark"""
    
    # Filter out invalid data (speedup = 0 atau NaN)
    plot_df = df[(df['speedup'] > 0) & (~pd.isna(df['speedup']))].copy()
    
    if len(plot_df) == 0:
        print("Tidak ada data valid untuk diplot!")
        return None
    
    # Urutkan data berdasarkan size dan threads untuk konsistensi
    plot_df = plot_df.sort_values(['size', 'threads']).reset_index(drop=True)
    
    # Create figure dengan multiple subplots
    fig = plt.figure(figsize=(20, 16))
    
    # ===== PLOT 1: Execution Time Comparison =====
    ax1 = plt.subplot(2, 3, 1)
    
    # Prepare data untuk grouped bar chart
    threads = sorted(plot_df['threads'].unique())
    sizes = sorted(plot_df['size'].unique())
    x = np.arange(len(sizes))
    width = 0.15  # Diperkecil karena ada lebih banyak thread
    
    # Plot parallel time untuk setiap thread count
    for i, thread in enumerate(threads):
        thread_data = plot_df[plot_df['threads'] == thread]
        parallel_times = []
        for size in sizes:
            size_data = thread_data[thread_data['size'] == size]
            if len(size_data) > 0:
                parallel_times.append(size_data['parallel_time'].values[0])
            else:
                parallel_times.append(0)
        
        ax1.bar(x + i*width, parallel_times, width, label=f'{thread} threads', 
               alpha=0.8)
    
    # Plot serial time
    serial_times = []
    for size in sizes:
        size_data = plot_df[plot_df['size'] == size]
        if len(size_data) > 0:
            # Ambil serial_time dari baris pertama (sama untuk semua thread dengan size yang sama)
            serial_times.append(size_data['serial_time'].values[0])
        else:
            serial_times.append(0)
    
    ax1.bar(x + len(threads)*width, serial_times, width, label='Serial', alpha=0.8, color='red')
    
    ax1.set_xlabel('Problem Size')
    ax1.set_ylabel('Time (seconds)')
    ax1.set_title('Execution Time Comparison')
    ax1.set_xticks(x + width * len(threads) / 2)
    ax1.set_xticklabels([format_size_label(size) for size in sizes], rotation=45)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')
    
    # ===== PLOT 2: Speedup by Configuration =====
    ax2 = plt.subplot(2, 3, 2)
    
    # Plot speedup untuk setiap konfigurasi
    for i, thread in enumerate(threads):
        if thread == 1:  # Skip thread 1 untuk speedup
            continue
        thread_data = plot_df[plot_df['threads'] == thread]
        speedups = []
        sizes_thread = []
        for size in sizes:
            size_data = thread_data[thread_data['size'] == size]
            if len(size_data) > 0:
                speedups.append(size_data['speedup'].values[0])
                sizes_thread.append(size)
        
        if speedups:
            ax2.plot([format_size_label(size) for size in sizes_thread], speedups, 
                    'o-', linewidth=2, markersize=8, label=f'{thread} threads')
    
    ax2.axhline(y=1, color='red', linestyle='--', alpha=0.7, label='Baseline (Serial)')
    ax2.set_xlabel('Problem Size')
    ax2.set_ylabel('Speedup')
    ax2.set_title('Speedup vs Problem Size')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.tick_params(axis='x', rotation=45)
    
    # ===== PLOT 3: Speedup Bar Chart =====
    ax3 = plt.subplot(2, 3, 3)
    
    # Buat bar chart untuk speedup
    x_pos = np.arange(len(plot_df))
    colors = plt.cm.viridis(np.linspace(0, 1, len(threads)))
    
    for i, thread in enumerate(threads):
        if thread == 1:
            continue
        thread_mask = plot_df['threads'] == thread
        thread_indices = x_pos[thread_mask]
        thread_speedups = plot_df[thread_mask]['speedup']
        if len(thread_speedups) > 0:
            ax3.bar(thread_indices, thread_speedups, color=colors[i], 
                   label=f'{thread} threads', alpha=0.8)
    
    ax3.axhline(y=1, color='red', linestyle='--', alpha=0.7, label='Baseline')
    ax3.set_xlabel('Configuration')
    ax3.set_ylabel('Speedup')
    ax3.set_title('Speedup by Configuration')
    ax3.set_xticks(x_pos)
    
    # Format label untuk Plot 3: Threads_Size
    config_labels = [format_config_label(row.threads, row.size) for _, row in plot_df.iterrows()]
    ax3.set_xticklabels(config_labels, rotation=45, ha='right')
    
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # ===== PLOT 4: Efficiency Plot =====
    ax4 = plt.subplot(2, 3, 4)
    
    # Hitung efficiency (speedup / threads)
    efficiencies_data = []  # Untuk menyimpan semua nilai efficiency
    for thread in threads:
        if thread > 1:  # Efficiency hanya meaningful untuk multi-threading
            thread_data = plot_df[plot_df['threads'] == thread]
            efficiencies = []
            sizes_eff = []
            for size in sizes:
                size_data = thread_data[thread_data['size'] == size]
                if len(size_data) > 0:
                    efficiency = size_data['speedup'].values[0] / thread
                    efficiencies.append(efficiency)
                    sizes_eff.append(size)
                    efficiencies_data.append(efficiency)
            
            if efficiencies:
                ax4.plot([format_size_label(size) for size in sizes_eff], efficiencies, 's-', linewidth=2, markersize=8, 
                        label=f'{thread} threads')
    
    ax4.axhline(y=1, color='green', linestyle='--', alpha=0.7, label='Perfect Efficiency')
    ax4.set_xlabel('Problem Size')
    ax4.set_ylabel('Efficiency')
    ax4.set_title('Efficiency (Speedup / Threads)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.tick_params(axis='x', rotation=45)
    if efficiencies_data:  # Only set ylim if there's data
        ax4.set_ylim(0, max(1.1, max(efficiencies_data) * 1.1))
    
    # ===== PLOT 5: Parallel Time Heatmap =====
    ax5 = plt.subplot(2, 3, 5)
    
    # Buat pivot table untuk heatmap
    pivot_parallel = plot_df.pivot(index='size', columns='threads', values='parallel_time')
    if not pivot_parallel.empty:
        im = ax5.imshow(pivot_parallel.values, cmap='YlOrRd', aspect='auto')
        
        # Set labels
        ax5.set_xticks(np.arange(len(threads)))
        ax5.set_xticklabels(threads)
        ax5.set_yticks(np.arange(len(sizes)))
        ax5.set_yticklabels([format_size_label(size) for size in sizes])
        ax5.set_xlabel('Threads')
        ax5.set_ylabel('Problem Size')
        ax5.set_title('Parallel Time Heatmap (seconds)')
        
        # Add colorbar
        plt.colorbar(im, ax=ax5)
        
        # Add text annotations
        for i in range(len(sizes)):
            for j in range(len(threads)):
                if i < pivot_parallel.shape[0] and j < pivot_parallel.shape[1]:
                    text = ax5.text(j, i, f'{pivot_parallel.values[i, j]:.3f}',
                                   ha="center", va="center", color="black", fontsize=8)
    
    # ===== PLOT 6: Speedup vs Ideal Scaling =====
    ax6 = plt.subplot(2, 3, 6)
    
    for thread in threads:
        if thread > 1:
            thread_data = plot_df[plot_df['threads'] == thread]
            actual_speedup = []
            sizes_ideal = []
            for size in sizes:
                size_data = thread_data[thread_data['size'] == size]
                if len(size_data) > 0:
                    actual_speedup.append(size_data['speedup'].values[0])
                    sizes_ideal.append(size)
            
            if actual_speedup:
                ax6.plot([format_size_label(size) for size in sizes_ideal], actual_speedup, 
                        'o-', label=f'Actual {thread} threads')
                ax6.axhline(y=thread, color='gray', linestyle='--', 
                           alpha=0.5, label=f'Ideal {thread} threads')
    
    ax6.set_xlabel('Problem Size')
    ax6.set_ylabel('Speedup')
    ax6.set_title('Actual vs Ideal Speedup')
    ax6.legend()
    ax6.grid(True, alpha=0.3)
    ax6.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    return fig

def create_simple_bar_charts(df):
    """Membuat grafik batang sederhana"""
    # Filter out invalid data
    plot_df = df[(df['speedup'] > 0) & (~pd.isna(df['speedup']))].copy()
    
    if len(plot_df) == 0:
        print("Tidak ada data valid untuk simple bar charts!")
        return None
    
    # Urutkan data berdasarkan size dan threads untuk konsistensi
    plot_df = plot_df.sort_values(['size', 'threads']).reset_index(drop=True)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Data preparation
    threads = plot_df['threads'].unique()
    
    # Plot 1: Time comparison bars
    x_pos = np.arange(len(plot_df))
    width = 0.35
    
    parallel_bars = ax1.bar(x_pos - width/2, plot_df['parallel_time'], width, 
                           label='Parallel Time', alpha=0.8, color='blue')
    serial_bars = ax1.bar(x_pos + width/2, plot_df['serial_time'], width, 
                         label='Serial Time', alpha=0.8, color='red')
    
    ax1.set_xlabel('Configuration (Threads_Size)')
    ax1.set_ylabel('Time (seconds)')
    ax1.set_title('Parallel vs Serial Execution Time')
    ax1.set_xticks(x_pos)
    
    # Format label untuk sumbu x
    config_labels = [format_config_label(row.threads, row.size) for _, row in plot_df.iterrows()]
    ax1.set_xticklabels(config_labels, rotation=45, ha='right')
    
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')
    
    # Plot 2: Speedup bars
    colors = ['green' if x >= 1 else 'orange' for x in plot_df['speedup']]
    speedup_bars = ax2.bar(x_pos, plot_df['speedup'], color=colors, alpha=0.8)
    
    ax2.axhline(y=1, color='red', linestyle='--', linewidth=1, label='Baseline')
    ax2.set_xlabel('Configuration (Threads_Size)')
    ax2.set_ylabel('Speedup')
    ax2.set_title('Speedup Achieved')
    ax2.set_xticks(x_pos)
    
    # Format label untuk sumbu x
    ax2.set_xticklabels(config_labels, rotation=45, ha='right')
    
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bar in speedup_bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}', ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    return fig

def create_thread_comparison_plots(df):
    """Membuat plot perbandingan berdasarkan thread count"""
    # Filter out invalid data
    plot_df = df[(df['speedup'] > 0) & (~pd.isna(df['speedup']))].copy()
    
    if len(plot_df) == 0:
        print("Tidak ada data valid untuk thread comparison plots!")
        return None
    
    # Urutkan data berdasarkan size dan threads untuk konsistensi
    plot_df = plot_df.sort_values(['size', 'threads']).reset_index(drop=True)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    threads = sorted(plot_df['threads'].unique())
    sizes = sorted(plot_df['size'].unique())
    
    # Plot 1: Parallel time by thread count
    for thread in threads:
        thread_data = plot_df[plot_df['threads'] == thread]
        parallel_times = []
        valid_sizes = []
        for size in sizes:
            size_data = thread_data[thread_data['size'] == size]
            if len(size_data) > 0:
                parallel_times.append(size_data['parallel_time'].values[0])
                valid_sizes.append(size)
        
        if parallel_times:
            ax1.plot([format_size_label(size) for size in valid_sizes], 
                    parallel_times, 'o-', linewidth=2, 
                    markersize=8, label=f'{thread} threads')
    
    ax1.set_xlabel('Problem Size')
    ax1.set_ylabel('Parallel Time (seconds)')
    ax1.set_title('Parallel Execution Time by Thread Count')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)
    ax1.set_yscale('log')
    
    # Plot 2: Speedup by thread count
    for thread in threads:
        if thread > 1:  # Speedup hanya meaningful untuk multi-threading
            thread_data = plot_df[plot_df['threads'] == thread]
            speedups = []
            valid_sizes = []
            for size in sizes:
                size_data = thread_data[thread_data['size'] == size]
                if len(size_data) > 0:
                    speedups.append(size_data['speedup'].values[0])
                    valid_sizes.append(size)
            
            if speedups:
                ax2.plot([format_size_label(size) for size in valid_sizes], 
                        speedups, 's-', linewidth=2, 
                        markersize=8, label=f'{thread} threads')
    
    # Add ideal scaling lines
    for thread in threads:
        if thread > 1:
            ax2.axhline(y=thread, color='gray', linestyle='--', alpha=0.5)
    
    ax2.axhline(y=1, color='red', linestyle='--', alpha=0.7, label='Baseline')
    ax2.set_xlabel('Problem Size')
    ax2.set_ylabel('Speedup')
    ax2.set_title('Speedup by Thread Count')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    return fig

def save_cleaned_data(df, filename='cleaned_results.csv'):
    """Menyimpan data yang sudah dibersihkan dan dihitung ulang"""
    df.to_csv(filename, index=False)
    print(f"✓ Data bersih disimpan: {filename}")

def main():
    """Main function"""
    filename = 'results_2.csv'
    
    # Read data
    df = read_and_process_data(filename)
    if df is None:
        return
    
    # Simpan data yang sudah dibersihkan
    save_cleaned_data(df)
    
    print(f"\nStatistik Data:")
    print(df.describe())
    
    # Create visualizations
    print("\nMembuat visualisasi data...")
    
    try:
        # 1. Comprehensive plots
        fig1 = create_comprehensive_plots(df)
        if fig1 is not None:
            fig1.savefig('comprehensive_analysis.png', dpi=300, bbox_inches='tight')
            print("✓ Comprehensive analysis plot disimpan: comprehensive_analysis.png")
        else:
            print("✗ Gagal membuat comprehensive analysis plot")
        
        # 2. Simple bar charts
        fig2 = create_simple_bar_charts(df)
        if fig2 is not None:
            fig2.savefig('simple_bar_charts.png', dpi=300, bbox_inches='tight')
            print("✓ Simple bar charts disimpan: simple_bar_charts.png")
        else:
            print("✗ Gagal membuat simple bar charts")
        
        # 3. Thread comparison plots
        fig3 = create_thread_comparison_plots(df)
        if fig3 is not None:
            fig3.savefig('thread_comparison.png', dpi=300, bbox_inches='tight')
            print("✓ Thread comparison plot disimpan: thread_comparison.png")
        else:
            print("✗ Gagal membuat thread comparison plot")
        
        # 4. Additional: Performance summary table
        create_performance_table(df)
        
        print(f"\nSemua visualisasi telah berhasil dibuat!")
        plt.show()
        
    except Exception as e:
        print(f"Error dalam membuat plot: {e}")
        import traceback
        traceback.print_exc()

def create_performance_table(df):
    """Membuat tabel summary performa"""
    # Filter data yang valid
    valid_data = df[(df['speedup'] > 0) & (~pd.isna(df['speedup']))]
    
    if len(valid_data) > 0:
        summary = valid_data.groupby('threads').agg({
            'parallel_time': ['mean', 'min', 'max'],
            'speedup': ['mean', 'max']
        }).round(4)
        
        print("\n" + "="*50)
        print("PERFORMANCE SUMMARY (Data Valid)")
        print("="*50)
        print(summary)
        
        # Best configuration
        best_speedup = valid_data.loc[valid_data['speedup'].idxmax()]
        print(f"\nKonfigurasi terbaik (speedup tertinggi):")
        print(f"  Threads: {best_speedup['threads']}")
        print(f"  Size: {format_size_label(best_speedup['size'])}")
        print(f"  Speedup: {best_speedup['speedup']:.2f}x")
        print(f"  Parallel Time: {best_speedup['parallel_time']:.4f}s")
        print(f"  Serial Time: {best_speedup['serial_time']:.4f}s")
    else:
        print("\nTidak ada data speedup yang valid untuk dianalisis")

if __name__ == "__main__":
    main()