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
output_file = "../manipulated_data/combinedtweets5.csv"
num_files = 0
csv.field_size_limit(sys.maxsize)

print 'Starting to combine data'

#Read in all of the names of files
directoryFiles = [f for f in listdir(path_to_folder) if isfile(join(path_to_folder, f))]

#open file for writing
# with open(output_file, 'wb') as csvwriter:
#     writer = csv.writer(csvwriter, delimiter=' ',
#                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

out = []

for file in directoryFiles:
    if file_suffix not in file:
        continue
    twitter_handle = "@%s" % (file.replace(file_suffix, ""))
    print "processing %s with twitter handle: %s" % (file, twitter_handle)
    file_name = "%s/%s" % (path_to_folder, file)
    prevline = ""

    reader = open(file_name, 'r')
    lines = reader.readlines()
    if num_files == 0:
        header = lines[0]
        header = filter(lambda c: 32 <= ord(c) <= 177, header)
        out.append(header)

    for line in lines[1:]:
        line = line.replace('\n', '').replace('\r', '')
        line = filter(lambda c: 32 <= ord(c) <= 177, line)

        if len(line) < 8 or not line[0:6].isdigit() or prevline.count(",") < 6 or "," not in line:
            prevline += line
        elif len(line) >= 8 and line[0:8].isdigit() and len(prevline) >= 8 and prevline[0:8].isdigit():
            if not prevline[0:5].isdigit():
                print "Darn!"
                print "prevline issue: %s" % prevline
            out.append(prevline)
            prevline = line
        else: #come across a non-IDed line
            prevline += line
    if prevline[0:8].isdigit():
        out.append(prevline)
    else:
        print "Drat!"
        print "Other prevline issue: %s" % prevline

    reader.close()
    num_files += 1

print len(out)
print "Start out"
# min_ascii = ord(out[0][0])
# max_ascii = ord(out[0][0])
# ords = {}
# for outline in out:
#     # if not outline[0:8].isdigit() or len(outline) < 40 or outline.count(",") < 6 or '\n' in outline:
#     #     print outline
#     for ch in outline:
#         ordch = ord(ch)
#         if ordch < 32 or ordch > 177:
#             if ordch in ords:
#                 ords[ordch] += 1
#             else:
#                 ords[ordch] = 1
            # print ch
            # print ord(ch)
            # print outline
    #     if ord(ch) > max_ascii:
    #         max_ascii = ord(ch)
    #     if ord(ch) < min_ascii:
    #         min_ascii = ord(ch)

# print "End out"
# print ords
# print ("Max: %i" % max_ascii)
# print ("Min: %i" % min_ascii)

with open(output_file, "w") as writer:
    output = '\n'.join(out)
    writer.write(output)
#    writer.writelines(out[0:2000])
writer.close()


print 'finished writing records from %d files to file: %s' % (num_files, output_file)