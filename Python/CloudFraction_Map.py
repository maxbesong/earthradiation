# This script creates a global contour map of the mean cloud fraction values
# at each location

# Import required packages
import scipy.io.netcdf as sp
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cf
from cartopy.util import add_cyclic_point

# Open the dataset file
fileObj = sp.NetCDFFile('/Users/maxbesong/Desktop/Research with Python/Data/CERES_EBAF-TOA_Ed4.1_Subset_200003-202011.nc', 'r')

# Make variables to store all the cloud fraction, latitude, and longitude
# values
cloudFrac = fileObj.variables['cldarea_total_daynight_mon'][:]
lat = fileObj.variables['lat'][:]
lon = fileObj.variables['lon'][:]

# Calculate how many full years of data is in the dataset
numYears = cloudFrac.shape[0] // 12

# Take a subset of the data in which the extra months at the end that are not
# part of a full year are excluded
fullYearCloudFrac = cloudFrac[0:numYears * 12, :, :]

# Average the data at each location across all months
means = fullYearCloudFrac.mean(axis=0)

# Fix problem with 0 longitude missing data
means, lon = add_cyclic_point(means, coord=lon)

# Set up a global map using the Plate Carree projection and add coastlines
axes = plt.axes(projection=ccrs.PlateCarree())
axes.add_feature(cf.COASTLINE, linewidth=0.5)

# Overlay the contours onto the map based on the mean cloud fraction values at
# each location. Include a color bar and add a title
plt.contourf(lon[:], lat[:], means[:,:], levels=12, cmap='bone')
plt.colorbar(orientation='horizontal')
plt.title('Mean Cloud Fraction, Mar 2000 - Feb 2020')

# Save a PNG image of the map to the computer and display it on screen
plt.savefig('/Users/maxbesong/Desktop/Research with Python/Scripts/CloudFraction_Map.png', bbox_inches='tight', dpi=200)
plt.show()

# projection options: https://scitools.org.uk/cartopy/docs/latest/crs/projections.html
# cmap options: https://matplotlib.org/stable/tutorials/colors/colormaps.html