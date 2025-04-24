from typing import Union

import numpy.typing as npt

from .definitions import ArrayLike, NumberLike, NumberLikeNpy

def deg_angular_difference(
    angle1: Union[NumberLike, ArrayLike],
    angle2: Union[NumberLike, ArrayLike],
    smallest_angle: bool,
) -> Union[float, npt.NDArray[NumberLikeNpy]]:
    """
    Calculate the angular difference between two angles in degrees.

    :param angle1: First angle in degrees.
    :type angle1: Union[NumberLike, ArrayLike]
    :param angle2: Second angle in degrees.
    :type angle2: Union[NumberLike, ArrayLike]
    :param smallest_angle: If True, return the smallest angular difference.
    :type smallest_angle: bool

    :returns: Angular difference in degrees.
    :rtype: Union[float, npt.NDArray[SUPPORTED_TYPES]]
    """
    ...

def rad_angular_difference(
    angle1: Union[NumberLike, ArrayLike],
    angle2: Union[NumberLike, ArrayLike],
    smallest_angle: bool,
) -> Union[float, npt.NDArray[NumberLikeNpy]]:
    """
    Calculate the angular difference between two angles in radians.

    :param angle1: First angle in radians.
    :type angle1: Union[NumberLike, ArrayLike]
    :param angle2: Second angle in radians.
    :type angle2: Union[NumberLike, ArrayLike]
    :param smallest_angle: If True, return the smallest angular difference.
    :type smallest_angle: bool

    :returns: Angular difference in radians.
    :rtype: Union[float, npt.NDArray[SUPPORTED_TYPES]]
    """
    ...

def RRM2DDM(rrm_position: npt.NDArray[NumberLikeNpy]) -> npt.NDArray[NumberLikeNpy]:
    """Convert array with units radians, radians, X to array with units degrees, degrees, X

    :param rrm_position: Array with units radians, radians, X
    :type rrm_position: npt.NDArray[SUPPORTED_TYPES]
    :return: Array with units degrees, degrees, X
    :rtype: npt.NDArray[SUPPORTED_TYPES]
    """
    ...

def DDM2RRM(ddm_position: npt.NDArray[NumberLikeNpy]) -> npt.NDArray[NumberLikeNpy]:
    """Convert array with units degrees, degrees, X to array with units radians, radians, X

    :param rrm_position: Array with units degrees, degrees, X
    :type rrm_position: npt.NDArray[SUPPORTED_TYPES]
    :return: Array with units radians, radians, X
    :rtype: npt.NDArray[SUPPORTED_TYPES]
    """
    ...

def wrap(
    num: Union[NumberLike, ArrayLike],
    bound_lower: Union[NumberLike, ArrayLike],
    bound_upper: Union[NumberLike, ArrayLike],
) -> Union[float, npt.NDArray[NumberLikeNpy]]:
    """
    Wrap a number or array of numbers within a specified range.

    :param num: Number or array of numbers to be wrapped.
    :type num: Union[NumberLike, ArrayLike]
    :param bound_lower: Lower bound of the range.
    :type bound_lower: Union[NumberLike, ArrayLike]
    :param bound_upper: Upper bound of the range.
    :type bound_upper: Union[NumberLike, ArrayLike]

    :returns: Wrapped number or array of numbers within the specified range.
    :rtype: Union[float, npt.NDArray[SUPPORTED_TYPES]]
    """
    ...
