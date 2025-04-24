"""
Module defining Foo, which multiplies matrices
"""

from dataclasses import dataclass

import numpy as np


class ShapeMismatchError(ValueError):

    """
    Error to raise when matrices don't have multiplication-compatible shapes
    """


@dataclass
class Foo:

    first_matrix: np.typing.NDArray[np.floating]
    """first matrix to multiply"""

    second_matrix: np.typing.NDArray[np.floating]
    """second matrix to multiply"""

    def __post_init__(self):

        if not self.first_matrix.shape[1] == self.second_matrix.shape[0]:
            raise ShapeMismatchError("Matrices don't have compatible shapes")

    def multiply_matrices(self) -> np.typing.NDArray[np.floating]:

        """
        Multiply the matrices defined in the helper class
        """

        return self.first_matrix @ self.second_matrix
