"""Filename parser for Marsrover filenames."""

from pathlib import Path


class _FilenameBase:
    """Parser class for filenames."""

    pattern: str = ''
    keys: dict = {}

    def __init__(self, filename):
        for c, p in zip(filename, self.pattern, strict=False):
            if key := self.keys.get(p):
                setattr(self, key, getattr(self, key, '') + c)


class MSLSingleFilename(_FilenameBase):
    """MSL EDR and single frame RDR filename class.

    See MSL Camera & LIBS EDR / RDR Data Products SIS (https://planetarydata.jpl.nasa.gov/img/data/msl/MSLHAZ_0XXX/DOCUMENT/MSL_CAMERA_SIS_latest.PDF, Page 88)
    """

    #          NLB_668441715RAD_F0870792NCAM00252M1.IMG"""
    pattern = 'aabcdddddddddeeefghhhiiiijjjjjjjjjkl.mmm'

    keys = {
        'a': 'inst',  # instrument
        'b': 'config',  # configuration (Computer A or B)
        'c': 'spec',  # special processing flag
        'd': 'sclk',  # spacecraft clock count
        'e': 'prodid',  # product ID (e.g. ECM, RAD,..)
        'f': 'geom',  # geometry (_ for raw geometry, L for liniearized)
        'g': 'samp',  # sample type (F for full, S for subframe, D for downsampled, T for thumbnail, etc.)
        'h': 'site',  # site ID
        'i': 'drive',  # drive ID
        'j': 'seqid',  # sequence ID
        'k': 'venue',  # venue/producer ID
        'l': 'ver',  # version number, 1-9, A-Z, _ (36+)
        'm': 'ext',  # extension
    }

    def __init__(self, filename):
        filename = filename.upper()
        super().__init__(filename)
        self.prod_level = 'EDR' if self.prodid[0] in {'E', 'N'} else 'RDR'
        self.prod_code = self.prodid + self.geom
        self.is_thumbnail = self.samp == 'T'
        _quality = {
            'F': 10,  # Full frame raster data, full resolution
            'S': 9,  # Subframed raster data, full resolution
            'D': 5,  # Downsampled raster data, reduced resolution
            'M': 6,  # Mixed (Subframe and Downsampled) raster data, mixed resolution
            'T': 1,  # Thumbnail raster data, reduced resolution
            'B': 4,  # Bayer extraction subsampling (MMM only) raster data
            'Y': 0.9,  # Thumbnail Bayer extraction subsampling (MMM only) raster data
            'N': 3,  # Non-raster data
        }  # Quality factor for compression
        self._desirability = (
            _quality.get(self.samp, 0) * int(self.ver)
        )  # desirability tries to measure the quality of the product in case multiple versions are available
        self._observation = (
            self.inst + self.config + self.sclk + self.geom + self.site + self.drive + self.seqid
        ).upper()
        self._product = (
            self.inst
            + self.config
            + self.sclk
            + self.prodid
            + self.geom
            + self.site
            + self.drive
            + self.seqid
        ).upper()  # unique identifier for a product variant
        self.product_id = Path(filename).stem.upper()
        self.version = self.ver


