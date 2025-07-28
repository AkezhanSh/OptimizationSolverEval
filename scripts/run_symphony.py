import subprocess
import re
import os
import sys
import time
from datetime import datetime


mps_file_name = "icap6000.mps"
problem_type  = "MIQP"


# Base dir = one level up from this script
base_dir     = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
problem_file = os.path.join(base_dir, problem_type, mps_file_name)
problem_name = os.path.splitext(os.path.basename(problem_file))[0]
results_dir = os.path.join(os.getcwd(), "results", problem_type)

log_file     = os.path.join(results_dir, f"{problem_name}_{problem_type}_SYMPHONY.log")


if not os.path.exists(problem_file):
    print(f"Error: {problem_file} not found.")
    sys.exit(1)
os.makedirs(results_dir, exist_ok=True)


start = time.time()
try:
    proc = subprocess.run(
        ["symphony", "-F", problem_file],
        capture_output=True, text=True, check=True
    )
    out, err = proc.stdout, proc.stderr
    with open(log_file, "w") as f:
        f.write("=== STDOUT ===\n" + out + "\n=== STDERR ===\n" + err)
except subprocess.CalledProcessError as e:
    with open(log_file, "a") as f:
        f.write(f"Error running Symphony: {e.stderr}\n")
    print("Symphony error:", e.stderr)
    sys.exit(1)
runtime = time.time() - start

print(f"\nResults saved to: {log_file}")
