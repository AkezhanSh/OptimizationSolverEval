# MIP Solver Tests

This repository tests [SCIP](https://scipopt.org) and [SYMPHONY](https://github.com/coin-or/SYMPHONY) on mixed integer programming (MIP) problems using public-domain instances from MIPLIB.

## Overview
The goal is to evaluate solver performance on infeasible (`mod008inf`) and feasible (`p0201`, `air03`) MIP instances, validate solutions (e.g., integer constraints, infeasibility), and document results. Benchmarks from Mittelmann (plato.asu.edu) provide context.

## Repository Structure
- **problems/**: MPS files (e.g., `mod008inf.mps`).
- **scripts/**: Solver and validation scripts.
- **results/**: Solver output logs.
- **README.md**: This file.

## Prerequisites
1. **SCIP**: Install from [scipopt.org](https://scipopt.org) (Apache 2.0).
2. **SYMPHONY**: Install from [github.com/coin-or/SYMPHONY](https://github.com/coin-or/SYMPHONY) (EPL).
3. **Python (Optional)**: For `pyscipopt`, install Python 3.9+ and:
   ```bash
   pip install pyscipopt

## To run solvers through terminal: 
1. **SCIP**: 
scip -f problems/mod008inf.mps > results/mod008inf_scip.log
bash scripts/run_scip.sh
2. **SYMPHONY**:
g++ scripts/run_symphony.cpp -o scripts/run_symphony -lSym
./scripts/run_symphony problems/mod008inf.mps > results/mod008inf_symphony.log