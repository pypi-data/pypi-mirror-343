from typing import Union, overload

import numpy.typing as npt

from .definitions import ArrayLike, NumberLike, NumberLikeNpy

@overload
def geodetic2UTM(
    rrm_LLA: npt.NDArray[NumberLikeNpy],
    m_semi_major_axis: float,
    m_semi_minor_axis: float,
) -> npt.NDArray[NumberLikeNpy]:
    """
    Convert geodetic coordinates (latitude, longitude, altitude) to UTM coordinates.

    :param rrm_LLA: The geodetic coordinates as a NumPy array.
    :type rrm_LLA: npt.NDArray[NumberLikeNpy]
    :param m_semi_major_axis: The semi-major axis of the ellipsoid.
    :type m_semi_major_axis: float
    :param m_semi_minor_axis: The semi-minor axis of the ellipsoid.
    :type m_semi_minor_axis: float

    :return: The UTM coordinates as a NumPy array.
    :rtype: npt.NDArray[NumberLikeNpy]
    """
    ...

@overload
def geodetic2UTM(
    rad_lat: Union[NumberLike, ArrayLike],
    rad_lon: Union[NumberLike, ArrayLike],
    m_alt: Union[NumberLike, ArrayLike],
    m_semi_major_axis: float,
    m_semi_minor_axis: float,
) -> tuple[
    npt.NDArray[NumberLikeNpy],
    npt.NDArray[NumberLikeNpy],
]:
    """
    Convert geodetic coordinates (latitude, longitude, altitude) to UTM coordinates.

    :param rad_lat: The latitude in radians as a NumPy array, pandas Series, or list of floats.
    :type rad_lat: Union[NumberLike, ArrayLike]
    :param rad_lon: The longitude in radians as a NumPy array, pandas Series, or list of floats.
    :type rad_lon: Union[NumberLike, ArrayLike]
    :param m_alt: The altitude in meters as a NumPy array, pandas Series, or list of floats.
    :type m_alt: Union[NumberLike, ArrayLike]
    :param m_semi_major_axis: The semi-major axis of the ellipsoid.
    :type m_semi_major_axis: float
    :param m_semi_minor_axis: The semi-minor axis of the ellipsoid.
    :type m_semi_minor_axis: float

    :return: The UTM coordinates as a tuple of NumPy arrays.
    :rtype: tuple[npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy]]
    """
    ...

@overload
def UTM2geodetic(
    mmUTM: npt.NDArray[NumberLikeNpy],
    zone_number: int,
    zone_letter: str,
    m_semi_major_axis: float,
    m_semi_minor_axis: float,
) -> npt.NDArray[NumberLikeNpy]:
    """
    Convert UTM coordinates to geodetic coordinates (latitude, longitude, altitude).

    :param mmUTM: The UTM coordinates as a NumPy array.
    :type mmUTM: npt.NDArray[NumberLikeNpy]
    :param zone_number: The UTM zone number.
    :type zone_number: int
    :param zone_letter: The UTM zone letter.
    :type zone_letter: str
    :param m_semi_major_axis: The semi-major axis of the ellipsoid.
    :type m_semi_major_axis: float
    :param m_semi_minor_axis: The semi-minor axis of the ellipsoid.
    :type m_semi_minor_axis: float

    :return: The geodetic coordinates as a NumPy array.
    :rtype: npt.NDArray[NumberLikeNpy]
    """
    ...

@overload
def UTM2geodetic(
    m_X: Union[NumberLike, ArrayLike],
    m_Y: Union[NumberLike, ArrayLike],
    zone_number: int,
    zone_letter: str,
    m_semi_major_axis: float,
    m_semi_minor_axis: float,
) -> tuple[
    npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy]
]:
    """
    Convert UTM coordinates to geodetic coordinates (latitude, longitude, altitude).

    :param m_X: The UTM easting coordinates as a NumPy array, pandas Series, or list of floats.
    :type m_X: Union[NumberLike, ArrayLike]
    :param m_Y: The UTM northing coordinates as a NumPy array, pandas Series, or list of floats.
    :type m_Y: Union[NumberLike, ArrayLike]
    :param zone_number: The UTM zone number.
    :type zone_number: int
    :param zone_letter: The UTM zone letter.
    :type zone_letter: str
    :param m_semi_major_axis: The semi-major axis of the ellipsoid.
    :type m_semi_major_axis: float
    :param m_semi_minor_axis: The semi-minor axis of the ellipsoid.
    :type m_semi_minor_axis: float

    :return: The geodetic coordinates (latitude, longitude, altitude) as a tuple of NumPy arrays.
    :rtype: tuple[npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy]]
    """
    ...

