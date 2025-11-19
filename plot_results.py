import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Style settings
plt.style.use('default')
plt.rcParams['figure.figsize'] = [15, 10]
plt.rcParams['font.size'] = 10

def read_and_process_data(filename):
    """Membaca dan memproses data dari CSV"""
    if not os.path.exists(filename):
        print(f"Error: File {filename} tidak ditemukan!")
        return None
    
    df = pd.read_csv(filename)
    print(f"Data berhasil dibaca: {len(df)} baris")
    print(f"Kolom: {list(df.columns)}")
    print("\n5 baris pertama data:")
    print(df.head())
    return df

def create_comprehensive_plots(df):
    """Membuat visualisasi komprehensif dari data benchmark"""
    
    # Create figure dengan multiple subplots
    fig = plt.figure(figsize=(20, 16))
    
    # ===== PLOT 1: Execution Time Comparison =====
    ax1 = plt.subplot(2, 3, 1)
    
    # Prepare data untuk grouped bar chart
    threads = df['threads'].unique()
    sizes = df['size'].unique()
    x = np.arange(len(sizes))
    width = 0.25
    
    # Plot parallel time untuk setiap thread count
    for i, thread in enumerate(threads):
        thread_data = df[df['threads'] == thread]
        parallel_times = [thread_data[thread_data['size'] == size]['parallel_time'].values[0] 
                         for size in sizes]
        ax1.bar(x + i*width, parallel_times, width, label=f'Parallel {thread} threads', 
               alpha=0.8)
    
    # Plot serial time (sama untuk semua thread count pada size yang sama)
    serial_times = [df[df['size'] == size]['serial_time'].values[0] for size in sizes]
    ax1.bar(x + len(threads)*width, serial_times, width, label='Serial', alpha=0.8, color='red')
    
    ax1.set_xlabel('Problem Size')
    ax1.set_ylabel('Time (seconds)')
    ax1.set_title('Execution Time Comparison')
    ax1.set_xticks(x + width * len(threads) / 2)
    ax1.set_xticklabels([f'{size:.0e}' for size in sizes], rotation=45)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')
    
    # ===== PLOT 2: Speedup by Configuration =====
    ax2 = plt.subplot(2, 3, 2)
    
    # Plot speedup untuk setiap konfigurasi
    for i, thread in enumerate(threads):
        thread_data = df[df['threads'] == thread]
        speedups = thread_data['speedup'].values
        sizes_thread = thread_data['size'].values
        ax2.plot([f'{size:.0e}' for size in sizes_thread], speedups, 
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
    x_pos = np.arange(len(df))
    colors = plt.cm.viridis(np.linspace(0, 1, len(threads)))
    
    for i, thread in enumerate(threads):
        thread_mask = df['threads'] == thread
        thread_indices = x_pos[thread_mask]
        thread_speedups = df[thread_mask]['speedup']
        ax3.bar(thread_indices, thread_speedups, color=colors[i], 
               label=f'{thread} threads', alpha=0.8)
    
    ax3.axhline(y=1, color='red', linestyle='--', alpha=0.7, label='Baseline')
    ax3.set_xlabel('Configuration')
    ax3.set_ylabel('Speedup')
    ax3.set_title('Speedup by Configuration')
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels([f'{row.threads}_{row.size:.0e}' for _, row in df.iterrows()], 
                       rotation=45, ha='right')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # ===== PLOT 4: Efficiency Plot =====
    ax4 = plt.subplot(2, 3, 4)
    
    # Hitung efficiency (speedup / threads)
    for thread in threads:
        if thread > 1:  # Efficiency hanya meaningful untuk multi-threading
            thread_data = df[df['threads'] == thread]
            efficiencies = thread_data['speedup'] / thread
            sizes_eff = [f'{size:.0e}' for size in thread_data['size']]
            ax4.plot(sizes_eff, efficiencies, 's-', linewidth=2, markersize=8, 
                    label=f'{thread} threads')
    
    ax4.axhline(y=1, color='green', linestyle='--', alpha=0.7, label='Perfect Efficiency')
    ax4.set_xlabel('Problem Size')
    ax4.set_ylabel('Efficiency')
    ax4.set_title('Efficiency (Speedup / Threads)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.tick_params(axis='x', rotation=45)
    ax4.set_ylim(0, 1.1)
    
    # ===== PLOT 5: Parallel Time Heatmap =====
    ax5 = plt.subplot(2, 3, 5)
    
    # Buat pivot table untuk heatmap
    pivot_parallel = df.pivot(index='size', columns='threads', values='parallel_time')
    im = ax5.imshow(pivot_parallel.values, cmap='YlOrRd', aspect='auto')
    
    # Set labels
    ax5.set_xticks(np.arange(len(threads)))
    ax5.set_xticklabels(threads)
    ax5.set_yticks(np.arange(len(sizes)))
    ax5.set_yticklabels([f'{size:.0e}' for size in sizes])
    ax5.set_xlabel('Threads')
    ax5.set_ylabel('Problem Size')
    ax5.set_title('Parallel Time Heatmap (seconds)')
    
    # Add colorbar
    plt.colorbar(im, ax=ax5)
    
    # Add text annotations
    for i in range(len(sizes)):
        for j in range(len(threads)):
            text = ax5.text(j, i, f'{pivot_parallel.values[i, j]:.3f}',
                           ha="center", va="center", color="black", fontsize=8)
    
    # ===== PLOT 6: Speedup vs Ideal Scaling =====
    ax6 = plt.subplot(2, 3, 6)
    
    for thread in threads:
        if thread > 1:
            thread_data = df[df['threads'] == thread]
            sizes_ideal = thread_data['size'].values
            actual_speedup = thread_data['speedup'].values
            ideal_speedup = thread  # Ideal speedup = number of threads
            
            ax6.plot([f'{size:.0e}' for size in sizes_ideal], actual_speedup, 
                    'o-', label=f'Actual {thread} threads')
            ax6.axhline(y=ideal_speedup, color='gray', linestyle='--', 
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
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Data preparation
    threads = df['threads'].unique()
    sizes = df['size'].unique()
    
    # Plot 1: Time comparison bars
    x_pos = np.arange(len(df))
    width = 0.35
    
    parallel_bars = ax1.bar(x_pos - width/2, df['parallel_time'], width, 
                           label='Parallel Time', alpha=0.8, color='blue')
    serial_bars = ax1.bar(x_pos + width/2, df['serial_time'], width, 
                         label='Serial Time', alpha=0.8, color='red')
    
    ax1.set_xlabel('Configuration (Threads_Size)')
    ax1.set_ylabel('Time (seconds)')
    ax1.set_title('Parallel vs Serial Execution Time')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels([f'{row.threads}_{row.size:.0e}' for _, row in df.iterrows()], 
                       rotation=45, ha='right')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')
    
    # Plot 2: Speedup bars
    colors = ['green' if x >= 1 else 'orange' for x in df['speedup']]
    speedup_bars = ax2.bar(x_pos, df['speedup'], color=colors, alpha=0.8)
    
    ax2.axhline(y=1, color='red', linestyle='--', linewidth=1, label='Baseline')
    ax2.set_xlabel('Configuration (Threads_Size)')
    ax2.set_ylabel('Speedup')
    ax2.set_title('Speedup Achieved')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels([f'{row.threads}_{row.size:.0e}' for _, row in df.iterrows()], 
                       rotation=45, ha='right')
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
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    threads = df['threads'].unique()
    sizes = df['size'].unique()
    
    # Plot 1: Parallel time by thread count
    for thread in threads:
        thread_data = df[df['threads'] == thread]
        ax1.plot([f'{size:.0e}' for size in thread_data['size']], 
                thread_data['parallel_time'], 'o-', linewidth=2, 
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
            thread_data = df[df['threads'] == thread]
            ax2.plot([f'{size:.0e}' for size in thread_data['size']], 
                    thread_data['speedup'], 's-', linewidth=2, 
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

def main():
    """Main function"""
    filename = 'benchmark_results.csv'
    
    # Read data
    df = read_and_process_data(filename)
    if df is None:
        return
    
    # Convert speedup to numeric (handle non-numeric values)
    df['speedup'] = pd.to_numeric(df['speedup'], errors='coerce')
    
    print(f"\nStatistik Data:")
    print(df.describe())
    
    # Create visualizations
    print("\nMembuat visualisasi data...")
    
    # 1. Comprehensive plots
    fig1 = create_comprehensive_plots(df)
    fig1.savefig('comprehensive_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Comprehensive analysis plot disimpan: comprehensive_analysis.png")
    
    # 2. Simple bar charts
    fig2 = create_simple_bar_charts(df)
    fig2.savefig('simple_bar_charts.png', dpi=300, bbox_inches='tight')
    print("✓ Simple bar charts disimpan: simple_bar_charts.png")
    
    # 3. Thread comparison plots
    fig3 = create_thread_comparison_plots(df)
    fig3.savefig('thread_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Thread comparison plot disimpan: thread_comparison.png")
    
    # 4. Additional: Performance summary table
    create_performance_table(df)
    
    print(f"\nSemua visualisasi telah berhasil dibuat!")
    plt.show()

def create_performance_table(df):
    """Membuat tabel summary performa"""
    summary = df.groupby('threads').agg({
        'parallel_time': ['mean', 'min', 'max'],
        'speedup': ['mean', 'max']
    }).round(4)
    
    print("\n" + "="*50)
    print("PERFORMANCE SUMMARY")
    print("="*50)
    print(summary)
    
    # Best configuration
    best_speedup = df.loc[df['speedup'].idxmax()]
    print(f"\nKonfigurasi terbaik (speedup tertinggi):")
    print(f"  Threads: {best_speedup['threads']}")
    print(f"  Size: {best_speedup['size']:.0e}")
    print(f"  Speedup: {best_speedup['speedup']:.2f}x")
    print(f"  Parallel Time: {best_speedup['parallel_time']:.4f}s")
    print(f"  Serial Time: {best_speedup['serial_time']:.4f}s")

if __name__ == "__main__":
    main()