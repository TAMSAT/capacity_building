#========================================================================#
# This script creates plots that could be used to create an end of season
# rainfall monitoring bulletin using TAMSAT data.
#
# In this example, we use rainfall data for Zambia during the 2017-2018
# rainy season.
#------------------------------------------------------------------------#
# The script does the following:
# 1. Creates a time-series plot for area-average rainfall amount and
#    rainfall anomaly (averaged over Zambia)
# 2. Creates a rainfal maps for rainfal amount and rainfall anomaly
# 3. Creates a cumulative rainfall time-series plot for area-average
#    rainfal amount and rainfall anomaly (averaged over Zambia)
#
# There are many ways in Python to produce these plots, but this scripts
# provides one way of doing it.
#
# For this practical, we are using Python 3.7. We cannot guarantee this script
# will work if using other versions on Python.
#========================================================================#

#------------------------------------------------------------------------#
# Import modules - these modules are required
# Some of these modules may need to be installed, such as xarray
#------------------------------------------------------------------------#
import numpy as np
import pandas as pd
import xarray as xr
import os
import matplotlib.pyplot as plt
import seaborn as sns
import cartopy
import cartopy.io.shapereader as shpreader
import cartopy.crs as ccrs
import cartopy as car
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER


#------------------------------------------------------------------------#
# Task 1. Create rainfall time-series
#------------------------------------------------------------------------#
# Warning! Make sure you are in the same directory as the files.
#------------------------------------------------------------------------#
# Read in rainfall amount and rainfall anomaly CSV files
rain     = pd.read_csv('data/02-tamsatPentadal.v3.1-1506812400-1525129200_zam.csv', index_col=0, parse_dates=True)
rainanom = pd.read_csv('data/02a-tamsatPentadalAnomalies.v3.1-1506812400-1525129200_zam.csv', index_col=0, parse_dates=True)

# Plot rainfall amount time-series
sns.set(rc={'figure.figsize':(8, 4)})
rain['rfe'].plot(linewidth=3, color='blue', label='rainfall amount')
rainanom['rfe'].plot(linewidth=3, color='grey', linestyle='--', label='rainfall anomaly')
plt.xlabel('Date')
plt.ylabel('Rainfall (mm)')
plt.axhline(y=0, color='black', linestyle='-')
plt.title('Pentadal rainfall during rainy season')
plt.legend()
plt.savefig('zambia_2017-2018_rain_timeseries.png', bbox_inches='tight', pad_inches=.2, dpi=100)
plt.close()


#------------------------------------------------------------------------#
# Task 2. Create rainfall maps
#------------------------------------------------------------------------#
# Note that when extracting these files from the TAMSAT website, rather than choosing
# Zambia from the drop down list, instead the domain W=21.8, N=-8.0, S=-18.3, E=34.0
# was entered - this allows us to get estimates outside of Zambia but within this
# rectangular domain. You can select Zambia from the drop down list of countries,
# but this will only give you estimates within the Zambia border.
#------------------------------------------------------------------------#
# Read in netCDF file for rainfall amount and rainfall anomaly
rain_nc     = xr.open_dataset('data/04-tamsatMonthly.v3.1-1506812400-1525129200_21.8_34.0_-18.3_-8.0.nc')
rainanom_nc = xr.open_dataset('data/04a-tamsatMonthlyAnomalies.v3.1-1506812400-1525129200_21.8_34.0_-18.3_-8.0.nc')

# Sum each month in file to get season total
rain_sum_nc     = rain_nc.sum(dim='time')
rainanom_sum_nc = rainanom_nc.sum(dim='time')

# Plot map of rainfall amount
fig, ax = plt.subplots(1, 1, figsize=(10, 8), subplot_kw=dict(projection=ccrs.PlateCarree()))
ax.coastlines(resolution='50m')
gl = ax.gridlines(color='gray', draw_labels=False)
gl.xlabels_bottom = gl.ylabels_left = True
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
cs = ax.contourf(rain_sum_nc.lon.values, rain_sum_nc.lat.values, rain_sum_nc.rfe_filled.values, cmap='jet_r')
cbar = fig.colorbar(cs, shrink=0.5, orientation='horizontal', ax=ax, pad=0.1)
cbar.set_label('(mm)', size=10)
ax.add_feature(car.feature.BORDERS)
ax.set_ylabel('Latitude')
ax.set_xlabel('Longitude')
ax.set_title('Seasonal rainfall total')
plt.savefig('zambia_2017-2018_totalrain-amount_map.png', bbox_inches='tight', pad_inches=.2, dpi=100)
plt.close()

# Plot map of rainfall anomaly
fig, ax1 = plt.subplots(1, 1, figsize=(10, 8), subplot_kw=dict(projection=ccrs.PlateCarree()))
ax1.coastlines(resolution='50m')
gl = ax1.gridlines(color='gray', draw_labels=False)
gl.xlabels_bottom = gl.ylabels_left = True
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
cs = ax1.contourf(rainanom_sum_nc.lon.values, rainanom_sum_nc.lat.values, rainanom_sum_nc.rfe_filled.values, cmap='RdBu', vmin=-400, vmax=400)
cbar = fig.colorbar(cs, shrink=0.5, orientation='horizontal', ax=ax1, pad=0.1)
cbar.set_label('(mm)', size=10)
ax1.add_feature(car.feature.BORDERS)
ax1.set_ylabel('Latitude')
ax1.set_xlabel('Longitude')
ax.set_title('Seasonal rainfall-anomaly')
plt.savefig('zambia_2017-2018_totalrain-anom_map.png', bbox_inches='tight', pad_inches=.2, dpi=100)
plt.close()


#------------------------------------------------------------------------#
# Task 3. Create a cumulative rainfall time-series
#------------------------------------------------------------------------#
# For this, you can use the rain and rainanom variables from Task 1 above
#------------------------------------------------------------------------#
# Compute cumulative sum throughout rainy season
rain_cumsum     = rain.cumsum()
rainanom_cumsum = rainanom.cumsum()

# Plot rainfall amount time-series
sns.set(rc={'figure.figsize':(8, 4)})
rain_cumsum['rfe'].plot(linewidth=3, color='blue', label='rainfall amount')
rainanom_cumsum['rfe'].plot(linewidth=3, color='grey', linestyle='--', label='rainfall anomaly')
plt.xlabel('Date')
plt.ylabel('Rainfall (mm)')
plt.axhline(y=0, color='black', linestyle='-')
plt.title('Cumulative rainfall during rainy season')
plt.legend()
plt.savefig('zambia_2017-2018_cumsum_rain_timeseries.png', bbox_inches='tight', pad_inches=.2, dpi=100)
plt.close()
