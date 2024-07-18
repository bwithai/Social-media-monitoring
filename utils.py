import json
import os
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


def serialize_object_id(dic):
    dic = [
        {**doc, '_id': str(doc['_id'])} for doc in dic
    ]
    return dic


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


def save_json_file(system_info):
    # Save the system_info dictionary as a JSON file
    with open(get_path('system_info.json'), 'w') as json_file:
        json.dump(system_info, json_file, indent=4)
