import os
import pprint
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


# Function to fetch data from a profile
def fetch_profile_data(profile_url):
    # Path to your Chrome profile
    chrome_profile_path = os.path.expanduser('~/.config/google-chrome/Profile')

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={chrome_profile_path}")
    options.add_argument("start-maximized")

    # Initialize the WebDriver with the existing profile
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Wait until the tweets are loaded
    wait = WebDriverWait(driver, 20)

    post_links = set()  # Use a set to avoid duplicates
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        print(post_links)
        print(len(post_links))
        print("------------------------------------")
        if len(post_links) >= 3:
            pprint.pprint(post_links)
            break
        posts = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, '/p/')]")))
        for post in posts:
            post_links.add(post.get_attribute('href'))

        # Scroll down to load more posts
        driver.execute_script("window.scrollTo(0, window.innerHeight);")
        time.sleep(3)  # Wait for new posts to load

        # Check if we have reached the bottom of the page
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    insta_profile_posts = []
    for link in post_links:
        driver.get(link)
        time.sleep(2)  # Allow time for the post page to load

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
            caption_element = soup.find('div', class_='_a9zs')
            if caption_element:
                caption_h1 = caption_element.find('h1', class_='_ap3a _aaco _aacu _aacx _aad7 _aade')
                caption = caption_h1.text if caption_h1 else ""

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

            insta_profile_posts.append(post_data)

            # Save to MongoDB
            pprint.pprint(post_data)
            print('-' * 90)
            print('_' * 90)
            # collection.insert_one(post_data)
        except Exception as e:
            print(f"Error fetching post data for {link}: {e}")
            print(f"Page source: {driver.page_source}")

    return insta_profile_posts


# Main execution
if __name__ == "__main__":
    url = "https://www.instagram.com/mshir_azi78"

    profile_data = fetch_profile_data(url)
