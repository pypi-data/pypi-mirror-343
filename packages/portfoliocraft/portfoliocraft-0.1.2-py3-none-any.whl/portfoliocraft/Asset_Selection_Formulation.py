from math import isclose
from typing import Any, Dict, Optional, Tuple, cast
from warnings import warn

from docplex.mp.basic import Expr
from docplex.mp.constants import ComparisonType
from docplex.mp.constr import IndicatorConstraint, LinearConstraint, NotEqualConstraint, QuadraticConstraint #, QuadraticConstraintExpression
    
from docplex.mp.dvar import Var
from docplex.mp.linear import AbstractLinearExpr
from docplex.mp.model import Model
from docplex.mp.quad import QuadExpr
from docplex.mp.vartype import BinaryVarType, ContinuousVarType, IntegerVarType

class OptimizationModel:
    class Sense:
        MINIMIZE = 0
        MAXIMIZE = 1

    class ConstraintSense:
        LE = 0
        GE = 1
        EQ = 2

class OptimizationVariable:
    def __init__(self, name: str, vartype: int, lowerbound: float = 0.0, upperbound: float = None):
        self.name = name
        self.vartype = vartype
        self.lowerbound = lowerbound
        self.upperbound = upperbound

class QuadraticProgram:
    def __init__(self):
        self.variables = []
        self.objective = {
            'linear': {},
            'quadratic': {},
            'constant': 0.0,
            'sense': OptimizationModel.Sense.MINIMIZE
        }
        self.linear_constraints = []
        self.quadratic_constraints = []

def from_docplex_mp(quadratic_program: QuadraticProgram) -> Model:
    mdl = Model(quadratic_program.name)
    var = {}

    # Variable conversion
    for idx, x in enumerate(quadratic_program.variables):
        if x.vartype == ContinuousVarType:
            var[idx] = mdl.continuous_var(lb=x.lowerbound, ub=x.upperbound, name=x.name)
        elif x.vartype == BinaryVarType:
            var[idx] = mdl.binary_var(name=x.name)
        elif x.vartype == IntegerVarType:
            var[idx] = mdl.integer_var(lb=x.lowerbound, ub=x.upperbound, name=x.name)

    # Objective construction
    linear_part = mdl.sum(v * var[i] for i, v in quadratic_program.objective['linear'].items())
    quadratic_part = mdl.sum(v * var[i] * var[j] for (i, j), v in quadratic_program.objective['quadratic'].items())
    objective = quadratic_program.objective['constant'] + linear_part + quadratic_part

    if quadratic_program.objective['sense'] == OptimizationModel.Sense.MINIMIZE:
        mdl.minimize(objective)
    else:
        mdl.maximize(objective)

    # Constraint handling
    for constr in quadratic_program.linear_constraints:
        linear_expr = mdl.sum(v * var[j] for j, v in constr['linear'].items())
        rhs = constr['rhs']

        if constr['sense'] == OptimizationModel.ConstraintSense.EQ:
            mdl.add_constraint(linear_expr == rhs, ctname=constr.get('name', ''))
        elif constr['sense'] == OptimizationModel.ConstraintSense.GE:
            mdl.add_constraint(linear_expr >= rhs, ctname=constr.get('name', ''))
        elif constr['sense'] == OptimizationModel.ConstraintSense.LE:
            mdl.add_constraint(linear_expr <= rhs, ctname=constr.get('name', ''))

    for constr in quadratic_program.quadratic_constraints:
        quad_expr = (mdl.sum(v * var[j] for j, v in constr['linear'].items()) +
                    mdl.sum(v * var[j] * var[k] for (j, k), v in constr['quadratic'].items()))

        if constr['sense'] == OptimizationModel.ConstraintSense.EQ:
            mdl.add_constraint(quad_expr == constr['rhs'], ctname=constr.get('name', ''))
        elif constr['sense'] == OptimizationModel.ConstraintSense.GE:
            mdl.add_constraint(quad_expr >= constr['rhs'], ctname=constr.get('name', ''))
        elif constr['sense'] == OptimizationModel.ConstraintSense.LE:
            mdl.add_constraint(quad_expr <= constr['rhs'], ctname=constr.get('name', ''))

    return mdl



from typing import List, Tuple, Optional
import numpy as np
from docplex.mp.advmodel import AdvModel
from qiskit_optimization.translators import from_docplex_mp


class PortfolioFormulation:
    def __init__(
        self,
        expected_returns: np.ndarray,
        covariances: np.ndarray,
        risk_factor: float,
        budget: int,
        bounds: Optional[List[Tuple[int, int]]] = None
    ):
        self._expected_returns = expected_returns
        self._covariances = covariances
        self._risk_factor = risk_factor
        self._budget = budget
        self._bounds = bounds
        self._check_compatibility(bounds)

    def build_model(self) -> AdvModel:
        num_assets = len(self._expected_returns)
        mdl = AdvModel(name="Portfolio Optimization")

        # Variable creation with corrected bounds reference
        if self._bounds:
            x = [
                mdl.integer_var(lb=self._bounds[i][0],
                              ub=self._bounds[i][1],
                              name=f"x_{i}")
                for i in range(num_assets)
            ]
        else:
            x = [mdl.binary_var(name=f"x_{i}") for i in range(num_assets)]

        # Quadratic risk term using explicit sum
        quadratic_risk = mdl.sum(
            self._covariances[i][j] * x[i] * x[j]
            for i in range(num_assets)
            for j in range(num_assets)
        )

        # Linear returns term
        linear_returns = mdl.scal_prod(x, self._expected_returns)

        # Objective function
        mdl.minimize(self._risk_factor * quadratic_risk - linear_returns)

        # Budget constraint
        mdl.add_constraint(mdl.sum(x) == self._budget)

        qp = from_docplex_mp(mdl)

        return qp

    # Maintain original analytics methods
    def portfolio_expected_value(self, solution: np.ndarray) -> float:
        return np.dot(self._expected_returns, solution)

    def portfolio_variance(self, solution: np.ndarray) -> float:
        return np.dot(solution, np.dot(self._covariances, solution))

    # Preserve validation logic
    def _check_compatibility(self, bounds):
        # Original validation checks from Qiskit implementation
        if len(self._expected_returns) != len(self._covariances):
            raise ValueError("Mismatch between returns and covariances dimensions")

        if bounds and len(bounds) != len(self._expected_returns):
            raise ValueError("Bounds/asset count mismatch")

    # Retain property accessors
    @property
    def expected_returns(self) -> np.ndarray:
        return self._expected_returns

    @property
    def covariances(self) -> np.ndarray:
        return self._covariances

    @property
    def risk_factor(self) -> float:
        return self._risk_factor

    @property
    def budget(self) -> int:
        return self._budget
