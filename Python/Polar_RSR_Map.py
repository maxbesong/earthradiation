# This script creates a polar contour map of the mean RSR values at each
# location in the Northern Hemisphere

# Import required packages
import scipy.io.netcdf as sp
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cf
from cartopy.util import add_cyclic_point

# Open the dataset file
fileObj = sp.NetCDFFile('/Users/maxbesong/Desktop/Research with Python/Data/CERES_EBAF-TOA_Ed4.1_Subset_200003-202011.nc', 'r')

# Make variables to store all the RSR, latitude, and longitude values
RSR = fileObj.variables['toa_sw_all_mon'][:]
lat = fileObj.variables['lat'][:]
lon = fileObj.variables['lon'][:]

# Calculate how many full years of data is in the dataset
numYears = RSR.shape[0] // 12

# Take a subset of the data in which the extra months at the end that are not
# part of a full year are excluded
fullYearRSR = RSR[0:numYears * 12, :, :]

# Average the data at each location across all months
means = fullYearRSR.mean(axis=0)

# Fix problem with 0 longitude missing data
means, lon = add_cyclic_point(means, coord=lon)

# Set up a polar map and add coastlines
axes = plt.axes(projection=ccrs.NearsidePerspective(central_longitude=0, central_latitude=90, satellite_height=357858310))
axes.add_feature(cf.COASTLINE, linewidth=0.5)
axes.set_global()

# Overlay the contours onto the map based on the mean RSR values at each
# location. Include a color bar and add a title
plt.contourf(lon[:], lat[:], means[:,:], levels=12, cmap='bone', transform=ccrs.PlateCarree())
plt.colorbar(orientation='horizontal')

# Save a PNG image of the map to the computer and display it on screen
plt.title('Mean RSR, Mar 2000 - Feb 2020')
plt.savefig('/Users/maxbesong/Desktop/Research with Python/Scripts/Polar_RSR_Map.png', bbox_inches='tight', dpi=200)
plt.show()

# projection options: https://scitools.org.uk/cartopy/docs/latest/crs/projections.html
# cmap options: https://matplotlib.org/stable/tutorials/colors/colormaps.html