@overload
def geodetic2ECEF(
    rrm_LLA: npt.NDArray[NumberLikeNpy],
    m_semi_major_axis: float,
    m_semi_minor_axis: float,
) -> npt.NDArray[NumberLikeNpy]:
    """
    Convert geodetic coordinates (latitude, longitude, altitude) to ECEF (Earth-Centered, Earth-Fixed) coordinates.

    :param rrm_LLA: The geodetic coordinates as a NumPy array.
    :type rrm_LLA: npt.NDArray[NumberLikeNpy]
    :param m_semi_major_axis: The semi-major axis of the ellipsoid.
    :type m_semi_major_axis: float
    :param m_semi_minor_axis: The semi-minor axis of the ellipsoid.
    :type m_semi_minor_axis: float

    :return: The ECEF coordinates as a NumPy array.
    :rtype: npt.NDArray[NumberLikeNpy]
    """
    ...

@overload
def geodetic2ECEF(
    rad_lat: Union[NumberLike, ArrayLike],
    rad_lon: Union[NumberLike, ArrayLike],
    m_alt: Union[NumberLike, ArrayLike],
    m_semi_major_axis: float,
    m_semi_minor_axis: float,
) -> tuple[
    npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy]
]:
    """
    Convert geodetic coordinates (latitude, longitude, altitude) to ECEF (Earth-Centered, Earth-Fixed) coordinates.

    :param rad_lat: The latitude in radians as a NumPy array, pandas Series, or list of floats.
    :type rad_lat: Union[NumberLike, ArrayLike]
    :param rad_lon: The longitude in radians as a NumPy array, pandas Series, or list of floats.
    :type rad_lon: Union[NumberLike, ArrayLike]
    :param m_alt: The altitude in meters as a NumPy array, pandas Series, or list of floats.
    :type m_alt: Union[NumberLike, ArrayLike]
    :param m_semi_major_axis: The semi-major axis of the ellipsoid.
    :type m_semi_major_axis: float
    :param m_semi_minor_axis: The semi-minor axis of the ellipsoid.
    :type m_semi_minor_axis: float

    :return: The ECEF coordinates (X, Y, Z) as a tuple of NumPy arrays.
    :rtype: tuple[npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy]]
    """
    ...

@overload
def ECEF2geodetic(
    mmm_XYZ: npt.NDArray[NumberLikeNpy],
    m_semi_major_axis: float,
    m_semi_minor_axis: float,
) -> npt.NDArray[NumberLikeNpy]:
    """
    Convert ECEF (Earth-Centered, Earth-Fixed) coordinates to geodetic coordinates (latitude, longitude, altitude).

    :param mmm_XYZ: The ECEF coordinates as a NumPy array.
    :type mmm_XYZ: npt.NDArray[NumberLikeNpy]
    :param m_semi_major_axis: The semi-major axis of the ellipsoid.
    :type m_semi_major_axis: float
    :param m_semi_minor_axis: The semi-minor axis of the ellipsoid.
    :type m_semi_minor_axis: float

    :return: The geodetic coordinates as a NumPy array.
    :rtype: npt.NDArray[NumberLikeNpy]
    """
    ...

@overload
def ECEF2geodetic(
    m_X: Union[NumberLike, ArrayLike],
    m_Y: Union[NumberLike, ArrayLike],
    m_Z: Union[NumberLike, ArrayLike],
    m_semi_major_axis: float,
    m_semi_minor_axis: float,
) -> tuple[
    npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy]
]:
    """
    Convert ECEF (Earth-Centered, Earth-Fixed) coordinates to geodetic coordinates (latitude, longitude, altitude).

    :param m_X: The ECEF X coordinates as a NumPy array, pandas Series, or list of floats.
    :type m_X: Union[NumberLike, ArrayLike]
    :param m_Y: The ECEF Y coordinates as a NumPy array, pandas Series, or list of floats.
    :type m_Y: Union[NumberLike, ArrayLike]
    :param m_Z: The ECEF Z coordinates as a NumPy array, pandas Series, or list of floats.
    :type m_Z: Union[NumberLike, ArrayLike]
    :param m_semi_major_axis: The semi-major axis of the ellipsoid.
    :type m_semi_major_axis: float
    :param m_semi_minor_axis: The semi-minor axis of the ellipsoid.
    :type m_semi_minor_axis: float

    :return: The geodetic coordinates (latitude, longitude, altitude) as a tuple of NumPy arrays.
    :rtype: tuple[npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy]]
    """
    ...

@overload
def ECEF2ENU(
    rrm_LLA_local_origin: npt.NDArray[NumberLikeNpy],
    mmm_XYZ_target: npt.NDArray[NumberLikeNpy],
    m_semi_major_axis: float,
    m_semi_minor_axis: float,
) -> npt.NDArray[NumberLikeNpy]:
    """
    Convert ECEF (Earth-Centered, Earth-Fixed) coordinates to ENU (East-North-Up) coordinates.

    :param rrm_LLA_local_origin: The local origin geodetic coordinates (latitude, longitude, altitude) as a NumPy array.
    :type rrm_LLA_local_origin: npt.NDArray[NumberLikeNpy]
    :param mmm_XYZ_target: The target ECEF coordinates as a NumPy array.
    :type mmm_XYZ_target: npt.NDArray[NumberLikeNpy]
    :param m_semi_major_axis: The semi-major axis of the ellipsoid.
    :type m_semi_major_axis: float
    :param m_semi_minor_axis: The semi-minor axis of the ellipsoid.
    :type m_semi_minor_axis: float

    :return: The ENU coordinates as a NumPy array.
    :rtype: npt.NDArray[NumberLikeNpy]
    """
    ...

