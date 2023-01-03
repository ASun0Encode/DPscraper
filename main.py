import csv
from collections import defaultdict
import os

#COLLECTS NAMES OF FILES TO BE PROCESSED
path = 'csvs_before/'
folder = os.fsencode(path)
filenames = []
for file in os.listdir(folder):
    filename = os.fsdecode(file)
    if filename.endswith( ('.csv')):
        filenames.append(filename)

for currentfile in filenames:  #FOR EACH FILE

  # SETTING UP VARIABLES
  columns = defaultdict(list)
  
  # READ DATA INTO COLUMNS FOR PROCESSING=================================
  file = str('csvs_before/' + currentfile)
  with open(file) as Data:
    reader = csv.reader(Data)
    next(reader)
    for row in reader:
      for (i, v) in enumerate(row):
        columns[i].append(v)
  
  # ISOLATE PROJECT LINK INFO==============================================
  URLs = columns[5]        # a list of the project-links column in the CSV
  
  # SORT LINKS INTO DESIRED FORMAT=========================================
  y = len(URLs)
  # Set up of link storage
  GithubList = [None] * y    # list to hold github links
  OtherList = [None] * y     # list to hold all other links

  #iteration through each element in list
  i = 0
  for i in range(y):                                 
    TempList = URLs[i].split(',')                    # new list made from element with ',' as delimeter
    httpsList = [x for x in TempList if 'https' in x]  # extracts only links (elements containing 'https')
    print(httpsList)
    print(len(httpsList))

    if len(httpsList) == 0:
      Github = ''
      Other = ''
    else:
      # extract first github link listed if list not empty
      for link in httpsList:
        if 'github.com' in link:
            Github = link                                              # github.com link extracted
            Other = [item for item in httpsList if Github not in item] # removes github link from list
            break
        else: #case with no github link
            Github = ''
            Other = httpsList
    
    GithubList[i] = Github              # contains all github links per project
    print('this is the github:', GithubList[i])
    OtherList[i] = ', '.join(Other)     # contains additional links as one string per project
    print('this is the other link:', OtherList[i])
    
    #i = i+1      # to iterate through each project ##IS THIS NECESSARY?
  
  columns[5] = GithubList    # replace the original links column with github links
  columns[6] = OtherList     # create a new column containing the additional links
  
  # PRESENT DATA AS ROWS FOR WRITING TO CSV==============================================
  total = [[None]*7]*y    
  j = 1    # to avoid copying column numbers (had been previous enumerated)
  for j in range(y):
    total[j] = [ (columns[0])[j], (columns[1])[j], (columns[2])[j], (columns[3])[j], (columns[4])[j], (columns[5])[j], (columns[6])[j],]

  # add in headings
  export = [['web-scraper-start-url','project-name','project-description','project-team','devpost-link','github-links','other-project-links']] + total

  # WRITE DATA TO NEW CSV FILE==============================================
  FileName = str('csvs_after/' + currentfile + '_modified.csv')    # establish directory
  myFile = open(FileName, 'w')                                     # write mode
  writer = csv.writer(myFile, dialect='excel')                     # csv writer format
  
  # write each row
  for data_list in export:
      writer.writerow(data_list)
  myFile.close()


