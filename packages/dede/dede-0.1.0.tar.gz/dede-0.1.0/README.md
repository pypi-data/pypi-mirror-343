# DeDe

DeDe is a general, scalable, and theoretically grounded framework that accelerates resource allocation through **decouple** and **decompose**.

## Hardware requirements
- Linux OS
- a multi-core CPU instance

## Dependencies
- Python 3.8
- Run `pip install -r requirements.txt` to install `cvxpy` and `ray`

## Running DeDe
DeDe borrows the interface from `cvxpy` and inherits most of its methods, e.g. `Variable(.)`, `Minimize(.)`. 

Different from `cvxpy`,

- DeDe requires separate `resource_constraints` and `demand_constraints` when constructing a problem.
- DeDe has additional arguments in the `solve(.)` methods:
  - `enable_dede`: use DeDe if True; use `cvxpy` if False.
  - `num_cpus`: the number of CPU cores; if not specified, DeDe uses all available CPUs.
  - `rho`: the rho parameter in ADMM formulation.
  - `num_iter`: the number of iteration; if not specified, DeDe stops iterations when the improvement in accuracy is below 1%.

A toy example for resource allocation with DeDe is as follows.
```
import dede as dd
N, M = 100, 100

# Create allocation variables.
x = dd.Variable((N, M), nonneg=True)

# Create the constraints.
resource_constraints = [x[i,:].sum() >= i for i in range(N)]
demand_constraints = [x[:,j].sum() <= j for j in range(M)]

# Create an objective.
objective = dd.Minimize(x.sum())

# Construct the problem.
prob = dd.Problem(objective, resource_constraints, demand_constraints)

# Solve the problem with DeDe on a 64-core CPU.
print(prob.solve(num_cpus=64))

# Solve the problem with cvxpy
print(prob.solve(enable_dede=False))
```
