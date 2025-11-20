@echo off
setlocal enabledelayedexpansion

set "output_file=results.csv"
set "program=program.exe"

:: Create CSV file with header (without trailing spaces)
echo threads,size,parallel_time,serial_time,speedup > "%output_file%"

:: Define threads and sizes
set "threads=1 2 4 8"
set "sizes=100000 1000000 10000000 100000000 1000000000"

echo Running benchmarks...
echo =====================

:: Loop through all combinations of threads and sizes
for %%t in (%threads%) do (
    for %%s in (%sizes%) do (
        echo Running: %program% %%t %%s
        :: Run program and append output directly to CSV
        %program% %%t %%s >> "%output_file%" 2>nul
    )
)

echo.
echo Benchmark completed! Results saved to: %output_file%
echo.

:: Display the results
type "%output_file%"

endlocal