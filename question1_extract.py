#!/usr/bin/env python

'''
question1_extract.py
  Author(s): Madison Gara (0973333)
  Earlier contributors(s): Deborah Stacey, Andrew Hamilton-Wright, Luke Tremble (1167443), Aaron Tran (1188548), Jake Goode (1202742), Daniella Konert (1185607), Anna Rehman (1161763), Shreya Takkar (1203546)

  Project: Group assignment Q1 script
  Date of Last Update: Mar 27, 2022.

     Commandline Parameters: 12
        argv[0] = the .py file itself
        argv[1] = year of date to start
        argv[2] = month of date to start
        argv[3] = day of date to start
        argv[4] = year of date to end
        argv[5] = month of date to end
        argv[6] = day of date to end
        argv[7] = PRUID (Ontario)
        argv[8] = country one's ISO code (international)
        argv[9] = country two's ISO code (international)
        argv[10] = Canadian csv file to process
        argv[11] = worldwide csv file to process

     References
        Files from 
https://ccodwg.github.io/Covid19CanadaArchive-data-explorer/
https://ourworldindata.org/coronavirus-testing#source-information-country-by-country

      Runs:

python question1_extract.py 2020 3 12 2020 5 1 35 HKG KOR data/covid19-epiSummary-labIndicators_2021-05-28_22-02.csv data/owid-covid-data.csv

python question1_extract.py 2020 5 30 2020 8 1 35 HKG KOR data/covid19-epiSummary-labIndicators_2021-05-28_22-02.csv data/owid-covid-data.csv
'''

# The 'sys' module gives us access to system tools, including the
# command line parameters, as well as standard input, output and error
import sys

# The 'csv' module gives us access to a tool that will read CSV
import csv

#import datetime modules needed
from datetime import date
from datetime import datetime
from datetime import timedelta

