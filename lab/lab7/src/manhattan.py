import numpy as np
import pandas as pd


def get_manhattan_distance(
        df1: pd.DataFrame,
        df2: pd.DataFrame,
) -> float:
    if df1.shape != df2.shape:
        raise ValueError(f"DataFrame shapes must match. Got df1={df1.shape}, df2={df2.shape}.")
    if not all(pd.api.types.is_numeric_dtype(dtype) for dtype in df1.dtypes):
        raise TypeError("df1 must contain only numeric values.")
    if not all(pd.api.types.is_numeric_dtype(dtype) for dtype in df2.dtypes):
        raise TypeError("df2 must contain only numeric values.")

    element_wise_dist: pd.DataFrame = (df1 - df2).abs()
    dist: float = element_wise_dist.sum().sum().astype(float)
    return dist

