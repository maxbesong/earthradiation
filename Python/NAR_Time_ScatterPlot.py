# This script creates a scatter plot of the global mean net absorbed radiation
# over time

# Import required packages
import scipy.io.netcdf as sp
import numpy as np
import matplotlib.pyplot as plt

# Open the dataset file
fileObj = sp.NetCDFFile('/Users/maxbesong/Desktop/Research with Python/Data/CERES_EBAF-TOA_Ed4.1_Subset_200003-202011.nc', 'r')

# Make variables to store all the ISR, RSR, OLR, and latitude values
ISR = fileObj.variables['solar_mon'][:]
RSR = fileObj.variables['toa_sw_all_mon'][:]
OLR = fileObj.variables['toa_lw_all_mon'][:]
lat = fileObj.variables['lat'][:]

# Calculate how many full years of data is in the dataset
numYears = ISR.shape[0] // 12

# Create an array that stores a value for each year after 2000, with the year
# 2000 at index 0
years = np.arange(numYears)

# Calculate the ASR based on the ISR and RSR. Then calculate the net absorbed
# radiation (NAR) based on the ASR and OLR
ASR = ISR[:,:,:] - RSR[:,:,:]
NAR = ASR[:,:,:] - OLR[:,:,:]

# Create an array, with 0s as placeholders, that will be used to store the
# global mean NAR of each year
yearlyGlobalMeanNAR = np.zeros(numYears)

# Loop through each year and calculate the global mean NAR during that time
for i in range(numYears):
    # Store 12 months of NAR data
    oneYearNAR = NAR[i*12:i*12+12, :, :]
    
    # Average the data at each location across all 12 months
    meanYearNAR = oneYearNAR.mean(axis=0)
    
     # Average the data all longitude coordinates
    meanYearLonNAR = meanYearNAR.mean(axis=1)
    
    # Weight the data depending on its latitude coordinates, with data from
    # locations farther from the equator given less weight since it represents
    # a smaller area
    for j in range(lat.shape[0]):
        meanYearLonNAR[j] *= np.cos(lat[j] * np.pi/180)
    
    # Average the data across all latitude coordinates
    yearlyGlobalMeanNAR[i] = meanYearLonNAR.mean(axis=0)

# Calculate the slope, y-intercept, and correlation coefficient of the
# best-fit line through the NAR-vs-time points
m, b = np.polyfit(years, yearlyGlobalMeanNAR, 1)
r = np.corrcoef(years, yearlyGlobalMeanNAR)[0,1]

# Create a scatter plot of the global mean ISR values over time, and then plot
# the best-fit line through the points
plt.scatter(years, yearlyGlobalMeanNAR)
plt.plot(years, m * years + b)

# Adjust the viewing window of the graph, and place a text box containing the
# equation of the best-fit line and value of the correlation coefficient.
plt.axis([0, 20, 0, 1.2])
plt.text(11, 0.05, 'NAR = ' + f'{m:.4g}' + '*t + ' + f'{b:.4g}' + '\nr = ' + f'{r:.4g}')

# Add a title and labels to the horizontal and vertical axes. Then adjust how
# many ticks are on the horizontal axis and add gridlines.
plt.title('Global Mean NAR vs Time')
plt.xlabel('Years after 2000')
plt.ylabel('Global Mean NAR (W/m^2)')
plt.locator_params(axis='x', nbins=5)
plt.grid()

# Save a PNG image of the graph to the computer and display it on screen.
plt.savefig('/Users/maxbesong/Desktop/Research with Python/Scripts/NAR_Time_ScatterPlot.png', bbox_inches='tight', dpi=200)
plt.show()