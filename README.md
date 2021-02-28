This contains all the example NCL and Python code I have used for the research project on incoming and outgoing radiation on Earth. It also has a folders containing output files obtained from running the scripts.

Some notes:

For scripts in the NCL directory, you might need to change the file extensions rom ".txt" to ".ncl". On the cluster, it did not matter since we had to copy and paste this code into a text box in the browser, though you might need the ncl extension depending on how you are planning to run it. In each script, you will need to update the file name and path in the addFile() function (usually found near the top of each script) so it can find the data set you downloaded. Aside from that, the scripts should work fine with the new data sets aside from only running through the years available in the older data sets I was using. I can help you update a few numbers in the scripts to work with the most recent data set you downloaded.

Likewise, in the Python directory, you will need to update the sp.NetCDFFile() and plt.savefig() functions with the file names and paths of the the dataset file and output file respectively.