@overload
def ECEF2ENU(
    rad_lat_local_origin: Union[NumberLike, ArrayLike],
    rad_lon_local_origin: Union[NumberLike, ArrayLike],
    m_alt_local_origin: Union[NumberLike, ArrayLike],
    m_X_target: Union[NumberLike, ArrayLike],
    m_Y_target: Union[NumberLike, ArrayLike],
    m_Z_target: Union[NumberLike, ArrayLike],
    m_semi_major_axis: float,
    m_semi_minor_axis: float,
) -> tuple[
    npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy]
]:
    """
    Convert ECEF (Earth-Centered, Earth-Fixed) coordinates to ENU (East-North-Up) coordinates.

    :param rad_lat_local_origin: The local origin latitude in radians as a NumPy array, pandas Series, or list of floats.
    :type rad_lat_local_origin: Union[NumberLike, ArrayLike]
    :param rad_lon_local_origin: The local origin longitude in radians as a NumPy array, pandas Series, or list of floats.
    :type rad_lon_local_origin: Union[NumberLike, ArrayLike]
    :param m_alt_local_origin: The local origin altitude in meters as a NumPy array, pandas Series, or list of floats.
    :type m_alt_local_origin: Union[NumberLike, ArrayLike]
    :param m_X_target: The target ECEF X coordinates as a NumPy array, pandas Series, or list of floats.
    :type m_X_target: Union[NumberLike, ArrayLike]
    :param m_Y_target: The target ECEF Y coordinates as a NumPy array, pandas Series, or list of floats.
    :type m_Y_target: Union[NumberLike, ArrayLike]
    :param m_Z_target: The target ECEF Z coordinates as a NumPy array, pandas Series, or list of floats.
    :type m_Z_target: Union[NumberLike, ArrayLike]
    :param m_semi_major_axis: The semi-major axis of the ellipsoid.
    :type m_semi_major_axis: float
    :param m_semi_minor_axis: The semi-minor axis of the ellipsoid.
    :type m_semi_minor_axis: float

    :return: The ENU coordinates (East, North, Up) as a tuple of NumPy arrays.
    :rtype: tuple[npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy]]
    """
    ...

@overload
def ECEF2NED(
    rrm_LLA_local_origin: npt.NDArray[NumberLikeNpy],
    mmm_XYZ_target: npt.NDArray[NumberLikeNpy],
    m_semi_major_axis: float,
    m_semi_minor_axis: float,
) -> npt.NDArray[NumberLikeNpy]:
    """
    Convert ECEF (Earth-Centered, Earth-Fixed) coordinates to NED (North-East-Down) coordinates.

    :param rrm_LLA_local_origin: The local origin geodetic coordinates (latitude, longitude, altitude) as a NumPy array.
    :type rrm_LLA_local_origin: npt.NDArray[NumberLikeNpy]
    :param mmm_XYZ_target: The target ECEF coordinates as a NumPy array.
    :type mmm_XYZ_target: npt.NDArray[NumberLikeNpy]
    :param m_semi_major_axis: The semi-major axis of the ellipsoid.
    :type m_semi_major_axis: float
    :param m_semi_minor_axis: The semi-minor axis of the ellipsoid.
    :type m_semi_minor_axis: float

    :return: The NED coordinates as a NumPy array.
    :rtype: npt.NDArray[NumberLikeNpy]
    """
    ...

@overload
def ECEF2NED(
    rad_lat_local_origin: Union[NumberLike, ArrayLike],
    rad_lon_local_origin: Union[NumberLike, ArrayLike],
    m_alt_local_origin: Union[NumberLike, ArrayLike],
    m_X_target: Union[NumberLike, ArrayLike],
    m_Y_target: Union[NumberLike, ArrayLike],
    m_Z_target: Union[NumberLike, ArrayLike],
    m_semi_major_axis: float,
    m_semi_minor_axis: float,
) -> tuple[
    npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy]
]:
    """
    Convert ECEF (Earth-Centered, Earth-Fixed) coordinates to NED (North-East-Down) coordinates.

    :param rad_lat_local_origin: The local origin latitude in radians as a NumPy array, pandas Series, or list of floats.
    :type rad_lat_local_origin: Union[NumberLike, ArrayLike]
    :param rad_lon_local_origin: The local origin longitude in radians as a NumPy array, pandas Series, or list of floats.
    :type rad_lon_local_origin: Union[NumberLike, ArrayLike]
    :param m_alt_local_origin: The local origin altitude in meters as a NumPy array, pandas Series, or list of floats.
    :type m_alt_local_origin: Union[NumberLike, ArrayLike]
    :param m_X_target: The target ECEF X coordinates as a NumPy array, pandas Series, or list of floats.
    :type m_X_target: Union[NumberLike, ArrayLike]
    :param m_Y_target: The target ECEF Y coordinates as a NumPy array, pandas Series, or list of floats.
    :type m_Y_target: Union[NumberLike, ArrayLike]
    :param m_Z_target: The target ECEF Z coordinates as a NumPy array, pandas Series, or list of floats.
    :type m_Z_target: Union[NumberLike, ArrayLike]
    :param m_semi_major_axis: The semi-major axis of the ellipsoid.
    :type m_semi_major_axis: float
    :param m_semi_minor_axis: The semi-minor axis of the ellipsoid.
    :type m_semi_minor_axis: float

    :return: The NED coordinates (North, East, Down) as a tuple of NumPy arrays.
    :rtype: tuple[npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy]]
    """
    ...

