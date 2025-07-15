from ortools.linear_solver import pywraplp

def solve_miqp_with_or_tools():
    # Create the solver with the SCIP backend
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Could not create solver")
        return

    # Variables
    x = solver.IntVar(0.0, 10.0, 'x')   # Integer variable
    y = solver.NumVar(0.0, 10.0, 'y')   # Continuous variable

    # Constraints
    solver.Add(x + y <= 8)
    solver.Add(x - y >= 2)

    # Quadratic objective: x^2 + y^2 + 3x + 4y
    objective = solver.Objective()
    objective.SetCoefficient(x, 3)
    objective.SetCoefficient(y, 4)
    solver.Minimize(objective.Value() + x * x + y * y)  # <--- OR-Tools does NOT support this!

    # 🚨 Here's the problem: OR-Tools linear_solver doesn't support x^2 + y^2 directly.
    # For MIQP, you need to use **ORTools CP-SAT** or formulate QPs in **external solvers** like Gurobi

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        print(f'x = {x.solution_value()}')
        print(f'y = {y.solution_value()}')
        print(f'Objective = {solver.Objective().Value()}')
    else:
        print('The problem does not have an optimal solution.')

if __name__ == "__main__":
    solve_miqp_with_or_tools()
