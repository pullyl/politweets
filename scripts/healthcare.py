#analyze whether or not tweets are related to healthcare
from os import listdir
from os.path import isfile, join
import pandas as pd
import yaml, re
from datetime import datetime

generic_terms = [' health ', 'health care',
                    'medicare', 'medicaid', 'medical', 'health insurance', 'healthcare']
r_leaning = ['Obama Care', 'ObamaCare', 'american health care act', 'acha']
d_leaning = ['#?ACA[^re]', 'Affordable Care Act', 'Trump Care', 'TrumpCare']
healthcare_terms = generic_terms + r_leaning + d_leaning
path_to_folder = "../raw_data"
file_suffix = "_tweets.csv"
output_file = "../manipulated_data/healthcare_output.csv"
legislators_yamls = ['../../congress-legislators/legislators-current.yaml', '../../congress-legislators/legislators-historical-min.yaml' ]
social_yamls = ['../../congress-legislators/legislators-social-media.yaml',
               '../../congress-legislators/legislators-historical-social-media.yaml']

twitter = 'twitter'
social = 'social'
id = 'id'
bioguide = 'bioguide'
party = 'party'
terms = 'terms'

twitter_dict = {}

def simplify_text(input):
    text = input.replace("\n", "")
    return text

def is_healthcare(input):
    return contains_term(healthcare_terms, input)

def is_r_leaning(input):
    return contains_term(r_leaning, input)

def is_generic(input):
    return contains_term(generic_terms, input)

def is_d_leaning(input):
    return contains_term(d_leaning, input)

def contains_term(terms, input):
    for term in terms:
        if not re.search(term, input, flags=re.IGNORECASE) == None:
            #print(input)
            #print '          %s' % term
            return 1

    return 0

def healthcare_count(input):
    count = 0
    for term in healthcare_terms:
        if not re.search(term, input, flags=re.IGNORECASE) == None:
            count += 1
    return count

def contains_word(input, args):
    if not re.search(args, input, flags=re.IGNORECASE) == None:
        return 1

    return 0

def load_yaml():
    # load in social yaml
    twitter_dict = {}
    bio_dict = {}
    for file in social_yamls:
        with open(file, 'r') as stream:
            data_loaded = yaml.load(stream)
        for data in data_loaded:
            if twitter in data[social].keys():
                twitter_dict[data[social][twitter].lower()] = {bioguide: data[id][bioguide]}
                bio_dict[data[id][bioguide]] = data[social][twitter].lower()

    # load in legislators yaml
    for file in legislators_yamls:
        with open(file, 'r') as stream:
            data_loaded = yaml.load(stream)
            for data in data_loaded:
                if party in data[terms][0].keys():
                    if data[id][bioguide] in bio_dict.keys():
                        twitter_dict[bio_dict[data[id][bioguide]]][party] = data[terms][0][party]
                        twitter_dict[bio_dict[data[id][bioguide]]]['terms'] = convert_to_date(data[terms])

    return twitter_dict


def convert_to_date(data):
    new_data = []
    for term in data:
        start = datetime.strptime(term['start'], '%Y-%M-%d').replace(hour=0, minute=0, second=0)
        end = datetime.strptime(term['end'], '%Y-%M-%d').replace(hour=23, minute=59, second=59)
        new_data.append({'start': start, 'end': end})
    return new_data

def main():
    print('Analyzing tweets related to healthcare')

    global twitter_dict
    twitter_dict = load_yaml()

    #setting up constants
    first_write = True

    directoryFiles = [f for f in listdir(path_to_folder) if isfile(join(path_to_folder, f))]
    num_files = 0

    row_count = 0
    for file in directoryFiles:
        if file_suffix not in file:
            continue

        #if 'WhipHoyer' not in file:
        #    continue

        num_files += 1
        #if num_files > 5:
        #    break

        twitter_handle = file.replace(file_suffix, "").lower()
        print("processing %s with twitter handle: %s" % (file, twitter_handle))
        file_name = "%s/%s" % (path_to_folder, file)
        df = pd.read_csv(file_name, encoding='utf8', quotechar='"')
        df = df.rename(columns={'user': 'twitter'})
        df['text'] = df['text'].apply(simplify_text)
        df['healthcare_count'] = df['text'].apply(healthcare_count)
        df['r_leaning'] = df['text'].apply(is_r_leaning)
        df['d_leaning'] = df['text'].apply(is_d_leaning)
        df['generic'] = df['text'].apply(is_generic)

        for term in healthcare_terms:
            df[term] = df['text'].apply(contains_word, args={term})
        if twitter_handle in twitter_dict.keys():
            df['party'] = twitter_dict[twitter_handle][party]
            df['bioguide'] = twitter_dict[twitter_handle][bioguide]
        else:
            print 'inspect this'
        df['while_in_office'] = df['created_at'].apply(while_in_office, args={twitter_handle})



        #remove rows without healthcare
        print 'before transformation len is: %d' % len(df.index)
        df = df.ix[~(df['healthcare_count'] == 0)]
        df = df.ix[~(df['while_in_office'] == False)]
        print 'after transformation len is: %d' % len(df.index)

        row_count += len(df.index)

        # write the data to a file
        if first_write:
            df.to_csv(output_file, encoding='utf8')
            first_write = False
        else:
            df.to_csv(output_file, encoding='utf8', mode='a', header=False)

    print('just wrote %d rows' % (row_count))

def while_in_office(date, rep):
    new_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    #print('understanding if %s was in office on %s' % (rep, new_date))

    terms = twitter_dict[rep.lower()]['terms']
    for term in terms:
        if new_date > term['start'] and new_date < term['end']:
            return True

    return False

main()

def test():
    text = "Told reporters GOP will bring budget reconciliation bill to Floor-their 61st attempt to repeal/undermine #ACA, would also add to the deficit"
    print 'is healthcare: %d' % (is_healthcare(text))

    for term in healthcare_terms:
        print term
        print( contains_word(text, term) )
#test()