"""Module for coordinate frame transformations and conversions."""

from copy import deepcopy

import numpy as np
from scipy.spatial.transform import Rotation


class CoordinateFrame:
    """Represents a coordinate frame and provides methods for coordinate transformations.

    Coordinate frames are defined by an origin offset vector and an origin rotation.
    A reference coordinate system must be specified with a name and an index.

    Parameters
    ----------
    coordinate_system_name : str
        The name of the coordinate system.
    coordinate_system_index : int
        The index of the coordinate system.
    origin_offset_vector : numpy.ndarray
        The offset vector of the origin of the coordinate system.
    origin_rotation : scipy.spatial.transform.Rotation
        The rotation of the coordinate system.
    reference_coordinate_system_name : str
        The name of the reference coordinate system.
    reference_coordinate_system_index : int
        The index of the reference coordinate system.
    variant : str
        The variant of the coordinate system (e.g. NED, ENU).

    """

    def __init__(
        self,
        coordinate_system_name,
        coordinate_system_index,
        origin_offset_vector,
        origin_rotation,
        reference_coordinate_system_name,
        reference_coordinate_system_index,
        variant,
    ):
        """Initialize a CoordinateFrame object.

        Parameters
        ----------
        coordinate_system_name : str
            The name of the coordinate system.
        coordinate_system_index : int
            The index of the coordinate system.
        origin_offset_vector : np.ndarray
            The offset vector of the origin of the coordinate system.
        origin_rotation : scipy.spatial.transform.Rotation
            The rotation of the coordinate system.
        reference_coordinate_system_name : str
            The name of the reference coordinate system.
        reference_coordinate_system_index : int
            The index of the reference coordinate system.
        variant : str
            The variant of the coordinate system (e.g. NED, ENU).

        """
        self.coordinate_system_name = coordinate_system_name
        self.coordinate_system_index = coordinate_system_index
        self.origin_offset_vector = origin_offset_vector
        self.origin_rotation = origin_rotation
        self.reference_coordinate_system_name = reference_coordinate_system_name
        self.reference_coordinate_system_index = reference_coordinate_system_index
        self.variant = variant

    @classmethod
    def from_odl(cls, coord_system_parms):
        """Create a CoordinateFrame object from an ODL COORD_SYSTEM_PARMS dictionary.

        Parameters
        ----------
        coord_system_parms : dict
            Dictionary containing coordinate system parameters.

        Returns
        -------
        CoordinateFrame
            An instance of the CoordinateFrame class.

        Note
        -----
        The dictionary `coord_system_parms` must contain the following keys:

          - "COORDINATE_SYSTEM_NAME"
          - "COORDINATE_SYSTEM_INDEX"
          - "ORIGIN_OFFSET_VECTOR"
          - "ORIGIN_ROTATION_QUATERNION"
          - "REFERENCE_COORD_SYSTEM_NAME"
          - "REFERENCE_COORD_SYSTEM_INDEX"

        """
        coordinate_system_name = coord_system_parms['COORDINATE_SYSTEM_NAME']
        coordinate_system_index = coord_system_parms['COORDINATE_SYSTEM_INDEX']
        origin_offset_vector = list(coord_system_parms['ORIGIN_OFFSET_VECTOR'])
        origin_rotation = Rotation.from_quat(
            q_wxyz2xyzw(coord_system_parms['ORIGIN_ROTATION_QUATERNION'])
        )
        reference_coordinate_system_name = coord_system_parms['REFERENCE_COORD_SYSTEM_NAME']
        reference_coordinate_system_index = coord_system_parms['REFERENCE_COORD_SYSTEM_INDEX']
        variant = 'NED'

        return cls(
            coordinate_system_name,
            coordinate_system_index,
            origin_offset_vector,
            origin_rotation,
            reference_coordinate_system_name,
            reference_coordinate_system_index,
            variant,
        )

    @property
    def origin_rotation_quaternion(self):
        """Convenience function, returns the origin rotation in JPL style quaternion."""
        return q_xyzw2wxyz(self.origin_rotation.as_quat())

    @property
    def origin_rotation_matrix(self):
        """Convenience function, returns the origin rotation as a rotation matrix."""
        return self.origin_rotation.as_matrix()

    def transform_to(self, target_system):
        """Transform the coordinate system to a specified reference system.

        Note
        -----
        The reference system must match the reference system of the coordinate system.
        The reference system must be a CoordinateFrame object with the same coordinate
        system variant (e.g. NED, ENU).

        Parameters
        ----------
        target_system : CoordinateFrame
            The reference system to transform to.

        Returns
        -------
        CoordinateFrame
            The transformed coordinate system.

        Raises
        ------
        ValueError

          -  If the target system is not a CoordinateFrame object.
          -  If the target system does not have the same reference system name.
          -  If the target system does not have the same reference system index.
          -  If the target system does not have the same variant.

        """
        if not isinstance(target_system, CoordinateFrame):
            raise ValueError('Target system must be a CoordinateFrame object')

        if target_system.coordinate_system_name != self.reference_coordinate_system_name:
            raise ValueError(f"""Target system (name: {target_system.coordinate_system_name})
                    must be the same as the reference system of the coordinate system
                    (name: {self.reference_coordinate_system_name})""")

        if target_system.coordinate_system_index != self.reference_coordinate_system_index:
            raise ValueError(f"""Target system (index: {target_system.coordinate_system_index})
                    must be the same as the reference system of the coordinate system
                    (index: {self.reference_coordinate_system_index})""")

        if target_system.variant != self.variant:
            raise ValueError("""Target system must conform to the same coordinate system
                    variant (e.g. NED, ENU)""")

        # copy the target coordinate system and its methods
        transformed = deepcopy(target_system)

        # apply the transformation
        transformed.origin_rotation = target_system.origin_rotation * self.origin_rotation
        transformed.origin_offset_vector = (
            target_system.origin_rotation.apply(
                self.origin_offset_vector,
            )
            + target_system.origin_offset_vector
        )

        # overwrite the coordinate system name and index
        transformed.coordinate_system_name = self.coordinate_system_name
        transformed.coordinate_system_index = self.coordinate_system_index

        # change reference system
        transformed.reference_coordinate_system_name = (
            target_system.reference_coordinate_system_name
        )
        transformed.reference_coordinate_system_index = (
            target_system.reference_coordinate_system_index
        )

        return transformed  # return the transformed coordinate system

    def xyz(self, variant='NED'):
        """Return the xyz coordinates of the origin of the coordinate system.

        Parameters
        ----------
        variant : str, optional
            The coordinate system variant, by default "NED".

        Returns
        -------
        numpy.ndarray
            The xyz coordinates of the origin of the coordinate system.
        """
        if variant == self.variant:
            return self.origin_offset_vector

        # otherwise convert NED to ENU or vice versa
        return np.array(
            [
                self.origin_offset_vector[1],
                self.origin_offset_vector[0],
                -self.origin_offset_vector[2],
            ],
        )

    @property
    def easting(self):
        """Return the easting coordinate of the origin of the coordinate system.

        Returns
        -------
        float
            The easting coordinate of the origin.

        Raises
        ------
        ValueError
            If the reference coordinate system is not "ORBITAL" or if the variant is unknown.

        """
        if self.reference_coordinate_system_name != 'ORBITAL':
            raise ValueError(
                'Easting is only defined for coordinate systems with reference system ORBITAL',
            )
        if self.variant == 'NED':
            return self.origin_offset_vector[1]
        if self.variant == 'ENU':
            return self.origin_offset_vector[0]
        raise ValueError(f'Unknown variant {self.variant}')

    @property
    def northing(self):
        """Returns the northing coordinate of the origin of the coordinate system.

        Returns
        -------
        float
            The northing coordinate of the origin.

        Raises
        ------
        ValueError
            If the reference coordinate system is not "ORBITAL" or if the variant is unknown.

        """
        if self.reference_coordinate_system_name != 'ORBITAL':
            raise ValueError(
                'Northing is only defined for coordinate systems with reference system ORBITAL',
            )
        if self.variant == 'NED':
            return self.origin_offset_vector[0]
        if self.variant == 'ENU':
            return self.origin_offset_vector[1]
        raise ValueError(f'Unknown variant {self.variant}')

    @property
    def elevation(self):
        """Return the elevation of the origin of the coordinate system.

        Returns
        -------
        float
            The elevation coordinate of the origin in the ORBITAL coordinate system.

        Raises
        ------
        ValueError
            If the reference coordinate system is not "ORBITAL" or if the variant is unknown.

        """
        if self.reference_coordinate_system_name != 'ORBITAL':
            raise ValueError(
                'Elevation is only defined for coordinate systems with reference system ORBITAL',
            )
        if self.variant == 'NED':
            return -self.origin_offset_vector[2]
        if self.variant == 'ENU':
            return self.origin_offset_vector[2]
        raise ValueError(f'Unknown variant {self.variant}')

    @property
    def ypr(self):
        """Calculate the YPR (Yaw, Pitch, Roll) from the origin rotation.

        This method assumes that the camera is looking down for ypr = (0, 0, 0).

        Returns
        -------
        tuple
            A tuple containing the yaw, pitch, and roll angles.
        """
        return ypr_from_rotation(self.origin_rotation)

    @property
    def ypr_dji(self):
        """Calculate the DJI YPR (Yaw, Pitch, Roll) values.

        DJI YPR values assume that the camera is looking forward for ypr = (0, 0, 0).

        Returns
        -------
        numpy.ndarray
            The YPR values as a numpy array.
        """
        return ypr_from_rotation(
            self.origin_rotation * Rotation.from_euler('ZYX', [0, -90, 0], degrees=True),
        )

    @property
    def wphik(self):
        """Calculate the (Omega, Phi, Kappa) angles from the origin rotation.

        Returns
        -------
        tuple
            A tuple containing the omega, phi, and kappa angles.

        """
        return wphik_from_rotation(self.origin_rotation)


# rotation conversions ######################################


def ypr_from_rotation(rot):
    """Calculate the YPR (Yaw, Pitch, Roll) from a rotation object."""
    return rot.as_euler('ZYX', degrees=True)


def wphik_from_rotation(rot):
    """Calculate the (Omega, Phi, Kappa) angles from a rotation object."""
    return rot.as_euler('XYZ', degrees=True)


def q_wxyz2xyzw(q_wxyz):
    """Convert quaternion from wxyz (JPL) to xyzw (scipy)."""
    return np.array([q_wxyz[1], q_wxyz[2], q_wxyz[3], q_wxyz[0]])


def q_xyzw2wxyz(q_xyzw):
    """Convert quaternion from xyzw (scipy) to wxyz (JPL)."""
    return np.array([q_xyzw[3], q_xyzw[0], q_xyzw[1], q_xyzw[2]])
