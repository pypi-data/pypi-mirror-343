from satcube.cloud_detection import cloud_masking
from satcube.download import download_data



__all__ = ["cloud_masking", "download_data"]

import importlib.metadata
__version__ = importlib.metadata.version("satcube")

