import functools
import xarray as xr
from importlib_resources import files


@functools.cache
def _read_coeffs(file):
    return xr.open_dataset(files('seuvm._coeffs').joinpath(file))

def get_seuvm_ver0():
    return _read_coeffs('_seuvmv0_coeffs.nc').copy()

def get_seuvm_ver1l():
    return _read_coeffs('_seuvmv1l_coeffs.nc').copy()

def get_seuvm_ver1p():
    return _read_coeffs('_seuvmv1p_coeffs.nc').copy()

def get_seuvm_ver2l():
    return _read_coeffs('_seuvmv2l_coeffs.nc').copy()
