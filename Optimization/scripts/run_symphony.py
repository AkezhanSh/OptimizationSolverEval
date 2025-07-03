import subprocess
import re
import time
import os

def solve_mip(mps_file):
    start_time = time.time()
    testcase_name = os.path.splitext(os.path.basename(mps_file))[0]
    solver_name = "symphony"
    log_file = f"/Users/akezhansh/Documents/Rivermap/Optimization/results/{testcase_name}_{solver_name}.log"

    # Initialize log content
    log_content = [f"Testcase: {testcase_name}", f"Solver: {solver_name}"]

    if not os.path.exists(mps_file):
        log_content.append(f"File {mps_file} not found.")
        with open(log_file, 'w') as f:
            f.write("\n".join(log_content))
        print(f"File {mps_file} not found.")
        return

    result = subprocess.run(["symphony", "-F", mps_file], capture_output=True, text=True)
    runtime = time.time() - start_time
    output = result.stdout
    obj_match = re.search(r"Objective value:\s*([\d\.-]+)", output)

    if obj_match:
        log_content.append(f"Objective value: {obj_match.group(1)}")
        print(f"Objective value: {obj_match.group(1)}")
        
    if "optimal" in output.lower():
        log_content.append("Solution status: Optimal")
        print("Solution status: Optimal")
    elif "infeasible" in output.lower():
        log_content.append("Problem is infeasible.")
        print("Problem is infeasible.")
    else:
        log_content.append("Solution status: Non-optimal")
        print("Solution status: Non-optimal")
        
        
        
        # Parse non-zero variable values
    var_matches = re.findall(r"(\w+)\s+([+-]?\d*\.?\d+)", output)
    if var_matches:
        log_content.append("Non-zero variable values:")
        print("Non-zero variable values:")
        for var_name, var_value in var_matches:
            if float(var_value) != 0:
                log_content.append(f"Variable {var_name} = {var_value}")
                print(f"Variable {var_name} = {var_value}")

    # Parse problem statistics (if available)
    stats_match = re.search(r"Problem has\s+(\d+)\s+variables\s+and\s+(\d+)\s+constraints", output)
    if stats_match:
        log_content.append(f"Problem statistics: {stats_match.group(1)} variables, {stats_match.group(2)} constraints")
        print(f"Problem statistics: {stats_match.group(1)} variables, {stats_match.group(2)} constraints")
        
        
    log_content.append(f"Runtime: {runtime:.3f} seconds")
    print(f"Runtime: {runtime:.3f} seconds")

    # Write to log file
    with open(log_file, 'w') as f:
        f.write("\n".join(log_content))

if __name__ == "__main__":
    mps_file = "/Users/akezhansh/Documents/Rivermap/Optimization/problem_instances/dano3_5.mps"
    solve_mip(mps_file)