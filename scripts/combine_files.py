#!/usr/bin/python

#Script to combibe files from congresspeople

from os import listdir
from os.path import isfile, join
import csv, sys, yaml
import pandas as pd

#setup
path_to_folder = "../raw_data"
file_suffix = "_tweets.csv"
output_file = "../manipulated_data/combinedtweets.csv"
legislators_yaml = '../raw_data/legislators-current.yaml'
social_yaml = '../raw_data/legislators-social-media.yaml'
csv.field_size_limit(sys.maxsize)
party = 'party'
terms = 'terms'
twitter = 'twitter'
social = 'social'
bioguide = 'bioguide'
id = 'id'

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
    row_count = 0

    # load in social yaml
    with open(social_yaml, 'r') as stream:
        data_loaded = yaml.load(stream)
    twitter_dict = {}
    bio_dict = {}
    for data in data_loaded:
        if twitter in data[social].keys():
            twitter_dict[data[social][twitter].lower()] = {bioguide: data[id][bioguide]}
            bio_dict[data[id][bioguide]] = data[social][twitter].lower()

    # load in legislators yaml
    with open(legislators_yaml, 'r') as stream:
        data_loaded = yaml.load(stream)
        for data in data_loaded:
            if party in data[terms][0].keys():
                if data[id][bioguide] in bio_dict.keys():
                    twitter_dict[bio_dict[data[id][bioguide]]][party] = data[terms][0][party]

    # Read in all of the names of files
    directoryFiles = [f for f in listdir(path_to_folder) if isfile(join(path_to_folder, f))]

    for file in directoryFiles:
        if file_suffix not in file:
            continue

        num_files += 1
        twitter_handle = file.replace(file_suffix, "")
        print("processing %s with twitter handle: %s" % (file, twitter_handle))
        file_name = "%s/%s" % (path_to_folder, file)
        df = pd.read_csv(file_name, encoding='utf8', quotechar='"')
        df = df.rename(columns={'user': 'twitter'})
        df['party'] = twitter_dict[twitter_handle.lower()][party]
        del df['source']
        del df['favorite_count']
        del df['retweets']
        del df['text']

        # write the data to a file

        row_count += len(df.index)

        if first_write:
            df.to_csv(output_file, encoding='utf8')
            first_write = False
        else:
            df.to_csv(output_file, encoding='utf8', mode='a', header=False)

    print 'finished writing records from %d files to file: %s.  We found %d errors' % (num_files, output_file, error_count)
    print 'error files are:'
    print error_files

    print('just wrote %d rows' % (row_count))


main()