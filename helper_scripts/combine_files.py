#!/usr/bin/python

#Script to combibe files from congresspeople

from os import listdir
from os.path import isfile, join
import csv, sys
#import pandas as pd

#setup
path_to_folder = "../raw_data"
file_suffix = "_tweets.csv"
output_file = "../manipulated_data/combinedtweets.csv"
num_records = 0
csv.field_size_limit(sys.maxsize)

print 'Starting to combine data'

#Read in all of the names of files
directoryFiles = [f for f in listdir(path_to_folder) if isfile(join(path_to_folder, f))]

#open file for writing
with open(output_file, 'wb') as csvwriter:
    writer = csv.writer(csvwriter, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #writer.writerow(['Spam'] * 5 + ['Baked Beans'])
    #writer.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

    for file in directoryFiles:
        if file_suffix not in file:
            continue
        twitter_handle = "@%s" % (file.replace(file_suffix, ""))
        print "processing %s with twitter handle: %s" % (file, twitter_handle)
        file_name = "%s/%s" % (path_to_folder, file)
        print file_name
        with open(file_name, 'rU') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in csvreader:
                num_records += 1
                print file_name
                row.append(twitter_handle)
                print ', '.join(row)
                writer.writerow(row)


print 'finished writing %d records to file: %s' % (num_records, output_file)