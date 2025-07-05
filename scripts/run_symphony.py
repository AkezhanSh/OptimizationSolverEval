import subprocess
import re
import time
import os
from datetime import datetime

def solve_mip(mps_file):
    start_time = time.time()
    testcase_name = os.path.splitext(os.path.basename(mps_file))[0]
    solver_name = "symphony"
    
    # Get the directory of the current script and its parent directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)  # Parent directory of scripts/
    # Define results directory and ensure it exists
    results_dir = os.path.join(base_dir, "results")
    os.makedirs(results_dir, exist_ok=True)
    log_file = os.path.join(results_dir, f"{testcase_name}_{solver_name}.log")

    # Initialize log content
    log_content = [
        f"Solution Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 50,
        f"Testcase: {testcase_name}",
        f"Solver: {solver_name}"
    ]

    # Check if problem file exists
    if not os.path.exists(mps_file):
        log_content.append(f"File {mps_file} not found.")
        with open(log_file, 'w') as f:
            f.write("\n".join(log_content))
        print(f"File {mps_file} not found.")
        return

    # Run Symphony solver
    try:
        result = subprocess.run(
            ["symphony", "-F", mps_file],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        log_content.append(f"Error running Symphony: {e.stderr}")
        with open(log_file, 'w') as f:
            f.write("\n".join(log_content))
        print(f"Error running Symphony: {e.stderr}")
        return

    runtime = time.time() - start_time
    output = result.stdout

    # Parse solution status
    status = "unknown"
    if "optimal" in output.lower():
        status = "optimal"
    elif "infeasible" in output.lower():
        status = "infeasible"
    elif "unbounded" in output.lower():
        status = "unbounded"
    else:
        status = "non-optimal"
    log_content.append(f"Problem status: {status}")
    print(f"Problem status: {status}")

    # Parse objective value
    obj_match = re.search(r"Objective value:\s*([+-]?\d*\.?\d+)", output)
    if obj_match:
        obj_value = obj_match.group(1)
        log_content.append(f"Objective value: {obj_value}")
        print(f"Objective value: {obj_value}")
    else:
        log_content.append("Objective value: Not found")
        print("Objective value: Not found")

    # Parse variable values
    log_content.append("\nVariable Values:")
    print("\nVariable Values:")
    var_matches = re.findall(r"(\w+)\s+([+-]?\d*\.?\d+)", output)
    non_zero_vars = []
    if var_matches:
        for var_name, var_value in var_matches:
            if abs(float(var_value)) > 1e-10:  # Only include non-zero values
                non_zero_vars.append(f"{var_name}: {var_value}")
                print(f"{var_name}: {var_value}")
    if not non_zero_vars:
        log_content.append("No non-zero variable values found.")
        print("No non-zero variable values found.")
    else:
        log_content.extend(non_zero_vars)

    # Parse solver statistics
    log_content.append("\nSolver Statistics:")
    stats = []
    # Runtime
    stats.append(f"Solving Time: {runtime:.3f} seconds")
    print(f"Solving Time: {runtime:.3f} seconds")
    
    # Try to extract iteration or node counts (Symphony-specific)
    iter_match = re.search(r"Iterations:\s*(\d+)", output, re.IGNORECASE)
    if iter_match:
        stats.append(f"Number of Iterations: {iter_match.group(1)}")
        print(f"Number of Iterations: {iter_match.group(1)}")
    
    node_match = re.search(r"Nodes:\s*(\d+)", output, re.IGNORECASE)
    if node_match:
        stats.append(f"Number of Nodes: {node_match.group(1)}")
        print(f"Number of Nodes: {node_match.group(1)}")
    
    # Problem size statistics
    stats_match = re.search(r"Problem has\s+(\d+)\s+variables\s+and\s+(\d+)\s+constraints", output)
    if stats_match:
        stats.append(f"Problem statistics: {stats_match.group(1)} variables, {stats_match.group(2)} constraints")
        print(f"Problem statistics: {stats_match.group(1)} variables, {stats_match.group(2)} constraints")
    
    if not (iter_match or node_match or stats_match):
        stats.append("No additional solver statistics found.")
        print("No additional solver statistics found.")
    
    log_content.extend(stats)
    log_content.append("=" * 50)

    # Write to log file
    with open(log_file, 'w') as f:
        f.write("\n".join(log_content))

if __name__ == "__main__":
    # Get the directory of the current script and its parent directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)  # Parent directory of scripts/
    mps_file = os.path.join(base_dir, "problem_instances", "qap10.mps")
    solve_mip(mps_file)