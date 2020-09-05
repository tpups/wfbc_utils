import os, csv

path=os.getcwd()
filenames = os.listdir(path)

for filename in filenames:
    # input = open(filename, newline = '', encoding = 'ISO-8859-1')
    
    input = open(filename, 'rt', newline = '', encoding = 'ISO-8859-1')
    output = open('new/'+filename, 'wt', newline = '', encoding = 'ISO-8859-1')
    writer = csv.writer(output)
    for row in csv.reader(input):
        if any(row):
            writer.writerow(row)
    input.close()
    output.close()
    # csvfile.count('\x00')
    # standings = csv.reader(x.replace('\0', '') for x in csvfile)
    # for row in standings:
    #     standings = [item.replace("'", "") for item in standings]
    #     print("Found one")


        # for item in row:
        #     if "&#8943;" in item:
        #         item.replace("&#8943;", "")
