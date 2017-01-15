
def get_retweet(arr):
    if arr[3] == '':
        return arr[4]
    else:
        return arr[6]

def get_fav(arr):
    if arr[3] == '':
        return arr[5]
    else:
        return arr[7]

input_file = "../manipulated_data/combinedtweets5.csv"

file = open(input_file, 'r')

#,id,created_at,coordinates,retweets,favorite_count,source,text,twitter_handle
most_retweets = -1
most_retweets_list = []

most_favorited = -1
most_favorited_list = []

header = file.readline()

#for x in range(0, 10):
#    line = file.readline()
for line in file:
    arr = line.split(',')
    if len(arr) < 7:
        print line
        break
    retweets = get_retweet(arr)
    favs = get_fav(arr)
    # print arr
    # print "retweets:" + retweets
    # print "favs:" + favs

    # most retweets
    if retweets >= most_retweets:
        #Same number of retweets -> add to list
        if retweets == most_retweets:
            most_retweets_list.append(line)
        #New champ -> start new list
        else:
            most_retweets_list = [line]
            most_retweets = retweets
    # most retweets
    if favs >= most_favorited:
        #Same number of retweets -> add to list
        if favs == most_retweets:
            most_favorited_list.append(line)
        #New champ -> start new list
        else:
            most_favorited_list = [line]
            most_favorited = favs

print "Most retweeted:"
print most_retweets
print '\n'.join(most_retweets_list)
print ""
print "Most favorited:"
print most_favorited
print '\n'.join(most_favorited_list)

file.close()