class MSLMMMFilename(_FilenameBase):
    """MMM filename class.

    See https://doi.org/10.1002/2016EA000219 and
    https://planetarydata.jpl.nasa.gov/img/data/msl/msl_mmm/document/MSL_MMM_DPSIS.PDF (Page 25)
    """

    #          3060ML0159860360308509C00_DRXX.IMG"""
    pattern = 'ssssiifffffflllxxcccccpgv_dddd.zzz'

    keys = {
        's': 'sol',  # sol
        'i': 'inst',  # instrument
        'f': 'seqid',  # sequence ID
        'l': 'cmd_nr',  # command number in sequence
        'x': 'cdpid_counter',  # Camera Data Product Identifier (CDPID) counter that records the number of times this CDPID has been used over the lifetime of the mission
        'c': 'cdpid',  # CDPID value
        'p': 'prod_type',  # product type, compression type etc. See https://planetarydata.jpl.nasa.gov/img/data/msl/msl_mmm/document/MSL_MMM_DPSIS.PDF (Page 25)
        'g': 'gop',  # group of pictures hex counter
        'v': 'ver',  # version
        'd': 'processing_code',  # processing code (e.g. DRXX, DXXX, DRCX, etc.) See https://planetarydata.jpl.nasa.gov/img/data/msl/msl_mmm/document/MSL_MMM_DPSIS.PDF (Page 25)
        'z': 'ext',  # extension
    }

    def __init__(self, filename):
        filename = filename.upper()
        super().__init__(filename)
        self.prod_level = 'EDR' if self.processing_code == 'XXXX' else 'RDR'
        self.prod_code = self.processing_code
        self.is_thumbnail = self.prod_type in {'G', 'H', 'I', 'O', 'P', 'Q', 'T', 'U'}
        _quality = {
            'A': 10,  # Raster 16 bit image
            'B': 9,  # Raster 8 bit image
            'C': 8,  # Losslessly compressed raster 8 bit
            'D': 4,  # JPEG grayscale image
            'E': 5,  # JPEG 422 image
            'F': 6,  # JPEG 444 image
            'G': 1,  # Raster 8 bit thumbnail
            'H': 0.8,  # JPEG grayscale thumbnail
            'I': 0.6,  # JPEG 444 thumbnail
            'J': 8.9,  # Raster 8 bit video
            'K': 7.9,  # Losslessly compressed raster 8 bit
            'L': 3.9,  # JPEG grayscale video
            'M': 4.9,  # JPEG 422 video
            'N': 5.9,  # JPEG 444 video
            'O': 0.9,  # Raster 8 bit video thumbnail
            'P': 0.8,  # JPEG grayscale video thumbnail
            'Q': 0.7,  # JPEG 444 video thumbnail
            'R': 6.1,  # JPEG 444 focus merge image
            'S': 6.0,  # JPEG grayscale range map image
            'T': 0.3,  # JPEG 444 focus merge thumbnail
            'U': 0.2,  # JPEG grayscale range map thumbnail
        }  # Quality factor for compression
        self._desirability = _quality.get(
            self.prod_type, 0
        )  # desirability tries to measure the quality of the product in case multiple versions are available
        self._observation = (
            self.sol
            + self.inst
            + self.seqid
            + self.cmd_nr
            + self.cdpid_counter
            + self.cdpid
            + self.gop
        )
        self._product = (
            self.sol
            + self.inst
            + self.seqid
            + self.cmd_nr
            + self.cdpid_counter
            + self.cdpid
            + self.gop
            + self.processing_code
        )  # unique identifier for a product variant
        self.product_id = Path(filename).stem
        self.version = self.ver


