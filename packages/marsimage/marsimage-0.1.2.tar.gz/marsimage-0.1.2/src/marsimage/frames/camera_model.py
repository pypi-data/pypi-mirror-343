"""Module to parse and convert camera models."""

import math
from copy import deepcopy
from dataclasses import dataclass
from typing import Literal

import numpy as np
from scipy.spatial.transform import Rotation

from .coordinate_frames import CoordinateFrame


@dataclass
class CAHVORE:
    """Dataclass that holds the parameters of a CAHVOR(E) camera model."""

    cm_type: Literal['CAHV', 'CAHVOR', 'CAHVORE']
    C: np.ndarray
    A: np.ndarray
    H: np.ndarray
    V: np.ndarray
    coordinate_system_name: str
    coordinate_system_index: int
    reference_coordinate_system_name: str
    reference_coordinate_system_index: int
    O: np.ndarray = None
    R: np.ndarray = None
    E: float = None
    T: float = None
    P: float = None
    variant: Literal['NED', 'ENU'] = 'NED'

    @classmethod
    def from_odl(cls, geometric_camera_model):
        """
        Create a CAHVORE object from an ODL Label GEOMETRIC_CAMERA_MODEL group.

        Parameters
        ----------
        geometric_camera_model : dict
            The GEOMETRIC_CAMERA_MODEL group from the ODL Label.

        Note
        ----
        The dictionary GEOMETRIC_CAMERA_MODEL must at least contain the following keys:

        - MODEL_TYPE
        - MODEL_COMPONENT_1
        - MODEL_COMPONENT_2
        - MODEL_COMPONENT_3
        - MODEL_COMPONENT_4
        - REFERENCE_COORD_SYSTEM_NAME
        - REFERENCE_COORD_SYSTEM_INDEX

        If the MODEL_TYPE is CAHVOR, the dictionary must also contain the following
        keys:

        - MODEL_COMPONENT_5
        - MODEL_COMPONENT_6

        If the MODEL_TYPE is CAHVORE, the dictionary must also contain the following
        keys:

        - MODEL_COMPONENT_7
        - MODEL_COMPONENT_8
        - MODEL_COMPONENT_9

        Returns
        -------
        CAHVORE
            The CAHVORE object.
        """
        # CAHVORE parameters
        cm_type = geometric_camera_model['MODEL_TYPE']
        C = np.array(geometric_camera_model['MODEL_COMPONENT_1'])
        A = np.array(geometric_camera_model['MODEL_COMPONENT_2'])
        H = np.array(geometric_camera_model['MODEL_COMPONENT_3'])
        V = np.array(geometric_camera_model['MODEL_COMPONENT_4'])
        if 'CAHVOR' in cm_type:
            O = np.array(geometric_camera_model['MODEL_COMPONENT_5'])
            R = np.array(geometric_camera_model['MODEL_COMPONENT_6'])
        if cm_type == 'CAHVORE':
            E = geometric_camera_model['MODEL_COMPONENT_7']
            T = geometric_camera_model['MODEL_COMPONENT_8']
            P = geometric_camera_model['MODEL_COMPONENT_9']

        # Coordinate frame
        coordinate_system_name = 'SENSOR'
        coordinate_system_index = 0
        reference_coordinate_system_name = geometric_camera_model['REFERENCE_COORD_SYSTEM_NAME']
        reference_coordinate_system_index = geometric_camera_model['REFERENCE_COORD_SYSTEM_INDEX'][
            :2
        ]  # only return the site and drive
        variant = 'NED'

        return cls(
            cm_type=cm_type,
            C=C,
            A=A,
            H=H,
            V=V,
            coordinate_system_name=coordinate_system_name,
            coordinate_system_index=coordinate_system_index,
            reference_coordinate_system_name=reference_coordinate_system_name,
            reference_coordinate_system_index=reference_coordinate_system_index,
            O=O if 'CAHVOR' in cm_type else None,
            R=R if 'CAHVOR' in cm_type else None,
            E=E if cm_type == 'CAHVORE' else None,
            T=T if cm_type == 'CAHVORE' else None,
            P=P if cm_type == 'CAHVORE' else None,
            variant=variant,
        )

    @classmethod
    def from_json(cls, cahvore_json):
        """.. todo:: Create a CAHVORE object from a public raw image JSON metadata file.

        Create a CAHVORE object from a JSON dictionary containing the metadata.

        :param dict cahvore_json: The CAHVORE JSON dictionary
        :raises NotImplementedError: This method is not yet implemented

        """
        raise NotImplementedError

    # derived properties
    @property
    def hs(self):
        """The hs parameter."""
        return np.linalg.norm(np.cross(self.H, self.A))

    @property
    def vs(self):
        """The vs parameter."""
        return np.linalg.norm(np.cross(self.V, self.A))

    @property
    def hc(self):
        """The hc parameter."""
        return np.dot(self.H, self.A)

    @property
    def vc(self):
        """The vc parameter."""
        return np.dot(self.V, self.A)

    # unit vectors for H and V
    @property
    def H_n(self):
        """The normalized H vector H'."""
        return (self.H - self.hc * self.A) / self.hs

    @property
    def V_n(self):
        """The normalized V vector V'."""
        return (self.V - self.vc * self.A) / self.vs


