"""Various utility functions for writing metadata."""

import struct


class XMP:
    """Create an XMP metadata string for a MarsImage.

    Parameters
    ----------
    marsimage : MarsImage
        The MarsImage object to create the XMP metadata for.
    """

    def __init__(self, marsimage):
        try:
            self.xmp = (
                """<?xpacket id='W5M0MpCehiHzreSzNTczkc9d'?>
<x:xmpmeta xmlns:x='adobe:ns:meta/'>
 <rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>
  <rdf:Description rdf:about="Marsimage Meta Data"
    xmlns:tiff="http://ns.adobe.com/tiff/1.0/"
    xmlns:exif="http://ns.adobe.com/exif/1.0/"
    xmlns:xmp="http://ns.adobe.com/xap/1.0/"
    xmlns:xmpMM="http://ns.adobe.com/xap/1.0/mm/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:crs="http://ns.adobe.com/camera-raw-settings/1.0/"
    xmlns:drone-dji="http://www.dji.com/drone-dji/1.0/"
    xmlns:camera='http://pix4d.com/camera/1.0'>
   <camera:GPSXYAccuracy>0.5</camera:GPSXYAccuracy>
   <camera:GPSZAccuracy>1.0</camera:GPSZAccuracy>
   <camera:GyroRate>0.0</camera:GyroRate>
   <camera:IMUPitchAccuracy>3.0</camera:IMUPitchAccuracy>
   <camera:IMURollAccuracy>3.0</camera:IMURollAccuracy>
   <camera:IMUYawAccuracy>3.0</camera:IMUYawAccuracy>
   <camera:Yaw>"""
                + str(marsimage.cm_global.cf.ypr[0])
                + """</camera:Yaw>
   <camera:Pitch>"""
                + str(marsimage.cm_global.cf.ypr[1])
                + """</camera:Pitch>
   <camera:Roll>"""
                + str(marsimage.cm_global.cf.ypr[2])
                + """</camera:Roll>
   <camera:ModelType>"""
                + str(marsimage.cm_global.model_type)
                + """</camera:ModelType>
   <drone-dji:FlightYawDegree>"""
                + str(marsimage.localization.ypr[0])
                + """</drone-dji:FlightYawDegree>
   <drone-dji:FlightPitchDegree>"""
                + str(marsimage.localization.ypr[1])
                + """</drone-dji:FlightPitchDegree>
   <drone-dji:FlightRollDegree>"""
                + str(marsimage.localization.ypr[2])
                + """</drone-dji:FlightRollDegree>
   <drone-dji:GimbalYawDegree>"""
                + str(marsimage.cm_global.cf.ypr_dji[0])
                + """</drone-dji:GimbalYawDegree>
   <drone-dji:GimbalPitchDegree>"""
                + str(marsimage.cm_global.cf.ypr_dji[1])
                + """</drone-dji:GimbalPitchDegree>
   <drone-dji:GimbalRollDegree>"""
                + str(marsimage.cm_global.cf.ypr_dji[2])
                + """</drone-dji:GimbalRollDegree>
   <drone-dji:GimbalReverse>0</drone-dji:GimbalReverse>
   <exif:GPSAltitude>"""
                + str(abs(marsimage.cm_global.elevation))
                + """</exif:GPSAltitude>
   <exif:GPSAltitudeRef>"""
                + ('1' if marsimage.cm_global.elevation < 0 else '0')
                + """</exif:GPSAltitudeRef>
   <exif:GPSLatitude>"""
                + str(marsimage.cm_global.planetocentric_latitude)
                + """N</exif:GPSLatitude>
   <exif:GPSLongitude>"""
                + str(marsimage.cm_global.longitude)
                + """E</exif:GPSLongitude>
   <exif:GPSVersionID>2.3.0.0</exif:GPSVersionID>
   <dc:description>
   <rdf:Alt>
   <rdf:li xml:lang="x-default">"""
                + 'LMST: '
                + str(marsimage.mean_solar_time)
                + ' | Sun: Az: '
                + str(round(marsimage.solar_azimuth, 1))
                + ' deg, El: '
                + str(round(marsimage.solar_elevation, 1))
                + ' deg | '
                + marsimage.rationale
                + """</rdf:li>
   </rdf:Alt>
   </dc:description>
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>
<?xpacket end='w'?>"""
            )
        except ValueError as e:
            raise ValueError('Error creating XMP metadata') from e

    def write_xmp(self, filename):
        """Write the XMP metadata to a file.

        Parameters
        ----------
        filename : str | Path
            The path to save the XMP metadata to.
        """
        with open(filename, 'wb') as f:
            f.write(self.xmp.encode('utf-8'))

    @property
    def tag(self):
        """Return the XMP metadata as a TIFF tag."""
        # Convert XMP data to a byte string
        xmp_data_bytes = self.xmp.encode('utf-8')

        # Set XMP data as the value for TIFF tag 700
        return struct.pack(f'{len(xmp_data_bytes)}s', xmp_data_bytes)


