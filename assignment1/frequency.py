import sys
import re
import json

def lines(fp):
    print str(len(fp.readlines()))
    
def parse_raw_tweet(line):
    try:
        json_data = json.loads(line)
        if "text" in json_data:
            return json_data["text"]
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


def dofreq_tweet(tweet, freq_table):
    wordlist = get_wordlist(tweet)
    for word in wordlist:
        if word in freq_table:
            count = freq_table[word]
        else:
            count = 0
        count += 1
        freq_table[word] = count


def count_tweet_file(fp):
    #count = 0
    freq_table = {}
    with fp as data_file:
        for line in data_file:
            tweet = parse_raw_tweet(line)
            dofreq_tweet(tweet, freq_table)
            #count += 1
            #if count == 100:
            #    break
    return freq_table
            
def print_freq_table(freq_table):
    wordcount = sum(freq_table.itervalues())
    for key in freq_table:
        print key + " " + str(freq_table[key] / float(wordcount))

def main():
    tweet_file = open(sys.argv[1])
    freq_table = count_tweet_file(tweet_file)
    print_freq_table(freq_table)


if __name__ == '__main__':
    main()
