import sys
import operator
from tweet_utils import parse_raw_tweet

def get_hashtags(raw_tweet):
    entities = parse_raw_tweet(raw_tweet, "entities")
    if type(entities) == dict:
        if "hashtags" in entities:
            return entities["hashtags"]
    return []

def update_freq(freq_table, tags):
    for tag in tags:
        text = tag["text"]
        count = freq_table.get(text, 0)
        freq_table[text] = count + 1
    

def count_tweet_file(fp):
    count = 0
    freq_table = {}
    with fp as data_file:
        for line in data_file:
            tags = get_hashtags(line)
            update_freq(freq_table, tags)
            count += 1
            #if count == 100:
            #    break
    return freq_table
            
def print_top_ten(freq_table):
    sorted_freq_table = sorted(freq_table.iteritems(), key=operator.itemgetter(1), reverse=True)
    #print sorted_freq_table[:10]
    for tag in sorted_freq_table[:10]:
        print tag[0] + " " + str(tag[1])

def main():
    tweet_file = open(sys.argv[1])
    freq_table = count_tweet_file(tweet_file)
    print_top_ten(freq_table)


if __name__ == '__main__':
    main()
