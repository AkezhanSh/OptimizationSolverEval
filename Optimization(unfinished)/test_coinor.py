from ortools.linear_solver import pywraplp
import time

def test_solver():
    start_time = time.time()
    solver = pywraplp.Solver.CreateSolver("SAT")
    if not solver:
        print("No solver available (SAT solver failed).")
        return
    print("CP-SAT solver initialized successfully.")
    runtime = time.time() - start_time
    print(f"Runtime: {runtime:.3f} seconds")

if __name__ == "__main__":
    test_solver()