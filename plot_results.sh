#!/usr/bin/gnuplot -persist
#
# Organized bar charts by thread groups - FIXED VERSION
# Usage: gnuplot organized_bars_fixed.gnu

set terminal pngcairo size 1800,1400 enhanced font 'Arial,11'
set output 'organized_bar_charts_fixed.png'
set datafile separator comma

# Define format_size function
format_size(x) = x >= 1e9 ? "1e9" : \
                 x >= 1e8 ? "1e8" : \
                 x >= 1e7 ? "1e7" : \
                 x >= 1e6 ? "1e6" : \
                 x >= 1e5 ? "1e5" : \
                 x >= 1e4 ? "1e4" : "1e3"

# Style settings
set style data histogram
set style histogram clustered gap 2
set style fill solid 0.8
set boxwidth 0.9

# Color palette
set style line 1 lc rgb "#1f77b4"  # blue
set style line 2 lc rgb "#ff7f0e"  # orange  
set style line 3 lc rgb "#2ca02c"  # green
set style line 4 lc rgb "#d62728"  # red
set style line 5 lc rgb "#9467bd"  # purple
set style line 6 lc rgb "#8c564b"  # brown
set style line 7 lc rgb "#e377c2"  # pink

set multiplot layout 3,1

# ===== PLOT 1: Time Comparison for Each Thread Group =====
set title "Execution Time by Thread Count"
set ylabel "Time (seconds)"
set logscale y
set grid y
set key outside right top
set xlabel "Thread Count"
set xtics ("1" 1, "2" 2, "4" 3)

# Create artificial data for plotting by thread groups
set table "temp_thread_data.txt"
plot 'benchmark_results.csv' using 1:3:2 with table
unset table

# Plot for each size category
plot for [i=1:7] 'benchmark_results.csv' using ($2 == 10**(2+i) && $1 == 1 ? $3 : 1/0):(1) with impulses linewidth 10 linecolor i title sprintf("Size %s", format_size(10**(2+i))), \
     for [i=1:7] 'benchmark_results.csv' using ($2 == 10**(2+i) && $1 == 2 ? $3 : 1/0):(2) with impulses linewidth 10 linecolor i notitle, \
     for [i=1:7] 'benchmark_results.csv' using ($2 == 10**(2+i) && $1 == 4 ? $3 : 1/0):(3) with impulses linewidth 10 linecolor i notitle

# ===== PLOT 2: Speedup by Thread Count =====
set title "Speedup by Thread Count and Problem Size"
set ylabel "Speedup"
unset logscale y
set yrange [0:4]
set grid y
set xlabel "Thread Count"

plot for [i=1:7] 'benchmark_results.csv' using ($2 == 10**(2+i) && $1 == 1 ? $5 : 1/0):(1) with impulses linewidth 10 linecolor i title sprintf("Size %s", format_size(10**(2+i))), \
     for [i=1:7] 'benchmark_results.csv' using ($2 == 10**(2+i) && $1 == 2 ? $5 : 1/0):(2) with impulses linewidth 10 linecolor i notitle, \
     for [i=1:7] 'benchmark_results.csv' using ($2 == 10**(2+i) && $1 == 4 ? $5 : 1/0):(3) with impulses linewidth 10 linecolor i notitle, \
     x/1 with lines dashtype 2 lc black title "Linear scaling"

# ===== PLOT 3: Efficiency =====
set title "Efficiency (Speedup / Threads) by Thread Count"
set ylabel "Efficiency"
set yrange [0:1.2]
set xlabel "Thread Count"

plot for [i=1:7] 'benchmark_results.csv' using ($2 == 10**(2+i) && $1 == 2 ? $5/2 : 1/0):(2) with impulses linewidth 10 linecolor i title sprintf("Size %s", format_size(10**(2+i))), \
     for [i=1:7] 'benchmark_results.csv' using ($2 == 10**(2+i) && $1 == 4 ? $5/4 : 1/0):(3) with impulses linewidth 10 linecolor i notitle, \
     1 with lines dashtype 2 lc black title "Perfect efficiency"

unset multiplot

# Cleanup temporary file
system("rm -f temp_thread_data.txt")