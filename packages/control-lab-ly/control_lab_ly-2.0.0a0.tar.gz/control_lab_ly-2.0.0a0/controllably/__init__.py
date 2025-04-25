"""
.. include:: ../docs/README.md
.. include:: ../docs/CHANGELOG.md
"""
from .core import init, start_logging

import sys
import os
external_libs = os.path.join(os.path.dirname(__file__), 'external')
sys.path.insert(0, external_libs)

import numpy as np
np.set_printoptions(legacy='1.21')