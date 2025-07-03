from pyscipopt import Model
from datetime import datetime
import os
problem_file = "/Users/akezhansh/Documents/Rivermap/Optimization/problem_instances/dano3_5.mps"
problem_name = os.path.basename(problem_file).replace(".mps", "")
model = Model()
log_file = f"/Users/akezhansh/Documents/Rivermap/Optimization/results/{problem_name}_SCIP.log"
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
            if abs(model.getVal(var)) > 1e-10: # only print non-zero values to keep log file clean
                print(f"{var.name}: {model.getVal(var)}")
                log.write(f"{var.name}: {model.getVal(var)}\n")
    log.write("\nSolver Statistics:\n")
    log.write(f"Solving Time: {model.getSolvingTime()} seconds\n")
    log.write(f"Number of LP Iterations: {model.getNLPIterations}\n")
    log.write(f"Number of Nodes: {model.getNNodes()}\n")
    log.write("=" * 50 + '\n')
print(f"Solution saved to {log_file}")