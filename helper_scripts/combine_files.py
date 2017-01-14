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
num_files = 0
csv.field_size_limit(sys.maxsize)

print 'Starting to combine data'

#Read in all of the names of files
directoryFiles = [f for f in listdir(path_to_folder) if isfile(join(path_to_folder, f))]

#open file for writing
with open(output_file, 'wb') as csvwriter:
    writer = csv.writer(csvwriter, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for file in directoryFiles:
        if file_suffix not in file:
            continue
        num_files += 1
        twitter_handle = "@%s" % (file.replace(file_suffix, ""))
        print "processing %s with twitter handle: %s" % (file, twitter_handle)
        file_name = "%s/%s" % (path_to_folder, file)

        df = pd.read_csv(file_name, encoding='utf8')
        df['twitter_handle'] = twitter_handle
        if num_files == 1:
            df.to_csv(output_file, encoding='utf8')
        else:
            df.to_csv(output_file, encoding='utf8', mode='a', header=False)

print 'finished writing records from %d files to file: %s' % (num_files, output_file)