@overload
def ECEF2ENUv(
    rad_lat_local_origin: Union[NumberLike, ArrayLike],
    rad_lon_local_origin: Union[NumberLike, ArrayLike],
    m_alt_local_origin: Union[NumberLike, ArrayLike],
    m_X_target: Union[NumberLike, ArrayLike],
    m_Y_target: Union[NumberLike, ArrayLike],
    m_Z_target: Union[NumberLike, ArrayLike],
) -> tuple[
    npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy]
]:
    """
    Convert ECEF (Earth-Centered, Earth-Fixed) velocity coordinates to ENU (East-North-Up) velocity coordinates.

    :param rad_lat_local_origin: The local origin latitude in radians as a NumPy array, pandas Series, or list of floats.
    :type rad_lat_local_origin: Union[NumberLike, ArrayLike]
    :param rad_lon_local_origin: The local origin longitude in radians as a NumPy array, pandas Series, or list of floats.
    :type rad_lon_local_origin: Union[NumberLike, ArrayLike]
    :param m_alt_local_origin: The local origin altitude in meters as a NumPy array, pandas Series, or list of floats.
    :type m_alt_local_origin: Union[NumberLike, ArrayLike]
    :param m_X_target: The target ECEF X velocity coordinates as a NumPy array, pandas Series, or list of floats.
    :type m_X_target: Union[NumberLike, ArrayLike]
    :param m_Y_target: The target ECEF Y velocity coordinates as a NumPy array, pandas Series, or list of floats.
    :type m_Y_target: Union[NumberLike, ArrayLike]
    :param m_Z_target: The target ECEF Z velocity coordinates as a NumPy array, pandas Series, or list of floats.
    :type m_Z_target: Union[NumberLike, ArrayLike]

    :return: The ENU velocity coordinates (East, North, Up) as a tuple of NumPy arrays.
    :rtype: tuple[npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy]]
    """
    ...

@overload
def ECEF2ENUv(
    rrm_LLA_local_origin: npt.NDArray[NumberLikeNpy],
    mmm_XYZ_target: npt.NDArray[NumberLikeNpy],
) -> npt.NDArray[NumberLikeNpy]:
    """
    Convert ECEF (Earth-Centered, Earth-Fixed) velocity coordinates to ENU (East-North-Up) velocity coordinates.

    :param rrm_LLA_local_origin: The local origin geodetic velocity coordinates (latitude, longitude, altitude) as a NumPy array.
    :type rrm_LLA_local_origin: npt.NDArray[NumberLikeNpy]
    :param mmm_XYZ_target: The target ECEF velocity coordinates as a NumPy array.
    :type mmm_XYZ_target: npt.NDArray[NumberLikeNpy]

    :return: The ENU velocity coordinates as a NumPy array.
    :rtype: npt.NDArray[NumberLikeNpy]
    """
    ...

@overload
def ECEF2NEDv(
    rrm_LLA_local_origin: npt.NDArray[NumberLikeNpy],
    mmm_XYZ_target: npt.NDArray[NumberLikeNpy],
) -> npt.NDArray[NumberLikeNpy]:
    """
    Convert ECEF (Earth-Centered, Earth-Fixed) velocity coordinates to NED (North-East-Down) velocity coordinates.

    :param rrm_LLA_local_origin: The local origin geodetic velocity coordinates (latitude, longitude, altitude) as a NumPy array.
    :type rrm_LLA_local_origin: npt.NDArray[NumberLikeNpy]
    :param mmm_XYZ_target: The target ECEF velocity coordinates as a NumPy array.
    :type mmm_XYZ_target: npt.NDArray[NumberLikeNpy]

    :return: The NED velocity coordinates as a NumPy array.
    :rtype: npt.NDArray[NumberLikeNpy]
    """
    ...

