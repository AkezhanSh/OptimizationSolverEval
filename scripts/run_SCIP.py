from pyscipopt import Model
from datetime import datetime
import os

# Get the directory of the current script
base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__),), '..')
# Define relative paths
problem_file = os.path.join(base_dir, "problem_instances", "dano3_5.mps")
problem_name = os.path.basename(problem_file).replace(".mps", "")
results_dir = os.path.join(base_dir, "results")
log_file = os.path.join(results_dir, f"{problem_name}_SCIP.log")

# Check if problem file exists
if not os.path.exists(problem_file):
    print(f"Error: Problem file not found at {problem_file}")
    print("Please ensure the 'problem_instances' folder exists in the script's directory and contains 'dano3_5.mps'.")
    exit(1)

# Create results directory if it doesn't exist
os.makedirs(results_dir, exist_ok=True)

# Create and solve the model
model = Model()
model.readProblem(problem_file)
model.optimize()

with open(log_file, "a") as log:
    log.write(f"Solution Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    log.write("=" * 50 + '\n')
    
    status = model.getStatus()
    log.write(f"Problem status: {status}\n")
    
    if status in ["optimal", "bestsol"]:
        obj_value = model.getObjVal()
        log.write(f"Objective value: {obj_value}\n")
        
        log.write("\nVariable Values:\n")
        for var in model.getVars():
            if abs(model.getVal(var)) > 1e-10:  # only print non-zero values to keep log file clean
                print(f"{var.name}: {model.getVal(var)}")
                log.write(f"{var.name}: {model.getVal(var)}\n")
    log.write("\nSolver Statistics:\n")
    log.write(f"Solving Time: {model.getSolvingTime()} seconds\n")
    log.write(f"Number of LP Iterations: {model.getNLPIterations}\n")
    log.write(f"Number of Nodes: {model.getNNodes()}\n")
    log.write("=" * 50 + '\n')
print(f"Solution saved to {log_file}")