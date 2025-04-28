# -*- coding: utf-8 -*-
""" Python bindings for exactextract """


# start delvewheel patch
def _delvewheel_patch_1_10_1():
    import os
    if os.path.isdir(libs_dir := os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'exactextract.libs'))):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_10_1()
del _delvewheel_patch_1_10_1
# end delvewheel patch

from ._exactextract import __version__
from .exact_extract import exact_extract
from .feature import Feature, FeatureSource
from .operation import Operation
from .processor import Processor
from .raster import RasterSource
from .writer import Writer