@overload
def ECEF2NEDv(
    rad_lat_local_origin: Union[NumberLike, ArrayLike],
    rad_lon_local_origin: Union[NumberLike, ArrayLike],
    m_alt_local_origin: Union[NumberLike, ArrayLike],
    m_X_target: Union[NumberLike, ArrayLike],
    m_Y_target: Union[NumberLike, ArrayLike],
    m_Z_target: Union[NumberLike, ArrayLike],
) -> tuple[
    npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy]
]:
    """
    Convert ECEF (Earth-Centered, Earth-Fixed) velocity coordinates to NED (North-East-Down) velocity coordinates.

    :param rad_lat_local_origin: The local origin latitude in radians as a NumPy array, pandas Series, or list of floats.
    :type rad_lat_local_origin: Union[NumberLike, ArrayLike]
    :param rad_lon_local_origin: The local origin longitude in radians as a NumPy array, pandas Series, or list of floats.
    :type rad_lon_local_origin: Union[NumberLike, ArrayLike]
    :param m_alt_local_origin: The local origin altitude in meters as a NumPy array, pandas Series, or list of floats.
    :type m_alt_local_origin: Union[NumberLike, ArrayLike]
    :param m_X_target: The target ECEF X velocity coordinates as a NumPy array, pandas Series, or list of floats.
    :type m_X_target: Union[NumberLike, ArrayLike]
    :param m_Y_target: The target ECEF Y velocity coordinates as a NumPy array, pandas Series, or list of floats.
    :type m_Y_target: Union[NumberLike, ArrayLike]
    :param m_Z_target: The target ECEF Z velocity coordinates as a NumPy array, pandas Series, or list of floats.
    :type m_Z_target: Union[NumberLike, ArrayLike]

    :return: The NED velocity coordinates (North, East, Down) as a tuple of NumPy arrays.
    :rtype: tuple[npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy]]
    """
    ...

@overload
def ENU2ECEF(
    rad_lat_local_origin: Union[NumberLike, ArrayLike],
    rad_lon_local_origin: Union[NumberLike, ArrayLike],
    m_alt_local_origin: Union[NumberLike, ArrayLike],
    m_east: Union[NumberLike, ArrayLike],
    m_north: Union[NumberLike, ArrayLike],
    m_up: Union[NumberLike, ArrayLike],
    m_semi_major_axis: float,
    m_semi_minor_axis: float,
) -> tuple[
    npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy]
]:
    """
    Convert ENU (East-North-Up) coordinates to ECEF (Earth-Centered, Earth-Fixed) coordinates.

    :param rad_lat_local_origin: The local origin latitude in radians as a NumPy array, pandas Series, or list of floats.
    :type rad_lat_local_origin: Union[NumberLike, ArrayLike]
    :param rad_lon_local_origin: The local origin longitude in radians as a NumPy array, pandas Series, or list of floats.
    :type rad_lon_local_origin: Union[NumberLike, ArrayLike]
    :param m_alt_local_origin: The local origin altitude in meters as a NumPy array, pandas Series, or list of floats.
    :type m_alt_local_origin: Union[NumberLike, ArrayLike]
    :param m_east: The East coordinate in meters as a NumPy array, pandas Series, or list of floats.
    :type m_east: Union[NumberLike, ArrayLike]
    :param m_north: The North coordinate in meters as a NumPy array, pandas Series, or list of floats.
    :type m_north: Union[NumberLike, ArrayLike]
    :param m_up: The Up coordinate in meters as a NumPy array, pandas Series, or list of floats.
    :type m_up: Union[NumberLike, ArrayLike]
    :param m_semi_major_axis: The semi-major axis of the ellipsoid.
    :type m_semi_major_axis: float
    :param m_semi_minor_axis: The semi-minor axis of the ellipsoid.
    :type m_semi_minor_axis: float

    :return: The ECEF coordinates (X, Y, Z) as a tuple of NumPy arrays.
    :rtype: tuple[npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy]]
    """
    ...

@overload
def ENU2ECEF(
    rrm_LLA_local_origin: npt.NDArray[NumberLikeNpy],
    mmm_XYZ_local: npt.NDArray[NumberLikeNpy],
    m_semi_major_axis: float,
    m_semi_minor_axis: float,
) -> npt.NDArray[NumberLikeNpy]:
    """
    Convert ENU (East-North-Up) coordinates to ECEF (Earth-Centered, Earth-Fixed) coordinates.

    :param rrm_LLA_local_origin: The local origin geodetic coordinates (latitude, longitude, altitude) as a NumPy array.
    :type rrm_LLA_local_origin: npt.NDArray[NumberLikeNpy]
    :param mmm_XYZ_local: The local ENU coordinates as a NumPy array.
    :type mmm_XYZ_local: npt.NDArray[NumberLikeNpy]
    :param m_semi_major_axis: The semi-major axis of the ellipsoid.
    :type m_semi_major_axis: float
    :param m_semi_minor_axis: The semi-minor axis of the ellipsoid.
    :type m_semi_minor_axis: float

    :return: The ECEF coordinates as a NumPy array.
    :rtype: npt.NDArray[NumberLikeNpy]
    """
    ...

