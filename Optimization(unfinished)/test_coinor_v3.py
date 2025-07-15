from ortools.math_opt.python import model_builder, solve

def solve_qp():
    model = model_builder.Model()

    x = model.add_continuous_variable(name="x")
    y = model.add_continuous_variable(name="y")

    # Objective: x^2 + y^2 + 3x + 4y
    model.minimize(x * x + y * y + 3 * x + 4 * y)

    # Constraints
    model.add_linear_constraint(x + y <= 5)
    model.add_linear_constraint(x >= 0)
    model.add_linear_constraint(y >= 0)

    result = solve.solve(model, solver_type=solve.SolverType.GUROBI)  # Or try with SCIP

    print("Status:", result.termination.reason)
    print("x =", result.variable_values[x])
    print("y =", result.variable_values[y])

if __name__ == "__main__":
    solve_qp()
