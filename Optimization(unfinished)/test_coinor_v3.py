import sys
import pulp
from pulp import LpProblem, LpStatus

def solve_mps_with_ortools(mps_file):
    print(f"Loading MPS file: {mps_file}")

    # Load model from MPS
    prob = LpProblem.fromMPS(mps_file, sense=pulp.LpMinimize)

    # Set OR-Tools as solver backend
    solver = pulp.getSolver('PULP_CBC_CMD', msg=True)  # ORTools not exposed directly in PuLP yet

    # Solve the problem
    prob.solve(solver)

    # Print results
    print(f"Status: {LpStatus[prob.status]}")
    print(f"Objective value: {pulp.value(prob.objective)}")

    for v in prob.variables():
        print(f"{v.name} = {v.varValue}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python solve_mps_with_ortools.py path/to/problem.mps")
        sys.exit(1)

    mps_file = sys.argv[1]
    solve_mps_with_ortools(mps_file)
