#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 15:57:27 2019

@author: leealex
"""

import numpy as np
import matplotlib.pyplot as plt
import GLMFunctions

dtStim = 0.01
dtSp = 0.001
nkt = 30;
ggsim = GLMFunctions.makeSimStruct_GLM(nkt, dtStim, dtSp)

