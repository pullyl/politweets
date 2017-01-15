__author__ = 'dylan'
#!/usr/bin/python

#Script to combibe files from congresspeople

from os import listdir
from os.path import isfile, join
import csv, sys
import pandas as pd

#setup
path_to_folder = "../raw_data"
file_suffix = "_tweets.csv"
output_file = "../manipulated_data/combinedtweets4.csv"
num_files = 0
csv.field_size_limit(sys.maxsize)

print 'Starting to combine data'

#Read in all of the names of files
directoryFiles = [f for f in listdir(path_to_folder) if isfile(join(path_to_folder, f))]

#open file for writing
# with open(output_file, 'wb') as csvwriter:
#     writer = csv.writer(csvwriter, delimiter=' ',
#                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
with open(output_file, "w") as writer:

    for file in directoryFiles:
        if file_suffix not in file:
            continue
        twitter_handle = "@%s" % (file.replace(file_suffix, ""))
        print "processing %s with twitter handle: %s" % (file, twitter_handle)
        file_name = "%s/%s" % (path_to_folder, file)

        reader = open(file_name, 'r')
        linenum = 0
        prevline = ""

        for line in reader:
            line = line.replace('\n', '')
            if linenum == 0:
                if num_files == 0:
                    writer.write(line) #write header
                linenum += 1
                continue

            if len(line) < 8 or not line[0:6].isdigit() or prevline.count(",") < 6 or "," not in line:
                prevline += line
            elif len(line) >= 8 and line[0:8].isdigit() and len(prevline) >= 8 and prevline[0:8].isdigit():
                if not prevline[0:5].isdigit():
                    print "Darn!"
                    print "prevline issue: %s" % prevline
                writer.write(prevline)
                prevline = line
            else: #come across a non-IDed line
                prevline += line
            linenum += 1
        if prevline[0:8].isdigit():
            writer.write(prevline)
        else:
            print "Drat!"
            print "Other prevline issue: %s" % prevline

        reader.close()
        num_files += 1
        writer.write("File done!")

writer.close()

print 'finished writing records from %d files to file: %s' % (num_files, output_file)