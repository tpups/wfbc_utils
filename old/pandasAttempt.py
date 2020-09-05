#must run using python3 command eg. "python3 pandasAttempt.py"

import os, csv, pandas, sys

path=os.getcwd()
# make list of all files in directory
allFiles = os.listdir(path)

for dataFile in allFiles:
    # rename xls extension to csv
    base_file, ext = os.path.splitext(dataFile)
    if ext == ".xls":
        os.rename(dataFile, base_file + ".csv")
        print(dataFile)

# declare empty list for csv files
csvFiles = []
# redefine allFiles variable to include newly renamed files
allFiles = os.listdir(path)
# add file to csvFiles list
for csvFile in allFiles:
    base_file, ext = os.path.splitext(csvFile)
    if ext == ".csv":
        csvFiles.append(csvFile)
        # print(csvFile)


# print number of csv files in directory
print(str(len(csvFiles)) + " csv files")

for csvFile in csvFiles:
    standings = pandas.read_csv(csvFile, sep='/t', header=None, engine='python')
#     modStandings = standings.replace("&#8943;", "-", regex=True)
#     modStandings.to_csv('new/'+csvFile, index=False)

    # for row in standings.itertuples(index=True, name='Pandas'):
    #     if standings[row][0].startswith("Standings"):
    #         print("booya")

    for row in standings:
        if standings[row][0].startswith("Standings"):
            print("Found it")

    # select first two rows
    # test = standings.head(n=2)
    # # test2 = test.iloc[0]
    # print("*****************************")
    # # if test.iloc[0].str.startswith('Standings'):
    # #     print("found it")
    # # print(test2)
    # print(standings.columns)
    # print("*****************************")
    # if standings.index[0].str.startswith("Standings"):
    #     print("Booya")

# using python csv module
# might have to use this to drop rows because pandas only allows referring to rows by index for rows after what it interprets as header
# for csvFile in csvFiles:
#     with open(csvFile, newline='') as f:
#         for line in f:
#             if line.startswith("Standings"):
#                 print("Found it")

