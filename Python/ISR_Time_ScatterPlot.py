# This script creates a scatter plot of the global mean ISR over time

# Import required packages
import scipy.io.netcdf as sp
import numpy as np
import matplotlib.pyplot as plt

# Open the dataset file
fileObj = sp.NetCDFFile('/Users/maxbesong/Desktop/Research with Python/Data/CERES_EBAF-TOA_Ed4.1_Subset_200003-202011.nc', 'r')

# Make variables to store all the ISR and latitude values
ISR = fileObj.variables['solar_mon'][:]
lat = fileObj.variables['lat'][:]

# Calculate how many full years of data is in the dataset
numYears = ISR.shape[0] // 12

# Create an array that stores a value for each year after 2000, with the year
# 2000 at index 0
years = np.arange(numYears)

# Create an array, with 0s as placeholders, that will be used to store the
# global mean ISR of each year
yearlyGlobalMeanISR = np.zeros(numYears)

# Loop through each year and calculate the global mean ISR during that time
for i in range(numYears):
    # Store 12 months of ISR data
    oneYearISR = ISR[i*12:i*12+12, :, :]
    
    # Average the data at each location across all 12 months
    meanYearISR = oneYearISR.mean(axis=0)
    
    # Average the data all longitude coordinates
    meanYearLonISR = meanYearISR.mean(axis=1)
    
    # Weight the data depending on its latitude coordinates, with data from
    # locations farther from the equator given less weight since it represents
    # a smaller area
    for j in range(lat.shape[0]):
        meanYearLonISR[j] *= np.cos(lat[j] * np.pi/180)
    
    # Average the data across all latitude coordinates
    yearlyGlobalMeanISR[i] = meanYearLonISR.mean(axis=0)

# Calculate the slope, y-intercept, and correlation coefficient of the
# best-fit line through the ISR-vs-time points
m, b = np.polyfit(years, yearlyGlobalMeanISR, 1)
r = np.corrcoef(years, yearlyGlobalMeanISR)[0,1]

# Create a scatter plot of the global mean ISR values over time, and then plot
# the best-fit line through the points
plt.scatter(years, yearlyGlobalMeanISR)
plt.plot(years, m * years + b)

# Adjust the viewing window of the graph, and place a text box containing the
# equation of the best-fit line and value of the correlation coefficient.
# Un-comment the next two lines by deleting the '#'s for this to take effect.
#plt.axis([0, 20, 0, 400])
#plt.text(10, 50, 'ISR = ' + f'{m:.4g}' + '*t + ' + f'{b:.4g}' + '\nr = ' + f'{r:.4g}')

# Add a title and labels to the horizontal and vertical axes. Then adjust how
# many ticks are on the horizontal axis and add gridlines.
plt.title('Global Mean ISR vs Time')
plt.xlabel('Years after 2000')
plt.ylabel('Global Mean ISR (W/m^2)')
plt.locator_params(axis='x', nbins=5)
plt.grid()

# Save a PNG image of the graph to the computer and display it on screen.
plt.savefig('/Users/maxbesong/Desktop/Research with Python/Scripts/ISR_Time_ScatterPlot.png', bbox_inches='tight', dpi=200)
plt.show()