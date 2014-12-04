import csv
import re

alphanum_pattern = re.compile('[\W]+')

# feature words
feature_file = open("../../../scripts/features.txt", 'r')
features = [x.strip() for x in feature_file.readlines()]

# tags
tags_file = open("../../../scripts/tags.txt", 'r')
tags = [x.strip() for x in tags_file.readlines()]

# select conversations to export

#round 1
# sample = files[0:49]  # a list

#round 2
# sample = files[50:99]

#round 3
sample = files[100:200]

sample_features_data = []

for s in sample:

    conversation = data[s]

    # calculate total number of words in conversation
    total_words = 0.0
    if 'post_tokenized' in conversation:
        total_words += len(conversation['post_tokenized'])

    if 'replies' in conversation:
        for i in conversation['replies'].keys():
            if 'reply_text_tokenized' in conversation['replies'][i]:
                total_words += len(conversation['replies'][i]['reply_text_tokenized'])

    # count the number of occurences for each of the feature words
    feature_counts = {}
    for word in features:
        count = 0.0
        if 'post_tokenized' in conversation:
            post_tokenized_clean = [re.sub(alphanum_pattern, '', x).lower() for x in conversation['post_tokenized']]
            count += post_tokenized_clean.count(word)

        if 'replies' in conversation:
            for i in conversation['replies'].keys():
                if 'reply_text_tokenized' in conversation['replies'][i]:
                    reply_text_tokenized_clean = [re.sub(alphanum_pattern, '', x).lower() for x in conversation['replies'][i]['reply_text_tokenized']]
                    count += reply_text_tokenized_clean.count(word)

        feature_counts[word] = count / total_words

    sample_features_data.append(feature_counts)


# write to csv for import into R
file = open('../../../priors/prior3.csv', 'wb')
csvwriter = csv.DictWriter(file, delimiter = ',', fieldnames = features)
csvwriter.writerow(dict((fn,fn) for fn in features))
for row in sample_features_data:
    csvwriter.writerow(row)
file.close()

    
