import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

def getKey(item):
    return item[0]

def make_sorted_list(dct):
    lst = []
    for k, v in dct.iteritems():
        sum = reduce((lambda acc, x: acc + x), v.values())
        tup = [sum, k, v]
        lst.append(tup)
    sorted_lst = sorted(lst, key=getKey, reverse=True)
    return sorted_lst

def make_output_file(filename, lst):
    with open(filename, "w") as writer:
        lines = []
        for obj in lst:
            count, word, mp = obj
            mplst = []
            for ky, val in mp.iteritems():
                mplst.append(ky + ":" + str(val))
            line = str(count) + "," + word + "," + ("|".join(mplst))
            lines.append(line)
        output = "\n".join(lines).encode('utf-8').strip()
        writer.write(output)
    writer.close()

df = pd.read_csv('../manipulated_data/combinedtweets.csv', encoding='utf-8')

df2 = df.loc[:, ['text', 'party', 'twitter']]

df3 = (df2.drop('text', axis=1)
          .join
          (
          df2.text
          .str
          .split(expand=True)
          .stack()
          .reset_index(drop=True, level=1)
          .rename('text')
          ))

records = df3.to_records()
#print records[:10]
words = {}
party_count = {}
hashtags = {}
hashtags_count = {}
ats = {}
ats_count = {}

for rec in records:
    line, party, handle, word = rec
    word = word.encode('utf-8').strip()
    word = str(word).lower()
    party = party[:1]

    # if party in party_count:
    #     party_count[party] += 1
    # else:
    #     party_count[party] = 1
    #
    # if word in words:
    #     w = words[word]
    #     if party in w:
    #         w[party] += 1
    #     else:
    #         w[party] = 1
    #     words[word] = w
    # else:
    #     words[word] = {party: 1}

    if '#' in word:
        hashtag = word
        if hashtag in hashtags:
            h = hashtags[hashtag]
            if party in h:
                h[party] += 1
            else:
                h[party] = 1
            hashtags[hashtag] = h
        else:
            hashtags[hashtag] = {party: 1}

        if party in hashtags_count:
            hashtags_count[party] += 1
        else:
            hashtags_count[party] = 1

    if '@' in word:
        at = word
        if at in ats:
            a = ats[at]
            if party in a:
                a[party] += 1
            else:
                a[party] = 1
            ats[at] = a
        else:
            ats[at] = {party: 1}

        if party in ats_count:
            ats_count[party] += 1
        else:
            ats_count[party] = 1

# print words
# print party_count
print hashtags
print hashtags_count


sorted_hashtags = make_sorted_list(hashtags)
print sorted_hashtags
make_output_file("sorted_hashtags.csv", sorted_hashtags)

print ats
print ats_count

sorted_ats = make_sorted_list(ats)
print sorted_ats
make_output_file("sorted_ats.csv", sorted_ats)
