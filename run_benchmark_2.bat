@echo off
setlocal enabledelayedexpansion

set "output_file=results_2.csv"
set "program=program.exe"

:: Create CSV file with header (without trailing spaces)
echo size,nt2_time,nt4_time,nt5_time,nt8_time,nt10_time,serial_time> "%output_file%"

:: Define threads and sizes
:: set "threads=1 2 4 8"
set "sizes=1000000 10000000 100000000 1000000000"

echo Running benchmarks...
echo =====================

:: Loop through all combinations of threads and sizes

    for %%s in (%sizes%) do (
        echo Running: %program% %%s
        :: Run program and append output directly to CSV
        %program% %%s >> "%output_file%" 2>nul
    )


echo.
echo Benchmark completed! Results saved to: %output_file%
echo.

:: Display the results
type "%output_file%"

python.exe .\plot_results2.py  

endlocal