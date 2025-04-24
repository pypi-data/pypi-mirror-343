"""
Module defining Bar, which does singular value decomposition
"""

from dataclasses import dataclass

import numpy as np


@dataclass
class Bar:

    """
    Helper class that calculates singular values, and also yells something while doing it
    """

    matrix: np.typing.NDArray[np.floating]
    """matrix to calculate singular values for"""

    def singular_values(self, phrase: str) -> np.typing.NDArray[np.floating]:

        """
        calculate singular values

        Args:
            phrase: Phrase to yell while it's performing SVD
        """

        print(phrase)
        return np.linalg.svdvals(self.matrix)
