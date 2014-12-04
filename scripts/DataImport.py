import os.path
import re
import datetime
import pprint

months = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
data = {}

#regexps for extraction
title_pattern = re.compile("Title:.*URL:", re.DOTALL)
URL_pattern = re.compile("URL:.*Statistics:", re.DOTALL)
views_pattern = re.compile("Views:.*?Votes:")
votes_pattern = re.compile("Votes:.*?Shares:")
shares_pattern = re.compile("Shares:.*")
poster_pattern = re.compile("Description:.*?/")
replies_pattern = re.compile("Reply:.*?$")
replier_pattern = re.compile("^.*? /")
replydate_pattern = re.compile("/.*? - [0-2][0-9]:[0-5][0-9] ")
endorsed_pattern = re.compile("Endorsed by.*See endorsement in context")
correct_pattern = re.compile("Correct Answer by.*See correct answer in context")
correct_answerer_pattern = re.compile("^.*? about")
correct_text_pattern = re.compile("months ago.*See correct answer in context")

# interate through directory and load data into a data dictionary
# data dictionary = {key: filename, value: dict of data in posting in filename}
files = [f for f in os.listdir('.') if os.path.isfile(f)]
for filename in files:
    # read in file and create a version without newlines
    f = open(filename, 'r')
    f_text = f.read()
    f_text_no_newlines = f_text.replace('\n', ' ')

    conversation = {}  # dict for data

    # Extract title
    title_MO = re.search(title_pattern, f_text_no_newlines)
    if title_MO:
        title_str = title_MO.group().replace("Title:", "").replace("URL:", "").strip()
        conversation['title'] = title_str

    # Extract URL
    URL_MO = re.search(URL_pattern, f_text_no_newlines)
    if URL_MO:
        URL_str = URL_MO.group().replace("URL:", "").replace("Statistics:", "").strip()
        conversation['URL'] = URL_str

    # Extract number of Views
    views_MO = re.search(views_pattern, f_text)
    if views_MO:
        views_str = re.sub(r"\D", "", views_MO.group())
        conversation['Views'] = int(views_str)

    # Extract number of Votes
    votes_MO = re.search(votes_pattern, f_text)
    if votes_MO:
        votes_str = re.sub(r"\D", "", votes_MO.group())
        conversation['Votes'] = int(votes_str)

    # Extract number of Shares
    shares_MO = re.search(shares_pattern, f_text)
    if shares_MO:
        shares_str = re.sub(r"\D", "", shares_MO.group())
        conversation['Shares'] = int(shares_str)
    
    # Extract original poster
    poster_MO = re.search(poster_pattern, f_text_no_newlines)
    if poster_MO:
        poster_str = poster_MO.group().replace("Description:", "").replace("/", "").strip()
        conversation['poster'] = poster_str

    # Extract posting date
    if poster_MO:
        postdate_pattern = re.compile(poster_MO.group() + ".*?$", re.M)
        postdate_MO = re.search(postdate_pattern, f_text)
        if postdate_MO:
            postdate_str = postdate_MO.group().replace(poster_MO.group(), "").strip()
            postdate_str_tokenized = postdate_str.split()
            postdate_month = int(months[postdate_str_tokenized[0]])
            postdate_date = int(re.sub(r"\D", "", postdate_str_tokenized[1]))
            postdate_year = int(postdate_str_tokenized[2])
            conversation['post_date'] = datetime.date(postdate_year, postdate_month, postdate_date)
    
    # Extract original posting
    post_pattern = re.compile(postdate_MO.group() + ".*I have this problem too")
    post_MO = re.search(post_pattern, f_text_no_newlines)
    if post_MO:
        post_str = post_MO.group().replace(postdate_MO.group(), "").replace("I have this problem too", "").strip()
        conversation['post'] = post_str
        conversation['post_tokenized'] = post_str.split()
    
    # Extract endorsement if exists
    endorsed_MO = re.search(endorsed_pattern, f_text_no_newlines)
    if endorsed_MO:
        endorsed_str = endorsed_MO.group().replace("Endorsed by", "").replace("See endorsement in context", "").strip()
        conversation['endorsed'] = endorsed_str
        conversation['endorsed_tokenized'] = endorsed_str.split()

    # Extract correct answers if exists
    correct_MO = re.search(correct_pattern, f_text)
    if correct_MO:
        # split correct answers in to individual answers and procees into dict
        correct_list_of_str = correct_MO.group().split("Correct Answer by")

        correct_answers_dict = {}
        i = 1;
        for s in correct_list_of_str:
            correct_dict = {}
            if len(s.strip()) > 0:
                # Extract correct answer ID
                correct_str = s.strip()
                correct_answerer_MO = re.search(correct_answerer_pattern, correct_str)
                correct_answerer_str = correct_answerer_MO.group().replace("about", "").strip()
                correct_dict['answerer'] = correct_answerer_str

                # Extract correct text
                correct_text_MO = re.search(correct_text_pattern, correct_str)
                if correct_text_MO:
                    correct_text_str = correct_text_MO.group().replace("months ago", "").replace("See correct answer in context", "").strip()
                    correct_dict['correct_text'] = correct_text_str
                    correct_dict['correct_text_tokenized'] = correct_text_str.split()

                # Put correct text into dict
                correct_answers_dict[i] = correct_dict
                i += 1

        # Add correct dict to conversation
        conversation['correct'] = correct_answers_dict
                
    # Extract replies if exists
    replies_MO = re.search(replies_pattern, f_text_no_newlines)

    if replies_MO:

        # split replies into individual replies and process into a dict
        replies_list_of_str = replies_MO.group().split("Reply: ")

        replies_dict = {}
        i = 1;
        for s in replies_list_of_str:
            reply_dict = {}
            if len(s.strip()) > 0:

                #Extract replier ID 
                reply_str = s.strip()
                replier_MO = re.search(replier_pattern, reply_str)
                if replier_MO:
                    replier_str = replier_MO.group().replace("/", "").strip()
                    reply_dict["replier"] = replier_str

                #Extract reply date
                replydate_MO = re.search(replydate_pattern, reply_str)
                if replydate_MO:
                    replydate_str = replydate_MO.group().replace("/", "").strip()
                    reply_dict["reply_date"] = datetime.datetime.strptime(replydate_str, "%a, %m%d%Y - %H:%M")
                    #Extract reply text
                    replytext_MO = re.search(replydate_MO.group() + ".*$", reply_str)
                    if replytext_MO:
                        replytext_str = replytext_MO.group().replace(replydate_MO.group(), "").strip()
                        reply_dict["reply_text"] = replytext_str
                        reply_dict['reply_text_tokenized'] = replytext_str.split()
                
                #Add the reply to replies_dict and increment
                replies_dict[i] = reply_dict
                i += 1

        #Add replies_dict to the conversation
        conversation['replies'] = replies_dict

    data[filename] = conversation
    
## pp = pprint.PrettyPrinter(indent = 4)
## pp.pprint(data)


# afinnfile = open("AFINN-111.txt")
# scores = {} # initialize an empty dictionary
# for line in afinnfile:
#    term, score  = line.split("\t")  # The file is tab-delimited.
#    scores[term] = int(score)  # Convert the score to an integer.


