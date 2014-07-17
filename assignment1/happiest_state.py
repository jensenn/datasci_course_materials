import sys
import re
from tweet_utils import score_tweet, create_score_dict, parse_raw_tweet

state_dict = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

inv_state_dict = {v.upper():k for k, v in state_dict.items()}

def get_tweet_state(raw_tweet):
    
    def search_state(in_str):
        if (in_str == ""):
            return ""
        #print "searching: " + in_str
        tmpstr = in_str.upper()
        for key in state_dict:
            if re.search(r"\b" + re.escape(key) + r"\b", tmpstr):
                return val
        for key in inv_state_dict:
            if re.search(r"\b" + re.escape(key) + r"\b", tmpstr):
                return inv_state_dict[key]
        return ""
        

    def parse_coord(raw_tweet):
#         coord = parse_raw_tweet(raw_tweet, "coordinates")
#         if (coord is not None and coord != ""):
#             print coord    
        return ""

    def parse_place(raw_tweet):
        place = parse_raw_tweet(raw_tweet, "place")
        if place is not None and place != "":
            if "full_name" in place:
                tmpstr = place["full_name"]
                state = search_state(tmpstr)
                if state != "":
                    return state
            if "name" in place:
                state = search_state(tmpstr)
                if state != "":
                    return state
        return ""

    def parse_user(raw_tweet):
        user = parse_raw_tweet(raw_tweet, "user")
        if (type(user) == dict):
            location = user["location"]
            return search_state(location.encode('utf-8'))
        return ""

    val = parse_coord(raw_tweet)
    if (val != ""):
        return val

    val = parse_place(raw_tweet)
    if (val != ""):
        return val
     
    val = parse_user(raw_tweet)
    if (val != ""):
        return val

    return ""


def update_state_dict(states, state, score):
    if (state != ""):
        if state in states:
            (count,total_score) = states[state]
            count += 1
            total_score += score
        else:
            count = 1
            total_score = score
        states[state] = (count, total_score)


def parse_tweet_file(fp, scores):
    count = 0
    states = {}
    with fp as data_file:
        for line in data_file:
            tweet = parse_raw_tweet(line, "text")
            score = score_tweet(tweet, scores)
            state = get_tweet_state(line)
            update_state_dict(states, state, score)    
            count += 1
            #if count == 20:
            #    break
    return states

            
def print_happiest_state(states):
    
    state = "Unknown"
    max_happiness = 0
    first = True
    for key in states:
        (count,total_score) = states[key]
        ave = total_score / float(count)
        print key + " - " + str(count) + " - " + str(ave)
        if first or ave > max_happiness:
            state = key
            max_happiness = ave
            first = False
    print state


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    scores = create_score_dict(sent_file)
    states = parse_tweet_file(tweet_file, scores)
    print_happiest_state(states)

if __name__ == '__main__':
    main()
