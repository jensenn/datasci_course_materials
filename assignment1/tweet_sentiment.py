import sys
from tweet_utils import score_tweet, create_score_dict, parse_raw_tweet
    
def score_tweet_file(fp, scores):
#     count = 0
    with fp as data_file:
        for line in data_file:
            tweet = parse_raw_tweet(line)
            print score_tweet(tweet, scores)
#             count += 1
#             if count == 8:
#                 break

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    scores = create_score_dict(sent_file)
    score_tweet_file(tweet_file, scores)

if __name__ == '__main__':
    main()
