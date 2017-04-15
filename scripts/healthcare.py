#analyze whether or not tweets are related to healthcare
from os import listdir
from os.path import isfile, join
import pandas as pd
import yaml

healthcare_terms = ['ACA', 'Affordable Care Act', 'Obama Care', 'ObamaCare', 'Trump Care', ' health ', 'health care',
                    'medicare', 'medicaid', 'medial', 'health insurance', 'american health care act', 'acha']
path_to_folder = "../raw_data"
file_suffix = "_tweets.csv"
output_file = "../manipulated_data/healthcare_output.csv"
social_yaml = '../raw_data/legislators-social-media.yaml'

twitter = 'twitter'
social = 'social'
id = 'id'
bioguide = 'bioguide'

def simplify_text(input):
    text = input.replace("\n", "")
    return text

def is_healthcare(input):
    for term in healthcare_terms:
        if input.find(term) == True:
            return True

    return False

def main():
    print('Analyzing tweets related to healthcare')

    #load in yaml
    with open(social_yaml, 'r') as stream:
        data_loaded = yaml.load(stream)

    ids = {}
    for data in data_loaded:
        if twitter in data[social].keys():
            ids[data[social][twitter]] = data[id][bioguide]

    #setting up constants
    first_write = True

    directoryFiles = [f for f in listdir(path_to_folder) if isfile(join(path_to_folder, f))]
    num_files = 0

    for file in directoryFiles:
        if file_suffix not in file:
            continue

        num_files += 1
        #if num_files > 5:
        #    break

        twitter_handle = file.replace(file_suffix, "")
        print("processing %s with twitter handle: %s" % (file, twitter_handle))
        file_name = "%s/%s" % (path_to_folder, file)
        df = pd.read_csv(file_name, encoding='utf8', quotechar='"')
        df[u'twitter'] = twitter_handle
        df[u'bioguide'] = ids[twitter_handle]
        df['text'] = df['text'].apply(simplify_text)
        df['healthcare'] = df['text'].apply(is_healthcare)

        #remove rows without healthcare
        df = df.ix[~(df['healthcare'] == False)]

        # write the data to a file
        if first_write:
            df.to_csv(output_file, encoding='utf8')
            first_write = False
        else:
            df.to_csv(output_file, encoding='utf8', mode='a', header=False)





main()