@overload
def NED2ECEF(
    rad_lat_local_origin: Union[NumberLike, ArrayLike],
    rad_lon_local_origin: Union[NumberLike, ArrayLike],
    m_alt_local_origin: Union[NumberLike, ArrayLike],
    m_north: Union[NumberLike, ArrayLike],
    m_east: Union[NumberLike, ArrayLike],
    m_down: Union[NumberLike, ArrayLike],
    m_semi_major_axis: float,
    m_semi_minor_axis: float,
) -> tuple[
    npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy]
]:
    """
    Convert NED (North-East-Down) coordinates to ECEF (Earth-Centered, Earth-Fixed) coordinates.

    :param rad_lat_local_origin: The local origin latitude in radians as a NumPy array, pandas Series, or list of floats.
    :type rad_lat_local_origin: Union[NumberLike, ArrayLike]
    :param rad_lon_local_origin: The local origin longitude in radians as a NumPy array, pandas Series, or list of floats.
    :type rad_lon_local_origin: Union[NumberLike, ArrayLike]
    :param m_alt_local_origin: The local origin altitude in meters as a NumPy array, pandas Series, or list of floats.
    :type m_alt_local_origin: Union[NumberLike, ArrayLike]
    :param m_north: The North coordinate in meters as a NumPy array, pandas Series, or list of floats.
    :type m_north: Union[NumberLike, ArrayLike]
    :param m_east: The East coordinate in meters as a NumPy array, pandas Series, or list of floats.
    :type m_east: Union[NumberLike, ArrayLike]
    :param m_down: The Down coordinate in meters as a NumPy array, pandas Series, or list of floats.
    :type m_down: Union[NumberLike, ArrayLike]
    :param m_semi_major_axis: The semi-major axis of the ellipsoid.
    :type m_semi_major_axis: float
    :param m_semi_minor_axis: The semi-minor axis of the ellipsoid.
    :type m_semi_minor_axis: float

    :return: The ECEF coordinates (X, Y, Z) as a tuple of NumPy arrays.
    :rtype: tuple[npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy]]
    """
    ...

@overload
def NED2ECEF(
    rrm_LLA_local_origin: npt.NDArray[NumberLikeNpy],
    mmm_XYZ_local: npt.NDArray[NumberLikeNpy],
    m_semi_major_axis: float,
    m_semi_minor_axis: float,
) -> npt.NDArray[NumberLikeNpy]:
    """
    Convert NED (North-East-Down) coordinates to ECEF (Earth-Centered, Earth-Fixed) coordinates.

    :param rrm_LLA_local_origin: The local origin geodetic coordinates (latitude, longitude, altitude) as a NumPy array.
    :type rrm_LLA_local_origin: npt.NDArray[NumberLikeNpy]
    :param mmm_XYZ_local: The local NED coordinates as a NumPy array.
    :type mmm_XYZ_local: npt.NDArray[NumberLikeNpy]
    :param m_semi_major_axis: The semi-major axis of the ellipsoid.
    :type m_semi_major_axis: float
    :param m_semi_minor_axis: The semi-minor axis of the ellipsoid.
    :type m_semi_minor_axis: float

    :return: The ECEF coordinates as a NumPy array.
    :rtype: npt.NDArray[NumberLikeNpy]
    """
    ...

@overload
def ENU2ECEFv(
    rad_lat_local_origin: Union[NumberLike, ArrayLike],
    rad_lon_local_origin: Union[NumberLike, ArrayLike],
    m_alt_local_origin: Union[NumberLike, ArrayLike],
    m_east: Union[NumberLike, ArrayLike],
    m_north: Union[NumberLike, ArrayLike],
    m_up: Union[NumberLike, ArrayLike],
) -> tuple[
    npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy]
]:
    """
    Convert ENU (East-North-Up) velocity coordinates to ECEF (Earth-Centered, Earth-Fixed) velocity coordinates.

    :param rad_lat_local_origin: The local origin latitude in radians as a NumPy array, pandas Series, or list of floats.
    :type rad_lat_local_origin: Union[NumberLike, ArrayLike]
    :param rad_lon_local_origin: The local origin longitude in radians as a NumPy array, pandas Series, or list of floats.
    :type rad_lon_local_origin: Union[NumberLike, ArrayLike]
    :param m_alt_local_origin: The local origin altitude in meters as a NumPy array, pandas Series, or list of floats.
    :type m_alt_local_origin: Union[NumberLike, ArrayLike]
    :param m_east: The East coordinate in meters as a NumPy array, pandas Series, or list of floats.
    :type m_east: Union[NumberLike, ArrayLike]
    :param m_north: The North coordinate in meters as a NumPy array, pandas Series, or list of floats.
    :type m_north: Union[NumberLike, ArrayLike]
    :param m_up: The Up coordinate in meters as a NumPy array, pandas Series, or list of floats.
    :type m_up: Union[NumberLike, ArrayLike]

    :return: The ECEF velocity coordinates (X, Y, Z) as a tuple of NumPy arrays.
    :rtype: tuple[npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy]]
    """
    ...

