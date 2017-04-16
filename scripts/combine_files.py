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
legislators_yaml = '../raw_data/legislators-current.yaml'
csv.field_size_limit(sys.maxsize)

def convert_to_lat(input):
    input = str(input)
    if input == "nan":
        return ""

    input2 = input.replace("{u'type': u'Point', u'coordinates': [", "").replace("]}", "").split(",")
    return input2[1]

def convert_to_long(input):
    input = str(input)
    if input == "nan":
        return ""

    input2 = input.replace("{u'type': u'Point', u'coordinates': [", "").replace("]}", "").split(",")
    return input2[0]

def simplify_text(input):
    text = input.replace("\n", "")
    return text

def main():
    print 'Starting to combine data'

    error_files = []
    num_files = 0
    error_count = 0
    first_write = True

    # Read in all of the names of files
    directoryFiles = [f for f in listdir(path_to_folder) if isfile(join(path_to_folder, f))]

    for file in directoryFiles:
        if file_suffix not in file:
            continue

        num_files += 1
        twitter_handle = file.replace(file_suffix, "")
        print "processing %s with twitter handle: %s" % (file, twitter_handle)
        file_name = "%s/%s" % (path_to_folder, file)
        df = pd.read_csv(file_name, encoding='utf8', quotechar='"')
        df[u'twitter'] = twitter_handle
        del df['source']
        del df['favorite_count']
        del df['retweets']
        del df['text']

        # write the data to a file
        if first_write:
            df.to_csv(output_file, encoding='utf8')
            first_write = False
        else:
            df.to_csv(output_file, encoding='utf8', mode='a', header=False)


    print 'finished writing records from %d files to file: %s.  We found %d errors' % (num_files, output_file, error_count)
    print 'error files are:'
    print error_files

main()