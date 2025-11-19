#!/bin/bash

# Advanced benchmark script
# Usage: ./benchmark.sh

PROGRAM="./program"
OUTPUT_FILE="benchmark_results.csv"
LOG_FILE="benchmark.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fungsi untuk log
log() {
    echo -e "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Check if program exists
if [ ! -f "$PROGRAM" ]; then
    log "${RED}Error: Program $PROGRAM tidak ditemukan!${NC}"
    log "Pastikan program sudah dikompilasi dengan: g++ -std=c++11 -pthread program.cpp -o program"
    exit 1
fi

# Check if program is executable
if [ ! -x "$PROGRAM" ]; then
    log "${YELLOW}Making program executable...${NC}"
    chmod +x "$PROGRAM"
fi

# Thread configurations
threads=(1 2 4)
sizes=(1000 10000 100000 1000000 10000000 100000000 1000000000)

# Size labels for readable output
declare -A size_labels=(
    [1000]="1e3"
    [10000]="1e4" 
    [100000]="1e5"
    [1000000]="1e6"
    [10000000]="1e7"
    [100000000]="1e8"
    [1000000000]="1e9"
)

# Initialize output file
echo "threads,size,parallel_time,serial_time,speedup" > "$OUTPUT_FILE"

log "${GREEN}Starting benchmark...${NC}"
log "Program: $PROGRAM"
log "Threads: ${threads[*]}"
log "Sizes: ${sizes[*]}"
log "Output: $OUTPUT_FILE"

total_runs=$(( ${#threads[@]} * ${#sizes[@]} ))
current_run=0

# Loop melalui semua kombinasi
for thread in "${threads[@]}"; do
    for size in "${sizes[@]}"; do
        current_run=$((current_run + 1))
        size_label="${size_labels[$size]}"
        
        log "${YELLOW}[$current_run/$total_runs] Running: $thread threads, size $size_label${NC}"
        
        # Jalankan program dan tangkap output
        output=$($PROGRAM $thread $size 2>/dev/null)
        
        # Check if program executed successfully
        if [ $? -eq 0 ] && [ ! -z "$output" ]; then
            # Parse output (format: threads,size,parallel_time,serial_time)
            IFS=',' read -r out_threads out_size out_parallel out_serial <<< "$output"
            
            # Calculate speedup
            speedup=$(echo "scale=2; $out_serial / $out_parallel" | bc 2>/dev/null || echo "N/A")
            
            # Write to CSV
            echo "$out_threads,$out_size,$out_parallel,$out_serial,$speedup" >> "$OUTPUT_FILE"
            
            log "${GREEN}✓ Success: $output (speedup: $speedup)${NC}"
        else
            log "${RED}✗ Failed: thread=$thread, size=$size${NC}"
            echo "$thread,$size,ERROR,ERROR,ERROR" >> "$OUTPUT_FILE"
        fi
        
        # Small delay antara runs untuk menghindari overhead system
        sleep 0.1
    done
done

log "${GREEN}Benchmark completed! Results saved to $OUTPUT_FILE${NC}"

# Show summary
echo
log "${GREEN}=== SUMMARY ===${NC}"
log "Total runs: $total_runs"
log "Output file: $OUTPUT_FILE"
log "Log file: $LOG_FILE"

# Display first few lines of results
echo
log "${GREEN}First 10 lines of results:${NC}"
head -n 10 "$OUTPUT_FILE"