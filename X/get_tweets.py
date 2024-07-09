import os
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import json


def get_tweets(username, days=30):
    url = f"https://twitter.com/{username}"
    # Path to your Chrome profile
    chrome_profile_path = os.path.expanduser('~/.config/google-chrome/Profile')

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={chrome_profile_path}")
    options.add_argument("start-maximized")

    # Initialize the WebDriver with the existing profile
    driver = webdriver.Chrome(options=options)

    # Open the user's Twitter profile
    driver.get(url)

    # Wait until the tweets are loaded
    wait = WebDriverWait(driver, 20)

    tweet_selector = 'article[role="article"]'
    last_height = driver.execute_script("return document.body.scrollHeight")
    tweets_data = []

    # Set the cutoff date
    cutoff_date = datetime.now() - timedelta(days=days)

    while True:
        # Find tweets on the page
        elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, tweet_selector)))
        for elem in elements:
            try:
                tweet_text = elem.text
                images = elem.find_elements(By.CSS_SELECTOR, 'img')
                videos = elem.find_elements(By.CSS_SELECTOR, 'video')

                # Filter out unnecessary images
                tweet_images = [img.get_attribute('src') for img in images if
                                'emoji' not in img.get_attribute('src')] # and 'profile_images' not in img.get_attribute('src')]

                # Get video URLs
                tweet_videos = [video.get_attribute('src') for video in videos if video.get_attribute('src')]

                # Extract the tweet date
                date_elements = elem.find_elements(By.CSS_SELECTOR, 'time')
                tweet_date = None
                if date_elements:
                    date_str = date_elements[0].get_attribute('datetime')
                    tweet_date = datetime.fromisoformat(date_str[:-1])  # Remove the 'Z' at the end for proper parsing

                # Check if the tweet date is within the specified range
                if tweet_date and tweet_date < cutoff_date:
                    # print(f"Reached tweets older than {days} days.")
                    # # Print the collected tweets in JSON format
                    # for tweet in tweets_data:
                    #     print(json.dumps(tweet, indent=4, default=str))

                    # or add into database


                    input("Press Enter to close the browser...")
                    # Close the browser
                    driver.quit()
                    return tweet_date

                # Extract hashtags
                hashtags = [part for part in tweet_text.split() if part.startswith('#')]

                links = [part for part in tweet_text.split() if part.startswith("https")]

                # Check if the tweet is a repost or self-repost
                reposted = 'reposted' in tweet_text
                # self_repost = 'self' in tweet_text.lower()

                # Check if the tweet is pinned
                pinned = 'Pinned' in tweet_text

                tweet_data = {
                    'text': tweet_text,
                    'images': tweet_images,
                    'videos': tweet_videos,
                    'date': tweet_date,
                    'hashtags': hashtags,
                    'links': links,
                    'reposted': 'yes' if reposted else 'no',
                    'pinned': 'yes' if pinned else 'no'
                }

                if tweet_data not in tweets_data:
                    tweets_data.append(tweet_data)
            except StaleElementReferenceException:
                # Handle the case where the element becomes stale
                continue

        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for new tweets to load

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


# username = input("Enter username: ")
# days = int(input("Enter the number of days to fetch tweets for: "))
# fetch_tweets(username, days)
