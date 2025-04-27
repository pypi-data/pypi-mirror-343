from __future__ import annotations
from dataclasses import dataclass, field
from itertools import combinations, product
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

Window = Tuple[float, float]
Kernel = Dict[str, Any]

__all__ = ["PKR"]

@dataclass
class PKR:
    """Pure Kernel Regression estimator.

    Parameters
    ----------
    max_dim : int, default=3
        Maximum kernel dimension (1-3).
    window : float, default=0.5
        Width of numeric windows in scaled space.
    step : float, default=0.25
        Step size for sliding numeric windows.
    min_purity : float, default=0.9
        Minimum proportion of a single y_bin inside a kernel.
    min_count : int, default=10
        Minimum number of rows for a kernel to be valid.
    top_k : int, default=120
        Maximum number of kernels to keep (by purity).
    n_jobs : int, default=-1
        Number of parallel jobs for scanning.
    """
    max_dim: int = 3
    window: float = 0.5
    step: float = 0.25
    min_purity: float = 0.9
    min_count: int = 10
    top_k: int = 120
    n_jobs: int = -1

    # Learned attributes
    kernels_: List[Kernel] = field(default_factory=list, init=False)
    kernels_df_: pd.DataFrame | None = field(default=None, init=False)
    scaling_: Dict[str, Tuple[float, float]] = field(default_factory=dict, init=False)
    rep_: Dict[str, float] = field(default_factory=dict, init=False)
    target_: str | None = field(default=None, init=False)

    def fit(self, df: pd.DataFrame, *, target: str) -> "PKR":
        """Fit the PKR model on the training DataFrame."""
        self.target_ = target
        work = df.copy()
        self._label_polarisation(work)
        predictors = [c for c in work.columns if c not in [target, "y_bin"]]
        self._scale_numeric(work, predictors)
        raw_kernels = self._mine_kernels(work, predictors)
        self.kernels_ = self._select_kernels(raw_kernels)
        self.kernels_df_ = pd.DataFrame(self.kernels_)
        self._compute_reps(work)
        return self

    def predict(self, df: pd.DataFrame) -> np.ndarray:
        """Make continuous predictions for the test DataFrame."""
        self._check_fitted()
        data = df.copy()
        self._apply_scaling(data)
        return np.array([self._predict_row(row) for _, row in data.iterrows()])

    def classify(self, df: pd.DataFrame, no_match_label: int = -1) -> np.ndarray:
        """Return binary labels (0/1) based on kernel matches."""
        self._check_fitted()
        data = df.copy()
        self._apply_scaling(data)
        labels = []
        for _, row in data.iterrows():
            matches = [k["kernel_label"] for k in self.kernels_ if self._row_in_kernel(row, k)]
            if matches:
                labels.append(int(round(np.mean(matches))))
            else:
                labels.append(no_match_label)
        return np.array(labels)

    def get_kernels(self) -> pd.DataFrame:
        """Return the retained kernels as a pandas DataFrame."""
        self._check_fitted()
        return self.kernels_df_.copy()

    def _check_fitted(self):
        if not self.kernels_:
            raise RuntimeError("PKR instance is not fitted yet.")

    def _label_polarisation(self, df: pd.DataFrame):
        q20, q80 = df[self.target_].quantile([0.2, 0.8])
        df["y_bin"] = df[self.target_].apply(
            lambda y: 0 if y <= q20 else (1 if y >= q80 else np.nan)
        )
        df.dropna(subset=["y_bin"], inplace=True)
        df["y_bin"] = df["y_bin"].astype(int)

    def _scale_numeric(self, df: pd.DataFrame, predictors: List[str]):
        for col in predictors:
            if pd.api.types.is_numeric_dtype(df[col]):
                mn, mx = df[col].min(), df[col].max()
                self.scaling_[col] = (mn, mx)
                df[col + "_scaled"] = (df[col] - mn) / (mx - mn)

    def _apply_scaling(self, df: pd.DataFrame):
        for col, (mn, mx) in self.scaling_.items():
            df[col + "_scaled"] = (df[col] - mn) / (mx - mn)

    def _mine_kernels(self, df: pd.DataFrame, predictors: List[str]) -> List[Kernel]:
        all_kernels: List[Kernel] = []
        for dim in range(1, self.max_dim + 1):
            for subset in combinations(predictors, dim):
                all_kernels.extend(self._scan_subset(df, list(subset)))
        return all_kernels

    def _scan_subset(self, df: pd.DataFrame, subset: List[str]) -> List[Kernel]:
        bins_options: Dict[str, List[Any]] = {}
        for col in subset:
            if col in self.scaling_:
                starts = np.arange(0, 1 - self.window + 1e-6, self.step)
                bins_options[col + "_scaled"] = [(s, s + self.window) for s in starts]
            else:
                bins_options[col] = df[col].dropna().unique().tolist()
        keys = list(bins_options.keys())
        combos = product(*[bins_options[k] for k in keys])
        return Parallel(n_jobs=self.n_jobs)(
            delayed(self._evaluate_combo)(combo, keys, df) for combo in combos
        )

    def _evaluate_combo(self, combo: Tuple[Any, ...], keys: List[str], df: pd.DataFrame) -> Kernel | None:
        mask = pd.Series(True, index=df.index)
        kernel: Kernel = {}
        for key, val in zip(keys, combo):
            if key.endswith("_scaled"):
                lo, hi = val
                mask &= (df[key] >= lo) & (df[key] <= hi)
                kernel[key.replace("_scaled", "")] = (lo, hi)
            else:
                mask &= df[key] == val
                kernel[key] = val
        sub = df[mask]
        count = len(sub)
        if count < self.min_count:
            return None
        ratio = sub["y_bin"].mean()
        purity = max(ratio, 1 - ratio)
        if purity < self.min_purity:
            return None
        kernel["kernel_label"] = 1 if ratio > 0.5 else 0
        kernel["kernel_ratio"] = purity
        kernel["count"] = count
        kernel["kernel_metric"] = 1 - purity
        return kernel

    def _select_kernels(self, kernels: List[Kernel]) -> List[Kernel]:
        valid = [k for k in kernels if k]
        valid.sort(key=lambda x: x["kernel_metric"])
        return valid[: self.top_k]

    def _compute_reps(self, df: pd.DataFrame):
        rep0 = df[df["y_bin"] == 0][self.target_].quantile(0.33)
        rep1 = df[df["y_bin"] == 1][self.target_].quantile(0.66)
        rep_mid = df[self.target_].median()
        self.rep_ = {"rep0": rep0, "rep1": rep1, "rep_mid": rep_mid}

    def _row_in_kernel(self, row: pd.Series, kernel: Kernel) -> bool:
        for key, val in kernel.items():
            if key in {"kernel_label", "kernel_ratio", "count", "kernel_metric"}:
                continue
            if isinstance(val, tuple):
                lo, hi = val
                if not (lo <= row[key + "_scaled"] <= hi):
                    return False
            else:
                if str(row[key]).strip() != str(val).strip():
                    return False
        return True

    def _predict_row(self, row: pd.Series) -> float:
        reps = []
        for k in self.kernels_:
            if self._row_in_kernel(row, k):
                reps.append(self.rep_["rep0"] if k["kernel_label"] == 0 else self.rep_["rep1"])
        return float(np.mean(reps)) if reps else self.rep_["rep_mid"]