def main(argv):
    '''
    Main function in the script.
    '''
  
    #   Check that we have been given the right number of parameters,
    #   and store the single command-line argument in a variable with
    #   a better name
  
    if len(argv) != 12:
        print("Usage: read_file.py <file name>")

        # we exit with a zero when everything goes well, so we choose
        # a non-zero value for exit in case of an error
        sys.exit(1)

    #define command line args

    start_year = argv[1]
    start_month = argv[2]
    start_day = argv[3]
    end_year = argv[4]
    end_month = argv[5]
    end_day = argv[6]
    pruid_num = argv[7]
    country1_iso = argv[8]
    country2_iso = argv[9]
    canadian_file = argv[10]
    worldwide_file = argv[11]
  
    # Open the date data input files.  The encoding argument
    # indicates that we want to handle the BOM (if present)
    # by simply ignoring it.
  
    try:
        canadian_file = open(canadian_file, encoding="utf-8-sig")

    except IOError as err:
        # Here we are using the python format() function.
        # The arguments passed to format() are placed into
        # the string it is called on in the order in which
        # they are given.
        print("Unable to open name file '{}' : {}".format(
                canadian_file, err), file=sys.stderr)
        sys.exit(1)

    # do the same for the world file
    try:
        worldwide_file = open(worldwide_file, encoding="utf-8-sig")

    except IOError as err:
        print("Unable to open name file '{}' : {}".format(
                worldwide_file, err), file=sys.stderr)
        sys.exit(1)

    # Create a CSV (Comma Separated Value) reader based on this
    # open filehandle.  We can use the reader in a loop         iteration
    # in order to access each line in turn.
    file_reader_ON = csv.reader(canadian_file)
    file_reader_world = csv.reader(worldwide_file)

    #   Parse each line of data from the CSV reader, which will break
    #   the lines into fields based on comma delimiter
    #   The field for each line are stored in a different row data array
    #   for each line of the data.

    #format start and end date into datetime objects from arguments
    start_date = date(int(start_year), int(start_month), int(start_day))
    end_date = date(int(end_year), int(end_month), int(end_day))

    #create csv writer to write relevant data to question1_output (for graphing)
    file_to_graph = open('question1_output.csv', 'w', newline = '')
    file_writer = csv.writer(file_to_graph)
  
    #name headers of the new csv file and write those headers to the file
    header = ['DATE', 'LOCATION_NAME', 'TOTAL_TESTS']
    file_writer.writerow(header)

  

    '''
    Canada file handling
    '''
    #set current date to start date
    current_date = start_date
  
    #print the column names as required
    print("DATE,PR_NAME,TOTAL_TESTS")

    #initialize variables to blank values in case of empty field
    date_ON = "0000-00-00"
    pruid_num_infile = 0
    pr_name = " "
    numtests = 0.00

    #separating each field by comma
    for row in file_reader_ON:
      
      #initialize variables to be examined to their fields
      date_ON = row[1]
      pruid_num_infile = row[0]
      pr_name = row[2]
      if (row[3] != ""):
        numtests = row[3]

      #convert current date into string for comparison
      compare_date = datetime.strftime(current_date, "%Y-%m-%d")
      
      #if region is Ontario (by its PRUID number), print that line in file
      if (pruid_num_infile == pruid_num):

        #Additional if statement to ensure that only print data when date == current_date (formatted as a string)
        if (date_ON == compare_date): 
          
          #loop only through the years given as an argument
          while (current_date <= end_date):
  
            date_ON = row[1]
            pruid_num_infile = row[0]
            pr_name = row[2]
            if (row[3] != ""):
              #account for differences in population between the three countries
              numtests = float(row[3])
              numtests = ("{:.2f}".format(numtests / 1.95))

            #save everything to the csv file for later graphing
            data = [date_ON,pr_name,numtests]
            file_writer.writerow(data)

            #print everything
            print(date_ON + "," + pr_name + "," + str(numtests))
            
            #increment date then break to next line
            current_date += timedelta(days=1)
            break

  

    '''
    East Asia file handling - Hong Kong
    '''
  
    #set current date back to start date
    current_date = start_date
  
    #print the column names as required
    print()
    print("DATE,LOCATION,TOTAL_TESTS")
    print("COUNTRY 1")

    #initialize variables to blank values in case of empty field
    country_iso_infile = " "
    location = " "
    date_EA = "0000-00-00"
    total_tests = 0.00

    #separating each field by comma
    for row in file_reader_world:
      
      #initialize variables to be examined to their fields
      country_iso_infile = row[0]
      location = row[2]
      date_EA = row[3]
      if (row[26] != ""):
        total_tests = row[26]

      #convert current date into string for comparison
      compare_date = datetime.strftime(current_date, "%Y-%m-%d")
      
      #if region is first or second country, print that line in file
      if (country_iso_infile == country1_iso):

        #Additional if statement to ensure that only print data when date == current_date (formatted as a string)
        if (date_EA == compare_date): 
          
          #loop only through the years given as an argument
          while (current_date <= end_date):
  
            location = row[2]
            date_EA = row[3]
            if (row[26] != ""):
              #Hong Kong, as it has the smallest population, is being used as the base measure of the three countries
              total_tests = float(row[26])
              total_tests = ("{:.2f}".format(total_tests))

            #save everything to the csv file for later graphing
            data = [date_EA,location,total_tests]
            file_writer.writerow(data)

            print(date_EA + "," + location + "," + str(total_tests))

            #increment current date  
            current_date += timedelta(days=1)

            #break to the next line regardless once info is gathered
            break



    '''
    East Asia file handling - South Korea
    '''
  
    #reopen the file to reset the csv reader to the start
    worldwide_file = argv[11]
  
    try:
        worldwide_file = open(worldwide_file, encoding="utf-8-sig")

    except IOError as err:
        print("Unable to open name file '{}' : {}".format(
                worldwide_file, err), file=sys.stderr)
        sys.exit(1)

      
    # Create a CSV (Comma Separated Value) reader based on this
    # open filehandle.  We can use the reader in a loop iteration
    # in order to access each line in turn.
    file_reader_world = csv.reader(worldwide_file)
    
    #set current date back to start date
    current_date = start_date

    print("COUNTRY 2")

    #initialize variables to blank values in case of empty field
    country_iso_infile = " "
    location = " "
    date_EA = "0000-00-00"
    total_tests = 0.00

    #separating each field by comma - also removed double quotes!
    for row in file_reader_world:
      
      #initialize variables to be examined to their fields
      country_iso_infile = row[0]
      location = row[2]
      date_EA = row[3]
      if (row[26] != ""):
        total_tests = row[26]
        
      #convert current date into string for comparison
      compare_date = datetime.strftime(current_date, "%Y-%m-%d")
      
      #if region is first or second country, print that line in file
      if (country_iso_infile == country2_iso):

        #Additional if statement to ensure that only print data when date == current_date (formatted as a string)
        if (date_EA == compare_date): 
          
          #loop only through the years given as an argument
          while (current_date <= end_date):
  
            location = row[2]
            date_EA = row[3]
            if (row[26] != ""):
              #account for differences in population between the three countries
              total_tests = float(row[26])
              total_tests = ("{:.2f}".format(total_tests / 6.92))

            #save everything to the csv file for later graphing
            data = [date_EA,location,total_tests]
            file_writer.writerow(data)
  
            print(date_EA + "," + location + "," + total_tests)

            #increment current date  
            current_date += timedelta(days=1)

            #break to the next line regardless once info is gathered
            break
    
    #   End of Function

## Call our main function, passing the system argv as the parameter
main(sys.argv)