@dataclass
class CameraModel:
    """Camera model class based on the Photogrammetric camera model."""

    width: int
    height: int
    pixel_size: float
    pixel_size_x: float
    pixel_size_y: float
    f: float
    f_mm: float
    crop_factor: float
    f_35: float
    model_type: str
    x0: float
    y0: float
    x0_mm: float
    y0_mm: float
    cf: CoordinateFrame

    @classmethod
    def from_cahvore(cls, cahvore, width, height, pixel_size):
        """
        Initialize the photogrammetric camera model from a CAHVORE camera model.

        Calculations based on 'CAHVOR camera model and its photogrammetric conversion
        for planetary applications (https://doi.org/10.1029/2003JE002199)'.

        Parameters
        ----------
        cahvore : CAHVORE
            The CAHVORE camera model object.
        width : int
            The image width in pixels.
        height : int
            The image height in pixels.
        pixel_size : float
            The pixel size in mm.

        Returns
        -------
        CameraModel
            The CameraModel object.
        """
        # Intrinsic parameters

        # focal length
        f = cahvore.vs
        f_mm = f * pixel_size
        crop_factor = 43.27 / (math.sqrt(pow(width, 2) + pow(height, 2)) * pixel_size)
        f_35 = f_mm * crop_factor
        pixel_size_y = pixel_size
        pixel_size_x = pixel_size * (cahvore.hs / cahvore.vs)

        model_type = 'fisheye' if cahvore.cm_type == 'CAHVORE' and cahvore.T > 1 else 'perspective'

        # principal point in px
        x0 = cahvore.hc - width / 2
        y0 = height / 2 - cahvore.vc
        x0_mm = x0 * pixel_size
        y0_mm = y0 * pixel_size

        # Extrinsic parameters, a CoordinateFrame object
        cf = CoordinateFrame(
            cahvore.coordinate_system_name,
            cahvore.coordinate_system_index,
            cahvore.C,
            Rotation.from_matrix(np.transpose([-cahvore.V_n, cahvore.H_n, cahvore.A])),
            cahvore.reference_coordinate_system_name,
            cahvore.reference_coordinate_system_index,
            cahvore.variant,
        )

        return cls(
            width,
            height,
            pixel_size,
            pixel_size_x,
            pixel_size_y,
            f,
            f_mm,
            crop_factor,
            f_35,
            model_type,
            x0,
            y0,
            x0_mm,
            y0_mm,
            cf,
        )

    def transform_to(self, target_frame):
        """
        Transform the CameraModel to a specified reference system.

        Parameters
        ----------
        target_frame : CoordinateFrame
            The reference system to transform to.

        Returns
        -------
        CameraModel
            The transformed CameraModel object.
        """
        transformed = deepcopy(self)
        transformed.cf = self.cf.transform_to(target_frame)
        return transformed

    @property
    def ypr(self):
        """Calculate the YPR (Yaw, Pitch, Roll) from the origin rotation.

        This method assumes that the camera is looking down for ypr = (0, 0, 0).

        Returns
        -------
        tuple
            A tuple containing the yaw, pitch, and roll angles.
        """
        return self.cf.ypr

    @property
    def ypr_dji(self):
        """Calculate the DJI YPR (Yaw, Pitch, Roll) values.

        DJI YPR values assume that the camera is looking forward for ypr = (0, 0, 0).

        Returns
        -------
        numpy.ndarray
            The YPR values as a numpy array.
        """
        return self.cf.ypr_dji

    @property
    def cam_heading(self):
        """The compass heading of the camera."""
        return self.ypr[0] % 360

    # @property
    # def cam_elevation(self):
    #     """The pointing elevation of the camera"""
    #     return self.cf.rotation.as_euler("xyz")[1] * 180 / np.pi

    @property
    def planetocentric_latitude(self):
        """The planetocentric latitude of the camera."""
        return self.cf.planetocentric_latitude

    @property
    def planetodetic_latitude(self):
        """The planetodetic latitude of the camera."""
        return self.cf.planetodetic_latitude

    @property
    def longitude(self):
        """The longitude of the camera."""
        return self.cf.longitude

    @property
    def elevation(self):
        """The geographic elevation of the camera."""
        return self.cf.elevation
