'''
question1_plot.py
  Author(s): Madison Gara (0973333)

  Previous contributors: Andrew Hamilton-Wright, Kassy Raymond, Anna Rehman (1161763), Daniella Konert (1185607), Shreya Takkar (1203546)

  Project: Group assignment Q1 script
  Date of Last Update: Mar 21, 2022.

  Functional Summary
      question1_graphing.py reads a CSV file and saves
      a plot based on the data to a PDF file.

     Commandline Parameters: 3
        sys.argv[0] = name of this py file being run (does not need to be initialized)
        sys.argv[1] = name of output data file to read (question1_output.csv)
        sys.argv[2] = name of plot file to create

python question1_plot.py question1_output.csv question1.pdf
'''

#   Packages and modules
import sys

# identify data by column
import pandas as pd

# matplotlib for graphics, seaborn for interface for plot production
import seaborn as sns
from matplotlib import pyplot as plt

# import tools for "ticks" along the x and y-axes and calls them "ticktools"
from matplotlib import ticker as ticktools

def main(argv):

    # Check that we have been given the right number of parameters,
    # and store the single command line argument in a variable with a better name
    if len(argv) != 3:
        print("Usage:",
                "question1_plot.py <data file> <graphics file>")
        sys.exit(-1)

    #set command line arguments
    csv_filename = argv[1]
    graphics_filename = argv[2]

    # Open the data file using "pandas", which will attempt to read in the entire CSV file
    try:
        #df for data file
        df = pd.read_csv(csv_filename)

    except IOError as err:
        print("Unable to open source file", csv_filename,
                ": {}".format(err), file=sys.stderr)
        sys.exit(-1)

    # get figure to draw plot in before plotting to it
    fig = plt.figure()

    #querying of the necessary countries and dates is already done via question1_extract.py through its writing to the question1_output.csv file
 
    # create lineplot using seaborn - refer to data columns
    ax = sns.lineplot(x = "DATE", y = "TOTAL_TESTS", hue="LOCATION_NAME", data=df)

    #move legend to upper left
    plt.legend(loc='upper left', title = "LOCATION_NAME")

  # set num of x-axis labels to 8
    ax.xaxis.set_major_locator(ticktools.MaxNLocator(8))
  
    # rotate ticks on x-axis to 45 degrees to the right
    plt.xticks(rotation = 45, ha = 'right')

    # save matplotlib figure drawn by seaborn
    fig.savefig(graphics_filename, bbox_inches="tight")

    # if figure is too large to close -> CTRL+C to exit
    #plt.show()

    #   End of Function

## Call our main function, passing the system argv as the parameter
main(sys.argv)

#   End of Script