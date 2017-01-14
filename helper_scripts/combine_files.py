#!/usr/bin/python

#Script to combibe files from congresspeople

from os import listdir
from os.path import isfile, join
import csv, sys
import pandas as pd

#setup
path_to_folder = "../raw_data"
file_suffix = "_tweets.csv"
output_file = "../manipulated_data/combinedtweets.csv"
congress_data_file = "../raw_data/CongressTwitterHandles16and17.csv"
error_files = []
num_files = 0
error_count = 0
first_write = True
csv.field_size_limit(sys.maxsize)

print 'Starting to combine data'

#Read in all of the names of files
directoryFiles = [f for f in listdir(path_to_folder) if isfile(join(path_to_folder, f))]

#Read in congresspeople data
congress_data = pd.read_csv(congress_data_file, encoding='utf8')

for file in directoryFiles:
    if file_suffix not in file:
        continue

    num_files += 1
    twitter_handle = file.replace(file_suffix, "")
    print "processing %s with twitter handle: %s" % (file, twitter_handle)
    file_name = "%s/%s" % (path_to_folder, file)
    df = pd.read_csv(file_name, encoding='utf8')
    df[u'twitter'] = twitter_handle

    #try to merge with extracted data
    extracted_data = congress_data.loc[congress_data['twitter'] == twitter_handle]
    if len(extracted_data.index) > 0:

        #enhance extracted data
        df2 = pd.merge(df, congress_data, on='twitter', how='left')

        #write the data to a file
        if first_write:
            df2.to_csv(output_file, encoding='utf8')
            first_write = False
        else:
            df2.to_csv(output_file, encoding='utf8', mode='a', header=False)

    else:
        print 'we didnt find data for %s' % (twitter_handle)
        error_count += 1
        error_files.append(file)
        continue

print 'finished writing records from %d files to file: %s.  We found %d errors' % (num_files, output_file, error_count)
print 'error files are:'
print error_files