from __future__ import annotations
from typing import Literal
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator


class AltmanModel(BaseEstimator):

    def __init__(self) -> None:
        self.limitParameter = 1.8
        self.isFitted = False
        self.coefficients = np.ndarray
        super().__init__()

    @property
    def coef(self) -> np.ndarray:
        return self.coefficients

    def fit(self) -> AltmanModel:
        self.coefficients = np.array([0.254, 0.448, 0.0896, 1.583, 3.284])
        self.isFitted = True
        return self

    def predict(self, X) -> np.ndarray:
        if not self.isFitted:
            raise NotFittedError(
                "Model musi być wytrenowany przed predykcją."
            )
        labels = X.apply(self._predict_label, axis=1)
        labels = labels.to_numpy()
        return labels

    def _predict_value(self, series: pd.Series) -> float:
        value = series.dot(self.coefficients)
        return value

    def _predict_label(self, series: pd.Series) -> Literal[0, 1]:
        value = self._predict_value(series)
        return 1 if value < self.limitParameter else 0


class GroverModel(BaseEstimator):

    def __init__(self) -> None:
        self.limitParameter = -0.02
        self.isFitted = False
        self.coefficients = np.ndarray
        super().__init__()

    @property
    def coef(self) -> np.ndarray:
        return self.coefficients

    def fit(self) -> GroverModel:
        self.coefficients = np.array([1.650, 3.404, -0.016])
        self.isFitted = True
        return self

    def predict(self, X) -> np.ndarray:
        if not self.isFitted:
            raise NotFittedError(
                "Model musi być wytrenowany przed predykcją."
            )
        labels = X.apply(self._predict_label, axis=1)
        labels = labels.to_numpy()
        return labels

    def _predict_value(self, series: pd.Series) -> float:
        value = 0.057 + series.dot(self.coefficients)
        return value

    def _predict_label(self, series: pd.Series) -> Literal[0, 1]:
        value = self._predict_value(series)
        return 1 if value < self.limitParameter else 0


class ZmijewskiModel(BaseEstimator):

    def __init__(self) -> None:
        self.limitParameter = 0
        self.isFitted = False
        self.coefficients = np.ndarray
        super().__init__()

    @property
    def coef(self) -> np.ndarray:
        return self.coefficients

    def fit(self) -> ZmijweskiModel:
        self.coefficients = np.array([-4.5, 5.7, -0.004])
        self.isFitted = True
        return self

    def predict(self, X) -> np.ndarray:
        if not self.isFitted:
            raise NotFittedError(
                "Model musi być wytrenowany przed predykcją."
            )
        labels = X.apply(self._predict_label, axis=1)
        labels = labels.to_numpy()
        return labels

    def _predict_value(self, series: pd.Series) -> float:
        value = -4.3 + series.dot(self.coefficients)
        return value

    def _predict_label(self, series: pd.Series) -> Literal[0, 1]:
        value = self._predict_value(series)
        return 1 if value > self.limitParameter else 0


class NotFittedError(Exception):
    ...