@overload
def ENU2ECEFv(
    rrm_LLA_local_origin: npt.NDArray[NumberLikeNpy],
    mmm_XYZ_local: npt.NDArray[NumberLikeNpy],
) -> npt.NDArray[NumberLikeNpy]:
    """
    Convert ENU (East-North-Up) velocity coordinates to ECEF (Earth-Centered, Earth-Fixed) velocity coordinates.

    :param rrm_LLA_local_origin: The local origin geodetic velocity coordinates (latitude, longitude, altitude) as a NumPy array.
    :type rrm_LLA_local_origin: npt.NDArray[NumberLikeNpy]
    :param mmm_XYZ_local: The local ENU velocity coordinates as a NumPy array.
    :type mmm_XYZ_local: npt.NDArray[NumberLikeNpy]

    :return: The ECEF velocity coordinates as a NumPy array.
    :rtype: npt.NDArray[NumberLikeNpy]
    """
    ...

@overload
def NED2ECEFv(
    rad_lat_local_origin: Union[NumberLike, ArrayLike],
    rad_lon_local_origin: Union[NumberLike, ArrayLike],
    m_alt_local_origin: Union[NumberLike, ArrayLike],
    m_north: Union[NumberLike, ArrayLike],
    m_east: Union[NumberLike, ArrayLike],
    m_down: Union[NumberLike, ArrayLike],
) -> tuple[
    npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy]
]:
    """
    Convert NED (North-East-Down) velocity coordinates to ECEF (Earth-Centered, Earth-Fixed) velocity coordinates.

    :param rad_lat_local_origin: The local origin latitude in radians as a NumPy array, pandas Series, or list of floats.
    :type rad_lat_local_origin: Union[NumberLike, ArrayLike]
    :param rad_lon_local_origin: The local origin longitude in radians as a NumPy array, pandas Series, or list of floats.
    :type rad_lon_local_origin: Union[NumberLike, ArrayLike]
    :param m_alt_local_origin: The local origin altitude in meters as a NumPy array, pandas Series, or list of floats.
    :type m_alt_local_origin: Union[NumberLike, ArrayLike]
    :param m_north: The North velocity coordinate in meters as a NumPy array, pandas Series, or list of floats.
    :type m_north: Union[NumberLike, ArrayLike]
    :param m_east: The East velocity coordinate in meters as a NumPy array, pandas Series, or list of floats.
    :type m_east: Union[NumberLike, ArrayLike]
    :param m_down: The Down velocity coordinate in meters as a NumPy array, pandas
    :type m_down: Union[NumberLike, ArrayLike]

    :return: The ECEF velocity coordinates (X, Y, Z) as a tuple of NumPy arrays.
    :rtype: tuple[npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy]]
    """
    ...

@overload
def NED2ECEFv(
    rrm_LLA_local_origin: npt.NDArray[NumberLikeNpy],
    mmm_XYZ_local: npt.NDArray[NumberLikeNpy],
) -> npt.NDArray[NumberLikeNpy]:
    """
    Convert NED (North-East-Down) velocity coordinates to ECEF (Earth-Centered, Earth-Fixed) velocity coordinates.

    :param rrm_LLA_local_origin: The local origin geodetic velocity coordinates (latitude, longitude, altitude) as a NumPy array.
    :type rrm_LLA_local_origin: npt.NDArray[NumberLikeNpy]
    :param mmm_XYZ_local: The local NED velocity coordinates as a NumPy array.
    :type mmm_XYZ_local: npt.NDArray[NumberLikeNpy]

    :return: The ECEF velocity coordinates as a NumPy array.
    :rtype: npt.NDArray[NumberLikeNpy]
    """
    ...

@overload
def ENU2AER(
    m_east: Union[NumberLike, ArrayLike],
    m_north: Union[NumberLike, ArrayLike],
    m_up: Union[NumberLike, ArrayLike],
) -> tuple[
    npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy]
]:
    """
    Convert ENU (East-North-Up) coordinates to AER (Azimuth-Elevation-Range) coordinates.

    :param m_east: Array of East coordinates.
    :type m_east: Union[NumberLike, ArrayLike]
    :param m_north: Array of North coordinates.
    :type m_north: Union[NumberLike, ArrayLike]
    :param m_up: Array of Up coordinates.
    :type m_up: Union[NumberLike, ArrayLike]

    :returns: Tuple containing arrays of Azimuth, Elevation, and Range coordinates.
    :rtype: tuple[npt.NDArray[NumberLikeNpy],
                npt.NDArray[NumberLikeNpy],
                npt.NDArray[NumberLikeNpy]]
    """
    ...

@overload
def ENU2AER(mmm_ENU: npt.NDArray[NumberLikeNpy]) -> npt.NDArray[NumberLikeNpy]:
    """
    Convert ENU (East-North-Up) coordinates to AER (Azimuth-Elevation-Range) coordinates.

    :param mmm_ENU: Array of ENU coordinates.
    :type mmm_ENU: npt.NDArray[NumberLikeNpy]

    :returns: Array of AER coordinates.
    :rtype: npt.NDArray[NumberLikeNpy]
    """
    ...

