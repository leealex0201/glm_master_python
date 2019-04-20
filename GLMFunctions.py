#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 16:26:08 2019

@author: leealex
"""

import matplotlib.pyplot as plt
import numpy.matlib
import numpy as np
from scipy import special, optimize, signal, sparse
import warnings
import sys

def makeSimStruct_GLM(nkt, dtStim, dtSp):
#==============================================================================
#      Creates a list with default parameters for a GLM model
#      Input: nkt = number of time bins for stimulus filter
#             dtStim = bin size for sampling of stimulus kernel in sec
#             dtSp = bin size for sampling post-spike kernel in sec
#     
#      Output: (list)
#              filt - stimulus filter
#              nlfun - nonlinearity (exponential by default)
#              dc - dc input to cell
#              ih - post-spike current
#              ihbas - basis for post-spike current
#              iht - time lattice for post-spike current
#              dtsim - default time bin size for simulation
#              ihbasprs - basis for post-spike current
#==============================================================================
    
    # Check that spike bin size evenly divides stimulus bin size
    if (np.round(dtStim % dtSp) != 0):
        print('makeSimStruct_GLM: dtSp doesn''t evenly divide dtStim: rounding dtSp to nearest even divisor')
        dtSp = dtStim/np.round(dtStim/dtSp)
        print('dtSp reset to', dtSp)
        
    # Create a default (temporal) stimulus filter
    tk = np.arange(nkt)
    b1 = float(nkt)/32
    b2 = float(nkt)/16
    k1 = (1/(special.gamma(6.0)*b1)*(tk/b1)**5)*np.exp(-tk/b1)
    k2 = (1/(special.gamma(6.0)*b2)*(tk/b2)**5)*np.exp(-tk/b2)
    k = np.flipud(k1-k2/1.5)
    k = k/np.linalg.norm(k)/2;
    
    # Represent this filter (approximately) in temporal basis
    ktbasprs = {}
    ktbasprs['neye'] = np.minimum(5, nkt) # Number of "identity" basis vectors near time of spike
    ktbasprs['ncos'] = np.minimum(5, nkt) # Number of raised-cosine vectors to use
    ktbasprs['kpeaks'] = np.array([0,((nkt-ktbasprs['neye'])/2.0)]) # Position of 1st and last bump
    ktbasprs['b'] = 1.0 # Offset of nonlinear scailing (larger -> more linear)
    ktbas, _ = makeBasis_StimKernel(ktbasprs,nkt)
    
    return 0

def makeBasis_StimKernel(ktbasprs, nkt):
#==============================================================================
#     Generates a basis consisting of raised cosines and several columns of
#     identity matrix vectors for temporal structure of stimulus kernel
#
#     Args: kbasprs = dictionary with fields:
#               neye = number of identity basis vectors at front
#               ncos = # of vectors that are raised cosines
#               kpeaks = 2-vector, with peak position of 1st and last vector,
#                   relative to start of cosine basis vectors (e.g. [0 10])
#               b = offset for nonlinear scaling. larger values -> more linear
#                   scaling of vectors. bk must be >= 0
#           nkt = number of time samples in basis (optional)
#
#     Output:
#           kbasorth = orthogonal basis
#           kbasis = standard raised cosine (non-orthogonal) basis
#==============================================================================
    neye = ktbasprs['neye']
    ncos = ktbasprs['ncos']
    kpeaks = ktbasprs['kpeaks']
    b = ktbasprs['b']
    return 0