class PP3:
    """Create a RawTherapee pp3 file string.

    Parameters
    ----------
    baseline_exposure_stops : float
        The baseline exposure in stops to be applied in RawTherapee.
    pixel_averaging : int
        The downsampling factor that was applied to the image
        and should be considered in sharpening. (prevents oversharpening)
    """

    def __init__(self, baseline_exposure_stops, pixel_averaging):
        """Generate a RawTherapee pp3 file string."""
        # use PreExposure for baseline exposure if 0.1 < baseline_exposure factor < 16
        if 0.1 < 2**baseline_exposure_stops < 16:
            pre_exposure = str(round(2**baseline_exposure_stops, 4))
            compensation = '0'
        else:
            pre_exposure = '1.0'
            compensation = str(round(baseline_exposure_stops, 4))

        # sharpen image less if pixel averaging is used
        deconv_radius = str(0.55 / pixel_averaging)
        self.pp3 = (
            """
    [Exposure]
    Auto=false
    Compensation="""
            + compensation
            + """
    HistogramMatching=false
    CurveMode=FilmLike
    Curve=1;0;0;0.11;0.089999999999999997;0.34465753424657541;0.42178082191780825;0.69835616438356152;0.83164383561643851;1;1;

    [HLRecovery]
    Enabled=true
    Method=Coloropp

    [LensProfile]
    LcMode=none
    UseDistortion=true
    UseVignette=true
    UseCA=false

    [PostDemosaicSharpening]
    Enabled=true
    Contrast=21
    AutoContrast=false
    AutoRadius=false
    DeconvRadius="""
            + deconv_radius
            + """
    DeconvRadiusOffset=0
    DeconvIterCheck=true
    DeconvIterations=20

    [Color Management]
    ToneCurve=false
    ApplyLookTable=true
    ApplyBaselineExposureOffset=true
    ApplyHueSatMap=true
    DCPIlluminant=0

    [RAW]
    CA=false
    CAAvoidColourshift=true
    CAAutoIterations=2
    HotPixelFilter=true
    DeadPixelFilter=false
    HotDeadPixelThresh=100
    PreExposure= """
            + pre_exposure
            + """

    [RAW Bayer]
    Method=amaze
    LMMSEIterations=2
    Border=0
    PreTwoGreen=true
    LineDenoise=0
    LineDenoiseDirection=3
    GreenEqThreshold=0

    [MetaData]
    Mode=1
    ExifKeys=Exif.Image.Artist;Exif.Image.Copyright;Exif.Image.ImageDescription;Exif.Image.Make;Exif.Image.Model;Exif.Image.XResolution;Exif.Image.YResolution;Exif.Photo.DateTimeOriginal;Exif.Photo.ExposureBiasValue;Exif.Photo.ExposureTime;Exif.Photo.FNumber;Exif.Photo.Flash;Exif.Photo.FocalLength;Exif.Photo.FocalPlaneResolutionUnit;Exif.Photo.FocalPlaneXResolution;Exif.Photo.FocalPlaneYResolution;Exif.Photo.FocalLengthIn35mmFilm;Exif.Photo.ISOSpeedRatings;Exif.Photo.LensModel;Exif.Photo.UserComment;

    [RAW Preprocess WB]
    Mode=1
    """
        )

    def write(self, filename):
        """Write the pp3 metadata to a file."""
        with open(filename, 'wb') as f:
            f.write(self.pp3.encode('utf-8'))