@overload
def AER2ENU(
    rad_az: Union[NumberLike, ArrayLike],
    rad_el: Union[NumberLike, ArrayLike],
    m_range: Union[NumberLike, ArrayLike],
) -> tuple[
    npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy]
]:
    """
    Convert AER (Azimuth-Elevation-Range) coordinates to ENU (East-North-Up) coordinates.

    :param rad_az: Array of Azimuth angles in radians as a NumPy array, pandas Series, list, or set.
    :type rad_az: Union[NumberLike, ArrayLike]
    :param rad_el: Array of Elevation angles in radians as a NumPy array, pandas Series, list, or set.
    :type rad_el: Union[NumberLike, ArrayLike]
    :param m_range: Array of Range distances as a NumPy array, pandas Series, list, or set.
    :type m_range: Union[NumberLike, ArrayLike]

    :returns: Tuple containing arrays of East, North, and Up coordinates.
    :rtype: tuple[npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy]]
    """
    ...

@overload
def AER2ENU(rrm_AER: npt.NDArray[NumberLikeNpy]) -> npt.NDArray[NumberLikeNpy]:
    """
    Convert AER (Azimuth-Elevation-Range) coordinates to ENU (East-North-Up) coordinates.

    :param rrm_AER: Array of AER coordinates.
    :type rrm_AER: npt.NDArray[NumberLikeNpy]

    :returns: Array of ENU coordinates.
    :rtype: npt.NDArray[NumberLikeNpy]
    """
    ...

@overload
def NED2AER(mmm_NED: npt.NDArray[NumberLikeNpy]) -> npt.NDArray[NumberLikeNpy]:
    """
    Convert NED (North-East-Down) coordinates to AER (Azimuth-Elevation-Range) coordinates.

    :param mmm_NED: Array of NED coordinates.
    :type mmm_NED: npt.NDArray[NumberLikeNpy]

    :returns: Array of AER coordinates.
    :rtype: npt.NDArray[NumberLikeNpy]
    """
    ...

@overload
def NED2AER(
    m_north: Union[NumberLike, ArrayLike],
    m_east: Union[NumberLike, ArrayLike],
    m_down: Union[NumberLike, ArrayLike],
) -> tuple[
    npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy]
]:
    """
    Convert NED (North-East-Down) coordinates to AER (Azimuth-Elevation-Range) coordinates.

    :param m_north: Array of North coordinates as a NumPy array, pandas Series, or list of floats.
    :type m_north: Union[NumberLike, ArrayLike]
    :param m_east: Array of East coordinates as a NumPy array, pandas Series, or list of floats.
    :type m_east: Union[NumberLike, ArrayLike]
    :param m_down: Array of Down coordinates as a NumPy array, pandas Series, or list of floats.
    :type m_down: Union[NumberLike, ArrayLike]

    :returns: Tuple containing arrays of Azimuth, Elevation, and Range coordinates.
    :rtype: tuple[npt.NDArray[NumberLikeNpy],
                npt.NDArray[NumberLikeNpy],
                npt.NDArray[NumberLikeNpy]]
    """
    ...

@overload
def AER2NED(rrm_AER: npt.NDArray[NumberLikeNpy]) -> npt.NDArray[NumberLikeNpy]:
    """
    Convert AER (Azimuth-Elevation-Range) coordinates to NED (North-East-Down) coordinates.

    :param rrm_AER: Array of AER coordinates.
    :type rrm_AER: npt.NDArray[NumberLikeNpy]

    :returns: Array of NED coordinates.
    :rtype: npt.NDArray[NumberLikeNpy]
    """
    ...

@overload
def AER2NED(
    rad_az: Union[NumberLike, ArrayLike],
    rad_el: Union[NumberLike, ArrayLike],
    m_range: Union[NumberLike, ArrayLike],
) -> tuple[
    npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy], npt.NDArray[NumberLikeNpy]
]:
    """
    Convert AER (Azimuth-Elevation-Range) coordinates to NED (North-East-Down) coordinates.

    :param rad_az: Array of Azimuth angles in radians as a NumPy array, pandas Series, or list of floats.
    :type rad_az: Union[NumberLike, ArrayLike]
    :param rad_el: Array of Elevation angles in radians as a NumPy array, pandas Series, or list of floats.
    :type rad_el: Union[NumberLike, ArrayLike]
    :param m_range: Array of Range distances as a NumPy array, pandas Series, or list of floats.
    :type m_range: Union[NumberLike, ArrayLike]

    :returns: Tuple containing arrays of North, East, and Down coordinates.
    :rtype: tuple[npt.NDArray[NumberLikeNpy],
                npt.NDArray[NumberLikeNpy],
                npt.NDArray[NumberLikeNpy]]
    """
    ...
