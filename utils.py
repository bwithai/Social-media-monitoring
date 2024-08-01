import json
import os
from datetime import datetime

import unidecode
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv()


def get_database_url():
    username = os.environ["BD_USERNAME"]
    password = os.environ["DB_PASSWORD"]
    cluster_url = os.environ["MONGO_URI"]
    url = f"mongodb+srv://{username}:{password}@{cluster_url}"
    return url


def __login__(url):
    import os
    from selenium import webdriver

    # Path to your Chrome profile
    chrome_profile_path = os.path.expanduser('~/.config/google-chrome/Profile')

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={chrome_profile_path}")
    options.add_argument("start-maximized")

    # Initialize the WebDriver with the existing profile
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    input("Press Enter to close the browser...")
    # Close the browser
    driver.quit()

    # jalalayn, Jalalhaddad


def serialize_datetime(obj):
    if isinstance(obj, list):
        return [serialize_datetime(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: serialize_datetime(value) for key, value in obj.items()}
    elif isinstance(obj, datetime):
        return str(obj)
    else:
        return obj


def serialize_object_id(obj):
    if isinstance(obj, list):
        return [serialize_object_id(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: serialize_object_id(value) for key, value in obj.items()}
    elif isinstance(obj, ObjectId):
        return str(obj)
    else:
        return obj


def get_path(relative_path):
    # Get the full path
    full_path = os.path.abspath(relative_path)

    return full_path


def parse_engagement_metric(metric):
    if metric.endswith('K'):
        metric = int(float(metric[:-1]) * 1000)
    elif metric.endswith('M'):
        metric = int(float(metric[:-1]) * 1000000)
    else:
        metric = metric

    try:
        float(metric)
        return True
    except ValueError:
        return False


def clean_tweet_text(tweet_text):
    try:
        lines = tweet_text.split('\n')
        tweet = {}

        # Extract engagement metrics
        tweet['engagement'] = {
            'replays': lines[-4] if parse_engagement_metric(lines[-4]) else None,
            'retweets': lines[-3] if parse_engagement_metric(lines[-3]) else None,
            'likes': lines[-2] if parse_engagement_metric(lines[-2]) else None,
            'views': lines[-1] if parse_engagement_metric(lines[-1]) else None
        }

        # Extract username and handle
        tweet['context'] = lines[0]
        if "reposted" in tweet['context']:
            tweet['context'] += " tweet of " + lines[1]

            # Extract date
            tweet['datetime_on_x'] = lines[4]
            tweet['username'] = lines[2]

            # Extract tweet text
            tweet['tweet_text'] = '\n'.join(lines[5:-4])
        else:
            tweet['context'] = "tweeted by " + tweet['context']
            # Extract date
            tweet['datetime_on_x'] = lines[3]
            tweet['username'] = lines[1]

            num_none = sum(1 for value in tweet['engagement'].values() if value is None)
            to = num_none - 4
            tweet['tweet_text'] = '\n'.join(lines[5:to])

        return tweet
    except Exception as e:
        print(str(e))
        pass


def find_severity_score(hashtags, keyword):
    # Normalize the keyword for comparison
    normalized_keyword = unidecode.unidecode(keyword).lower()

    # Filter hashtags containing the keyword, with normalization
    filtered_hashtags = [hashtag for hashtag in hashtags if normalized_keyword in unidecode.unidecode(hashtag).lower()]

    # Severity score is the count of filtered hashtags
    severity_score = len(filtered_hashtags)

    # Calculate the percentage
    percentage = round((severity_score / len(hashtags)) * 100, 2)

    return severity_score, filtered_hashtags, percentage


def is_digit(likes):
    try:
        float(likes)
        return True
    except ValueError:
        return False


def clean_fb_post_text(post_text):
    lines = post_text.split('\n')
    post = {}
    likes = ""
    comments = ""
    shares = ""

    from_idx: int = 0
    to_idx: int = 0
    who_commented: int = 0
    comment_end: int = 0

    for idx, line in enumerate(lines):
        if line.strip() == "·":
            from_idx = idx + 1
        if line.strip() == "All reactions:":
            to_idx = idx
        if line.strip() == "Like":
            if lines[idx + 1] == "Comment" and lines[idx + 2] == "Send" and lines[idx + 3] == "Share":
                if lines[idx + 4] == "View more comments":
                    who_commented = idx + 5
                else:
                    who_commented = idx + 4
        if line.strip() == "Like":
            if lines[idx + 1].strip() == "Reply":
                comment_end = idx

    description = lines[from_idx:to_idx]
    likes = lines[to_idx + 2].strip()
    if is_digit(likes):
        likes = likes + " likes"
    comments_check = lines[to_idx + 3].strip()
    shares_check = lines[to_idx + 4].strip()
    if ("comments" in comments_check) or ("comment" in comments_check):
        comments = comments_check
    if ("shares" in shares_check) or ("share" in shares_check):
        shares = shares_check

    description_text: str = ""
    for d in description:
        description_text += d

    post['post_text'] = description_text
    post['engagement'] = {
        'likes': likes,
        'comments': comments,
        'shares': shares
    }
    person_comment = lines[who_commented + 1:comment_end - 2]
    comment_at = lines[comment_end - 2:comment_end]
    person_comment_text = ""
    comment_time = ""
    for t in person_comment:
        person_comment_text += t
    for t in comment_at:
        comment_time += t
    if comment_time != "":
        if person_comment_text != "":
            post['display_comment'] = lines[
                                          who_commented].strip() + f" commented at {comment_time} " + f' {person_comment_text}'
        else:
            post['display_comment'] = lines[
                                          who_commented].strip() + f" commented at {comment_time} " + 'comment contain emoji'
    return post


def save_json_file(system_info):
    # Save the system_info dictionary as a JSON file
    with open(get_path('system_info.json'), 'w') as json_file:
        json.dump(system_info, json_file, indent=4)
