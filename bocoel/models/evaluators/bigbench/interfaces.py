from typing import Protocol

from bocoel.models.evaluators.interfaces import Evaluator
from bocoel.models.scores import Score


class BigBenchEvalutor(Evaluator, Protocol):
    _score_fn: Score