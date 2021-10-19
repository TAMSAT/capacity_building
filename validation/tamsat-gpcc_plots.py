#========================================================================#
# This script creates plots that could be used for a simple validation
# report.
#
# In this example, we use TAMSAT and GPCC rainfall data from West Africa
# (northern Ghana/southern Burkina Faso) from 1983-2016.
# (GPCC is a gridded gauge-based data)
#------------------------------------------------------------------------#
# The script does the following:
# 1. Creates a seasonal cycle plot for area-average rainfall from TAMSAT and GPCC
# 2. Creates a scatter plot comparing the July rainfall value
# These next parts are optional!
# 3. Creates a time-series of July rainfall
# 4. Computes some statistics which can help quantify the skill of the TAMSAT data
#
# There are many ways in Python to produce these plots, but this scripts
# provides one way of doing it.
#
# For this practical, we are using Python 3.7. We cannot guarantee this script
# will work if using other versions on Python.
#========================================================================#

#------------------------------------------------------------------------#
# Import modules - these modules are required
#------------------------------------------------------------------------#
import numpy as np
import pandas as pd
import xarray as xr
import os
import scipy.stats
import matplotlib.pyplot as plt
import calendar

#------------------------------------------------------------------------#
# Task 1. Plot seasonal cycle
#------------------------------------------------------------------------#
# Warning! Make sure you are in the same directory as the files.
#------------------------------------------------------------------------#
# Read in rainfall data from CSV file
rainclim = pd.read_csv('monthly_climatology_tamsat-gpcc.csv')

# Plot
plt1 = plt.plot(rainclim.Month, rainclim.TAMSAT, color="blue", linewidth=2.0)
plt2 = plt.plot(rainclim.Month, rainclim.GPCC, color="black", linewidth=2.0)
labels = [calendar.month_abbr[x] for x in rainclim.Month]
plt.xticks(rainclim.Month, labels=labels)
plt.xlabel('Month')
plt.ylabel('Rainfall (mm)')
plt.legend(['TAMSAT', 'GPCC'])
plt.grid()
plt.title('Seasonal-cycle in rainfall over northern Ghana/southern Burkina Faso')
plt.savefig('seasonal-cycle_ghana-burkinafaso_1983-2016.png', bbox_inches='tight', pad_inches=.2, dpi=100)

#------------------------------------------------------------------------#
# Task 2. Plot scatter plot comparing July rainfall values
#------------------------------------------------------------------------#
# Read in rainfall data from CSV file
rain = pd.read_csv('july_rainfall_tamsat-gpcc.csv')

# Plot
plt.figure(figsize=(8, 8))
plt.plot(rain.GPCC, rain.TAMSAT, 'o')
plt.xlim(80, 300)
plt.ylim(80, 300)
plt.plot([0,500],[0,500], color='black')
plt.xlabel("GPCC (mm)")
plt.ylabel("TAMSAT (mm)")
plt.grid()
plt.title('Comparison of rainfall over northern Ghana/southern Burkina Faso \nbetween TAMSAT and GPCC')
plt.savefig('scatter-plot_tamsat-gpcc_ghana-burkinafaso_july_1983-2016.png', bbox_inches='tight', pad_inches=.2, dpi=100)


#------------------------------------------------------------------------#
# (Optional) Task 3. Plot a time-series of the July rainfall values
#------------------------------------------------------------------------#
# This shows the year-to-year variations in rainfall (interannual variability)
#------------------------------------------------------------------------#
years = [x[0:4] for x in rain.Date]
plt.figure(figsize=(15,6))
plt.plot(years, rain.GPCC, color="black")
plt.plot(years, rain.TAMSAT, color="blue")
plt.xticks(years, rotation=45)
plt.xlabel("Year")
plt.ylabel("Rainfall (mm)")
plt.grid()
plt.title('Interannual variability of July rainfall over northern Ghana/southern Burkina Faso')
plt.savefig('interannual-variability_tamsat-gpcc_ghana-burkinafaso_july_1983-2016.png', bbox_inches='tight', pad_inches=.2, dpi=100)


#------------------------------------------------------------------------#
# (Optional) Task 4. Compute rainfall statistics
#------------------------------------------------------------------------#

#------------------------------------------------------------------------#
# Rainfall amount functions for each statistic
#------------------------------------------------------------------------#
# These functions define some widely used statistics which can help
# quantify the skill of satellite rainfall estimates. These functions take
# two arguments: 'obs' is the reference rain gauge data (e.g. GPCC) and
# 'est' is the satellite rainfall estimate (e.g. TAMSAT).
#------------------------------------------------------------------------#
def correlation_func(obs, est):
    """ Return R^2 where est and obs are array-like."""
    
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(est, obs)
    return round(r_value,2)

def bias_func(obs, est):
    """ Return bias where est and obs are array-like."""
    
    return round(np.mean(est - obs),2)

def mae_func(obs, est):
    """ Return MAE where est and obs are array-like."""
    
    return round(np.abs(est - obs).mean(),2)

def rmse_func(obs, est):
    """ Return RMSE where est and obs are array-like."""
    
    return round(np.sqrt(((est - obs) ** 2).mean()),2)


# Using these functions, now compute statistics for July rainfall - here we use
# the object 'rain' which contains all of the July rainfall values
r    = correlation_func(rain.GPCC, rain.TAMSAT)
bias = bias_func(rain.GPCC, rain.TAMSAT)
mae  = mae_func(rain.GPCC, rain.TAMSAT)
rmse = rmse_func(rain.GPCC, rain.TAMSAT)
