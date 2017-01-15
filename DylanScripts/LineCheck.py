
def get_retweet(arr):
    return int(arr[4])

def get_fav(arr):
    return int(arr[5])

input_file = "../manipulated_data/combinedtweets.csv"

file = open(input_file, 'r')

delim = ","
delim_count = {}

for line in file:
    delims = line.count(delim)
    if delims == 6:
        print line
    if delims in delim_count:
        delim_count[delims] += 1
    else:
        delim_count[delims] = 1
file.close()

print delim_count