import re
import tweepy as tw
from inspect_reports import query_yes_no, read_as_list

def write_list(l, l_name, iterate, encoding):
    with open(l_name, 'w', encoding=encoding) as f:
        if iterate:
            for item in l:
                f.write("%s\n" % item)
        else:
            f.write("%s\n" % l)

if '__main__' == __name__:

    print('Retrieving tweets...')
    keys = read_as_list('twitter_keys.txt', 'latin-1')
    keywords = read_as_list('keywords.txt', 'latin-1')
    consumer_key, consumer_secret, access_token, access_token_secret=keys[0], keys[1], keys[2], keys[3]
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    results=[]
    date_since = "2000-01-01" 
    for search_words in keywords:
        for l in ['en', 'es']:
            tweets = tw.Cursor(api.search, q=search_words, lang=l, since=date_since, tweet_mode='extended', include_entities=True).items()
            for tweet in tweets:
                results.append(re.sub(r'[^\x00-\x7f]', r' ', tweet.full_text))
    out = list(set(results))

    print('Inspecting impact evidence on text...')
    positive_words = 'impact'
    for i in out:
        if positive_words in i:
            print(i)
            print('\n')
            answer = query_yes_no("Is this text about impact?")
            if answer:
                f = open("twitter.sentences", "a+")
                f.write(i)
                f.write("\n")
                f.close()
