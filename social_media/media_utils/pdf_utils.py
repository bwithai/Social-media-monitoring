import re

import unidecode

PER_PAGE_HEADER_FOOTER = """header {
                text-align: center;
                padding: 10px 0;
                background-color: #333;
                color: #fff;
                font-size: 1.2em;
                position: running(header);
                width: 640px;
                border-top-left-radius: 50%; /* Upper left corner */
                border-top-right-radius: 50%; /* Upper right corner */
            }
            footer {
                text-align: center;
                padding: 10px 0;
                margin-left: -19px;
                margin-bottom: -55px;
                background-color: #333;
                color: #fff;
                font-size: 1.2em;
                position: running(footer);
                width: 640px;
                border-bottom-left-radius: 50%; /* Upper left corner */
                border-bottom-right-radius: 50%; /* Upper right corner */
                position: fixed;
                bottom: 0;
            }"""


def find_severity_score_based_on_post_data(tweets_data, keyword):
    # Normalize the keyword for comparison
    normalized_keyword = unidecode.unidecode(keyword).lower()
    highlighted_keyword = f"<span style='color:blue;'>{keyword}</span>"

    # Compile a regex pattern for case-insensitive matching
    keyword_pattern = re.compile(re.escape(normalized_keyword), re.IGNORECASE)

    severity_score = 0

    # Function to highlight the keyword while preserving original text
    def highlight_match(match):
        return f"<span style='color:blue;'>{match.group(0)}</span>"

    # Iterate over tweets and replace the keyword with highlighted_keyword
    for tweet in tweets_data[0]['tweets']:
        tweet_text = tweet['original_tweet_text']
        if keyword_pattern.search(unidecode.unidecode(tweet_text).lower()):
            tweet['original_tweet_text'] = keyword_pattern.sub(highlight_match, tweet_text)
            severity_score += 1

    # Calculate the percentage
    percentage = round((severity_score / len(tweets_data[0]['tweets'])) * 100, 2)

    # Collect filtered tweets for output
    filtered_tweets = [
        tweet['original_tweet_text'] for tweet in tweets_data[0]['tweets']
        if highlighted_keyword in tweet['original_tweet_text']
    ]

    return severity_score, filtered_tweets, percentage
