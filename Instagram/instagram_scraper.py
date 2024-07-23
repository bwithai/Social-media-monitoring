import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import logging
from pymongo import MongoClient
from bs4 import BeautifulSoup

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['instagram']
collection = db['posts']

# Set up the WebDriver
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Function to log into Instagram
def login_instagram(username, password):
    driver.get("https://www.instagram.com/")
    time.sleep(3)  # Allow time for the login page to load
    logger.debug("Instagram login page loaded")

    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    
    time.sleep(5)  # Allow time for login to process
    logger.debug("Logged in to Instagram")

# Function to fetch data from a profile
def fetch_profile_data(profile_url):
    driver.get(profile_url)
    time.sleep(3)  # Allow time for the profile page to load
    logger.debug(f"Opened profile URL: {profile_url}")

    post_links = set()  # Use a set to avoid duplicates
    last_height = driver.execute_script("return document.body.scrollHeight")
    logger.debug(f"Initial page height: {last_height}")

    while True:
        posts = driver.find_elements(By.XPATH, "//a[contains(@href, '/p/')]")
        for post in posts:
            post_links.add(post.get_attribute('href'))

        logger.debug(f"Found {len(posts)} posts, total {len(post_links)} unique links collected")

        # Scroll down to load more posts
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait for new posts to load

        # Check if we have reached the bottom of the page
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        logger.debug(f"Scrolled to new height: {new_height}")

    profile_data = []
    for link in post_links:
        driver.get(link)
        time.sleep(2)  # Allow time for the post page to load
        logger.debug(f"Opened post URL: {link}")

        # Extract post information
        try:
            # Use BeautifulSoup to parse the page source
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Check if the post is a photo or video
            media_type = "photo"
            media_url = ""
            if soup.find('video'):
                media_type = "video"
                media_url = soup.find('video')['src']
            elif soup.find('meta', property='og:image'):
                media_url = soup.find('meta', property='og:image')['content']
            else:
                media_url = driver.find_element(By.XPATH, "//img").get_attribute('src')

            # Extract caption
            caption = ""
            caption_element = soup.find('div', {'role': 'button'}).find('span')
            if caption_element:
                caption = caption_element.text

            # Extract hashtags
            hashtags = [a.text for a in soup.find_all('a') if '/explore/tags/' in a['href']]

            post_data = {
                'link': link,
                'type': media_type,
                'media_url': media_url,
                'caption': caption,
                'hashtags': hashtags,
                'profile_url': profile_url
            }

            logger.info(f"Fetched post data: {post_data}")
            profile_data.append(post_data)

            # Save to MongoDB
            collection.insert_one(post_data)
        except Exception as e:
            logger.error(f"Error fetching post data for {link}: {e}")
            logger.error(f"Page source: {driver.page_source}")

    return profile_data

# Main execution
if __name__ == "__main__":
    username = 'zainnoor179'
    password = 'zainnoor179@123'
    
    profile_urls = [
        'https://www.instagram.com/zainnoor179/?hl=en',
    ]

    # Log in to Instagram
    login_instagram(username, password)

    # Fetch data for each profile
    for profile_url in profile_urls:
        logger.info(f"Fetching data for profile: {profile_url}")
        profile_data = fetch_profile_data(profile_url)

        # Print the fetched data
        for data in profile_data:
            logger.info(data)

    # Close the WebDriver
    driver.quit()
