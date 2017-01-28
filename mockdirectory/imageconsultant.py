import json
from watson_developer_cloud import PersonalityInsightsV2
from watson_developer_cloud import ToneAnalyzerV3

def imageconsultant(query):
    personality_insights = PersonalityInsightsV2(
        username='86ffda72-c2bc-46e7-9204-5b9e318bd1a9',
        password='H8aOZBNsPAtC')
    tone_analyzer = ToneAnalyzerV3(
        username='11594684-5795-4c08-852c-57b77ef1bf18',
        password='TNpwZBPeo65d',
        version='2016-05-19')

    #### If I have to modify, it's just altering where/when the file is accessed ####
    
    # open post data and parse the output
    inputjson = open('hackathon.json')
    data = json.load(inputjson)
    
    # store total likes as variable
    likes = data['likes']

    # store count as variable
    count = len(data['response']['data'])

    # average likes
    avglikes = likes/count

    # posts
    history = ''
    for i in range(count):
        try:
            history = history + ' ' + data['response']['data'][i]['message']
        except KeyError:
            continue
    
    #### Extract Traits ####

    # store personality traits as var(s)
    traits = personality_insights.profile(text=history.encode('utf-8'), accept='text/csv', csv_headers=True)
    traits = traits[traits.find('\n')+1:].encode('cp850', errors='replace')
    traits = traits.split(',')[2:54]

    # calculate likeability
    coefs = open('coefficients.txt')
    coeflines = coefs.read().split('\n')[1:]
    coefs = []
    for i in range(len(coeflines)-1):
        each = coeflines[i]
        each = each.split('\t')
        coefs.append(float(each[1]))
    
    likeability = float(coefs[0])
    for i in range(len(traits)):
        likeability = likeability + float(traits[i])*float(coefs[i])

    #### Generate Content ####

    # now calculate prospective values from the new post
    # we want to combine the query with the history and evaluate differences
    wordcounthist = history.count(' ')
    wordcountquery = query.count(' ')
    samplesize = 6000 # may want this to be proportional to post in the long run
    combine = ''
    if (wordcounthist + wordcountquery) > samplesize:
        combine = query + " ".join(history.split(' ')[:samplesize])
    else:
        combine = query + history

    traits2 = personality_insights.profile(text=combine.encode('utf-8'), accept='text/csv', csv_headers=True)
    traits2 = traits2[traits2.find('\n')+1:].encode('cp850', errors='replace')
    traits2 = traits2.split(',')[2:54]

    # magnititude of changes
    difference = []
    for i in range(len(traits2)):
        difference.append(float(traits2[i])-float(traits[i]))

    # calculate impact of changes
    impact = []
    for i in range(len(traits)):
        impact.append(coefs[i] * difference[i])
    
    # sentence analysis
    sentence = json.dumps(tone_analyzer.tone(text=query), indent=2)

    # predict likes from this new post too
    #predictiondata = open('predictdata.txt')
    # proportionaldifference =
    # prospavg = avglikes * proportionaldifference
    # prosplikes = (prospavg*(count+1))-likes
    prosplikes = 1

    traitlabels = ['Agreeableness', 'Altruism', 'Cooperation', 'Modesty', 'Morality',
                   'Sympathy', 'Trust', 'Conscientiousness', 'Achievement striving',
                   'Cautiousness', 'Dutifulness', 'Orderliness', 'Self-discipline',
                   'Self-efficacy', 'Extraversion', 'Activity level', 'Assertiveness',
                   'Cheerfulness', 'Excitement-seeking', 'Friendliness', 'Gregariousness',
                   'Neuroticism', 'Anger', 'Anxiety', 'Depression', 'Immoderation',
                   'Self-consciousness', 'Vulnerability', 'Openness', 'Adventurousness',
                   'Artistic interests', 'Emotionality', 'Imagination', 'Intellect',
                   'Liberalism', 'Liberty', 'Ideal', 'Love', 'Practicality',
                   'Self-expression', 'Stability', 'Structure', 'Challenge', 'Closeness',
                   'Curiosity', 'Excitement', 'Harmony', 'Conservation', 'Hedonism',
                   'Openness to change', 'Self-enhancement', 'Self-transcendence']

    data = {}
    for i in range(len(traits)):
        data[traitlabels[i]] = {"Difference": str(difference[i]), "Impact": str(impact[i])}
    data["Predicted Likes"] = str(prosplikes)
    return sentence, json.dumps(data)
    

# for testing
def main():
    query = 'Just keep in mind that using for in in native JavaScript, needs you be aware of your environment in terms of the possible prototype changes in the basic JavaScript objects and global data types. For instance if you are using a js lib that adds new stuff to Array.prototype or Object.prototype.'
    for each in imageconsultant(query):
        print each
        raw_input()
