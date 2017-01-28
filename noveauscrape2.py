import time
import random
import praw
import json
from os.path import join, dirname
from watson_developer_cloud import PersonalityInsightsV2

# initial shit
personality_insights = PersonalityInsightsV2(
    username='86ffda72-c2bc-46e7-9204-5b9e318bd1a9',
    password='H8aOZBNsPAtC')
r = praw.Reddit('Interested not Interesting2')
usernames = open('usernames.txt', 'a')
personalityoutput = open('newpersonalitydata.txt', 'a')

def process():
    global count
    # get a random redditor
    try: 
        user = r.get_random_submission().author
        sourcetext = ""
        isEnough = False
        try:
            try:
                for comment in user.get_comments(limit=None):
                    sourcetext = sourcetext + comment.body + ' '
                    if (sourcetext.count(' ') >= 6000):
                        isEnough = True
                        break
            except praw.errors.NotFound:
                pass
        except praw.errors.Forbidden:
            pass

        # if found, call watson on the results
        if (isEnough):
            measures = personality_insights.profile(text=sourcetext.encode('utf-8'), accept='text/csv', csv_headers=True)

            # ...and store all interesting data in a csv file
            # usernames
            usernames.write(user.name+'\n')
            print user.name

            # personality data
            if count == 0:
                personalityoutput.write(measures.encode('cp850', errors='replace'))
            else:
                personalityoutput.write(measures[measures.find('\n')+1:].encode('cp850', errors='replace'))

            # increment count
            count = count + 1

        # pause a bit
        print count, "complete."
    except UnicodeDecodeError:
        pass

count = 229
while count < 2900:
    process()
