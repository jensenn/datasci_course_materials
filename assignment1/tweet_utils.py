import re
import json

def lines(fp):
    print str(len(fp.readlines()))
    
def parse_raw_tweet(line, key):
    try:
        json_data = json.loads(line)
        if key in json_data:
            return json_data[key]
    except ValueError:
        pass
    
    return "" #if there is an error or no tweet data, return an empty string                


def create_score_dict(fp):
    scores = {} # initialize an empty dictionary
    for line in fp:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.
    return scores

def get_wordlist(tweet):
    return re.sub("[^\w]", " ", tweet.lower()).split()
    
def score_tweet(tweet, scores):
    wordlist = get_wordlist(tweet)
    score = 0
    for word in wordlist:
        score += scores.get(word, 0)
    return score
