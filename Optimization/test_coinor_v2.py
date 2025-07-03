from ortools.linear_solver import pywraplp
import os
import time

def solve_mip(mps_file):
    start_time = time.time()
    testcase_name = os.path.splitext(os.path.basename(mps_file))[0]
    solver_name = "OR-Tools-CBC"
    results_dir = "/Users/akezhansh/Documents/Rivermap/Optimization/results"
    log_file = f"{results_dir}/{testcase_name}_{solver_name}.log"

    # Create results directory if it doesn't exist
    os.makedirs(results_dir, exist_ok=True)

    # Initialize log content
    log_content = [f"Testcase: {testcase_name}", f"Solver: {solver_name}"]

    if not os.path.exists(mps_file):
        log_content.append(f"File {mps_file} not found.")
        with open(log_file, 'w') as f:
            f.write("\n".join(log_content))
        print(f"File {mps_file} not found.")
        return

    # Create CBC solver
    solver = pywraplp.Solver.CreateSolver("CBC")
    if not solver:
        log_content.append("No solver available (CBC solver failed).")
        with open(log_file, 'w') as f:
            f.write("\n".join(log_content))
        print("No solver available (CBC solver failed).")
        return

    # Read MPS file directly
    if not solver.ReadMps(mps_file, True):
        log_content.append(f"Failed to read MPS file: {mps_file}")
        with open(log_file, 'w') as f:
            f.write("\n".join(log_content))
        print(f"Failed to read MPS file: {mps_file}")
        return

    # Solve
    result_status = solver.Solve()
    runtime = time.time() - start_time

    # Process results
    if result_status == pywraplp.Solver.OPTIMAL:
        log_content.append("Solution status: Optimal")
        log_content.append(f"Objective value: {solver.Objective().Value()}")
        log_content.append(f"Runtime: {runtime:.3f} seconds")
        print("Solution status: Optimal")
        print(f"Objective value: {solver.Objective().Value()}")
        print(f"Runtime: {runtime:.3f} seconds")
        for var in solver.variables():
            if var.integrality():
                val = var.solution_value()
                if not float(val).is_integer():
                    warning = f"Warning: Variable {var.name()} = {val} is not integer!"
                    log_content.append(warning)
                    print(warning)
                else:
                    log_content.append(f"Variable {var.name()} = {val}")
                    print(f"Variable {var.name()} = {val}")
    elif result_status == pywraplp.Solver.INFEASIBLE:
        log_content.append("Problem is infeasible.")
        log_content.append(f"Runtime: {runtime:.3f} seconds")
        print("Problem is infeasible.")
        print(f"Runtime: {runtime:.3f} seconds")
    else:
        log_content.append(f"Solution status: {result_status}")
        log_content.append(f"Runtime: {runtime:.3f} seconds")
        print(f"Solution status: {result_status}")
        print(f"Runtime: {runtime:.3f} seconds")

    # Write to log file
    with open(log_file, 'w') as f:
        f.write("\n".join(log_content))

if __name__ == "__main__":
    mps_file = "/Users/akezhansh/Documents/Rivermap/Optimization/problem_instances/stein15inf.mps"
    solve_mip(mps_file)