class MSLMMMFilenameReprocessed(_FilenameBase):
    """MMM filename class.

    See https://doi.org/10.1002/2016EA000219 and
    https://planetarydata.jpl.nasa.gov/img/data/msl/msl_mmm/document/MSL_MMM_DPSIS.PDF (Page 25)
    """

    #          3060ML0159860360308509C00_DRXX_1.1.IMG"""
    pattern = 'ssssiifffffflllxxcccccpgv_dddd_www.zzz'

    keys = {
        's': 'sol',  # sol
        'i': 'inst',  # instrument
        'f': 'seqid',  # sequence ID
        'l': 'cmd_nr',  # command number in sequence
        'x': 'cdpid_counter',  # Camera Data Product Identifier (CDPID) counter that records the number of times this CDPID has been used over the lifetime of the mission
        'c': 'cdpid',  # CDPID value
        'p': 'prod_type',  # product type, compression type etc. See https://planetarydata.jpl.nasa.gov/img/data/msl/msl_mmm/document/MSL_MMM_DPSIS.PDF (Page 25)
        'g': 'gop',  # group of pictures hex counter
        'v': 'ver',  # version
        'd': 'processing_code',  # processing code (e.g. DRXX, DXXX, DRCX, etc.) See https://planetarydata.jpl.nasa.gov/img/data/msl/msl_mmm/document/MSL_MMM_DPSIS.PDF (Page 25)
        'w': 'ver2',  # version
        'z': 'ext',  # extension
    }

    def __init__(self, filename):
        filename = filename.upper()
        super().__init__(filename)
        self.prod_level = 'EDR' if self.processing_code == 'XXXX' else 'RDR'
        self.prod_code = self.processing_code
        self.is_thumbnail = self.prod_type in {'G', 'H', 'I', 'O', 'P', 'Q', 'T', 'U'}
        _quality = {
            'A': 10,  # Raster 16 bit image
            'B': 9,  # Raster 8 bit image
            'C': 8,  # Losslessly compressed raster 8 bit
            'D': 4,  # JPEG grayscale image
            'E': 5,  # JPEG 422 image
            'F': 6,  # JPEG 444 image
            'G': 1,  # Raster 8 bit thumbnail
            'H': 0.8,  # JPEG grayscale thumbnail
            'I': 0.6,  # JPEG 444 thumbnail
            'J': 8.9,  # Raster 8 bit video
            'K': 7.9,  # Losslessly compressed raster 8 bit
            'L': 3.9,  # JPEG grayscale video
            'M': 4.9,  # JPEG 422 video
            'N': 5.9,  # JPEG 444 video
            'O': 0.9,  # Raster 8 bit video thumbnail
            'P': 0.8,  # JPEG grayscale video thumbnail
            'Q': 0.7,  # JPEG 444 video thumbnail
            'R': 6.1,  # JPEG 444 focus merge image
            'S': 6.0,  # JPEG grayscale range map image
            'T': 0.3,  # JPEG 444 focus merge thumbnail
            'U': 0.2,  # JPEG grayscale range map thumbnail
        }  # Quality factor for compression
        self._desirability = (
            _quality.get(self.prod_type, 0) * (float(self.ver2) + 1.1)
        )  # desirability tries to measure the quality of the product in case multiple versions are available
        self._observation = (
            self.sol
            + self.inst
            + self.seqid
            + self.cmd_nr
            + self.cdpid_counter
            + self.cdpid
            + self.gop
        )  # unique identifier for a physical observation
        self._product = (
            self.sol
            + self.inst
            + self.seqid
            + self.cmd_nr
            + self.cdpid_counter
            + self.cdpid
            + self.gop
            + self.processing_code
        )  # unique identifier for a product variant
        self.product_id = Path(filename).stem
        self.version = self.ver2


class Filename:
    """General filename parser for Marsrover filenames.

    Currently capable of parsing MSL EDR and MMM filenames.

    Parameters
    ----------
    filename : str
        The filename to parse.

    Attributes
    ----------
    prod_level : str
        The product level (EDR or RDR).
    is_thumbnail : bool
        True if the product is a thumbnail.
    observation : str
        A unique identifier for the observation regardless of compression or processing.

    See Also
    --------
    MSLSingleFilename : MSL EDR and single frame RDR filename class.
    MSLMMMFilename : MMM filename class.

    Returns
    -------
    obj
        The parsed filename object. Parts of the filename can be accessed as attributes.
    """

    def __new__(cls, filename):  # noqa: D102
        fname = Path(filename)
        stem = fname.stem
        if len(stem) == 36:
            return MSLSingleFilename(fname.name)
        if len(stem) == 30:
            return MSLMMMFilename(fname.name)
        if len(stem) == 34:
            return MSLMMMFilenameReprocessed(fname.name)
        raise ValueError(f'Unknown filename format: {filename}')
