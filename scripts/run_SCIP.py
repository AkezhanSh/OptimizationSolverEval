from pyscipopt import Model
from datetime import datetime
import os
import sys

# Get base project directory (2 levels up from this script: scripts/ → ..)
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Define problem file location (adjust QPS filename here)
qps_file_name = "25fv47.mps"
problem_type = "LP"
problem_file = os.path.join(base_dir, problem_type, qps_file_name)
problem_name = os.path.splitext(os.path.basename(problem_file))[0]  # e.g., "QAFIRO"
results_dir = os.path.join(base_dir, "results")
log_file = os.path.join(results_dir, f"{problem_name}_{problem_type}_SCIP.log")

# Ensure problem file exists
if not os.path.exists(problem_file):
    print(f"Error: {problem_file} not found.")
    sys.exit(1)

# Create results dir if needed
os.makedirs(results_dir, exist_ok=True)

# Solve the problem
model = Model()
model.readProblem(problem_file, 'mps')
model.optimize()

# Write results
with open(log_file, "a") as log:
    log.write(f"Solution Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    log.write("=" * 50 + '\n')
    
    status = model.getStatus()
    log.write(f"Status: {status}\n")

    if status in ["optimal", "bestsol"]:
        obj = model.getObjVal()
        log.write(f"Objective Value: {obj}\n\nVariable Values:\n")
        for var in model.getVars():
            val = model.getVal(var)
            if abs(val) > 1e-10:
                print(f"{var.name}: {val}")
                log.write(f"{var.name}: {val}\n")
    
    log.write("\nSolver Statistics:\n")
    log.write(f"Time: {model.getSolvingTime():.4f} sec\n")
    log.write(f"Nodes: {model.getNNodes()}\n")
    log.write(f"LP Iterations: {model.getNLPIterations()}\n")
    log.write("=" * 50 + '\n')

print(f"\n Results saved to: {log_file}")
