from collections.abc import Mapping
from typing import Any

import numpy as np
from cma import CMAEvolutionStrategy

from bocoel.core.optim.evals import QueryEvaluator
from bocoel.core.optim.interfaces import Optimizer, Task
from bocoel.corpora import Boundary


class PyCMAOptimizer(Optimizer):
    """
    TODO: Documentation.

    CMA-ES
    """

    def __init__(
        self,
        query_eval: QueryEvaluator,
        boundary: Boundary,
        *,
        dims: int,
        samples: int,
        minimize: bool = True,
    ) -> None:
        self._query_eval = query_eval

        self._es = CMAEvolutionStrategy(dims * [0], 0.5)
        self._samples = samples
        self._minimize = minimize
        self._boundary = boundary

    @property
    def task(self) -> Task:
        return Task.MINIMIZE if self._minimize else Task.MAXIMIZE

    @property
    def terminate(self) -> bool:
        return self._es.stop()

    def render(self, **kwargs: Any) -> None:
        raise NotImplementedError

    def step(self) -> Mapping[int, float]:
        solutions = np.array(self._es.ask(self._samples))

        result = self._query_eval(solutions)

        # This works because result keeps the ordering.
        evaluation = np.array(list(result.values()))

        if not self._minimize:
            evaluation = -evaluation

        self._es.tell(solutions, evaluation)

        return result