# This script creates a global contour map of the trend in ASR values at each
# location

# Import required packages
import scipy.io.netcdf as sp
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cf
from cartopy.util import add_cyclic_point

# Open the dataset file
fileObj = sp.NetCDFFile('/Users/maxbesong/Desktop/Research with Python/Data/CERES_EBAF-TOA_Ed4.1_Subset_200003-202011.nc', 'r')

# Make variables to store all the ISR, RSR, latitude, and longitude values
ISR = fileObj.variables['solar_mon'][:]
RSR = fileObj.variables['toa_sw_all_mon'][:]
lat = fileObj.variables['lat'][:]
lon = fileObj.variables['lon'][:]

# Calculate how many full years of data is in the dataset
numYears = ISR.shape[0] // 12

# Create an array that stores a value for each year after 2000, with the year
# 2000 at index 0
years = np.arange(numYears)

# Calculate the ASR values based on the ISR and RSR
ASR = ISR[:,:,:] - RSR[:,:,:]

# Take a subset of the data in which the extra months at the end that are not
# part of a full year are excluded
fullYearASR = ASR[0:numYears * 12, :, :]

# Create an array, with 0s as placeholders, that will be used to store the
# mean ASR of each year at each location
annualASR = np.zeros((numYears, fullYearASR.shape[1], fullYearASR.shape[2]))

# Loop through each year and calculate the global mean ASR during that time at
# each loaction
for i in range(numYears):
    oneYearASR = ASR[i*12:i*12+12, :, :]
    annualASR[i,:,:] = oneYearASR.mean(axis=0)

# Create an array, with 0s as placeholders, that will be used to store the
# slopes of the trendlines through ASR-vs-time points at each location
slopes = np.zeros((annualASR.shape[1], annualASR.shape[2]))

# Loop through each latitude and longitude location and calculate the slopes
# of the trendlines through ASR-vs-time points at each location
for i in range(slopes.shape[0]):
    for j in range(slopes.shape[1]):
        m, b = np.polyfit(years, annualASR[:,i,j], 1)
        slopes[i,j] = m

# Fix problem with 0 longitude missing data
slopes, lon = add_cyclic_point(slopes, coord=lon)

# Print to the console the miniumum and maximum slope values
print(slopes.min())
print(slopes.max())

# Set up a global map using the Plate Carree projection and add coastlines
axes = plt.axes(projection=ccrs.PlateCarree())
axes.add_feature(cf.COASTLINE, linewidth=0.5)

# Overlay the contours onto the map based on the slopes of the trendlines at
# each location. Include a color bar and add a title
plt.contourf(lon[:], lat[:], slopes[:,:], levels=np.arange(-2, 2.25, 0.25), cmap='bwr')
plt.colorbar(orientation='horizontal')
plt.title('Yearly ASR Trend, Mar 2000 - Feb 2020')

# Save a PNG image of the map to the computer and display it on screen
plt.savefig('/Users/maxbesong/Desktop/Research with Python/Scripts/ASR_Trend_Map.png', bbox_inches='tight', dpi=200)
plt.show()