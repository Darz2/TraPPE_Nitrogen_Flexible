#!/usr/bin/env python
import os
import numpy as np
import pandas as pd

df = pd.read_csv("av_density.dat",delim_whitespace=True, header=None, skiprows=1)
# print(df.head())
first_column = df.iloc[:, 1]  # `0` refers to the first column
mean = np.mean(first_column)
print(mean)