import tracemalloc
import sys

sys.setrecursionlimit(10000)
print(sys.getrecursionlimit())


def recursive_function(n):
    if n == 0:
        return 0
    else:
        return n + recursive_function(n-1)
print("=" * 40)
print(f"{'Run #':<8} {'N':<12} {'Peak Mem (MB)':<12}")
print("=" * 40)
# Start tracking memory allocations
n = [100,500,1000,2000,3000,4000,5000,6000,7000,8000,9000]
i=0
for k in n:
  i += 1
  tracemalloc.start()
  recursive_function(k)
  current, peak = tracemalloc.get_traced_memory()
  print(f"{i:<8} {k:<12} {peak / 10**6:<12.2f}")
  tracemalloc.stop()
print("=" * 40)