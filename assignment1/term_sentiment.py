import sys
from tweet_utils import score_tweet, create_score_dict, get_wordlist, parse_raw_tweet


def sentiment_tweet(tweet, score, sentiments):
    wordlist = get_wordlist(tweet)
    for word in wordlist:
        if word in sentiments:
            (count, total_score) = sentiments[word]
        else:
            count = 0
            total_score = 0
        count += 1
        total_score += score
        sentiments[word] = (count, total_score)
        #print word + " - " + str(count) + " - " + str(score)
    return score


def score_tweet_file(fp, scores):
    #count = 0
    non_sentiments = {}
    with fp as data_file:
        for line in data_file:
            tweet = parse_raw_tweet(line)
            score = score_tweet(tweet, scores)
            sentiment_tweet(tweet, score, non_sentiments)
            #count += 1
            #if count == 100:
            #    break
    return non_sentiments
            
def print_sentiments(sentiments):
    for key in sentiments:
        (count, total_score) = sentiments[key]
        print key + " " + str(total_score / float(count))

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    scores = create_score_dict(sent_file)
    sentiments = score_tweet_file(tweet_file, scores)
    print_sentiments(sentiments)


if __name__ == '__main__':
    main()
