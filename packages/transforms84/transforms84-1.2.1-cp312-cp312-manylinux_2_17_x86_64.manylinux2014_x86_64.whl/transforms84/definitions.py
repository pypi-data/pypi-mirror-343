from typing import Any, Union

import numpy as np
import numpy.typing as npt
import pandas as pd

NumberLikePy = Union[float, int]
NumberLikeNpy = Union[np.integer[Any], np.floating[Any]]
NumberLike = Union[NumberLikePy, NumberLikeNpy]
ArrayLike = Union[
    npt.NDArray[NumberLikeNpy], "pd.Series[Union[float, int]]", list[NumberLike]
]
