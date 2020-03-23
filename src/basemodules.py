"""
Modules needed for data analysis.
We import them in the top-level cell of all notebooks via `%run src/basemodules.py`.
These modules then become globally available in the notebook.
"""

# Python modules
import copy
import glob
import lmfit
import matplotlib
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import pickle
from scipy import signal
from scipy.interpolate import interp1d
import scipy.constants
from scipy.constants import hbar, pi
import stlabutils
from stlabutils.utils.stlabdict import framearr_to_mtx


# Self-written modules
def S21(w,R1,C1,R2,C2):
    return 1/((1+1j*w*R1*C1)*(1+1j*w*R2*C2))

def S21dB(w,R1,C1,R2,C2):
    return 20*np.log10(np.abs(S21(w,R1,C1,R2,C2)))

def S21ph(w,R1,C1,R2,C2):
    return np.angle(S21(w,R1,C1,R2,C2))


# Plot parameters
plotall = True
overview_plot = True

cmap = matplotlib.cm.get_cmap('PuBu_r')

import seaborn as sns
sns.set()
sns.set_style('white')
sns.set_style('ticks')
plt.style.use('src/my_rcparams.mplstyle')

def cm2inch(*tupl):
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i / inch for i in tupl[0])
    else:
        return tuple(i / inch for i in tupl)


dpi = 1000

# IPython modules
from IPython.display import Image, display

# Path to data
dataHe7 = '/home/jovyan/steelelab/measurement_data/He7/Felix/181217_lowpass_filters/'
dataTriton= '/home/jovyan/steelelab/measurement_data/Triton/Felix/190201_CuPW_filters_RT/'
datamisc = '/home/jovyan/steelelab/projects/Felix/projects/RC-filters/measurement_data/'

# Print file contents
with open('src/basemodules.py') as f:
    print(f.read())
