import os
import pprint
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager


# Function to fetch data from a profile
def fetch_profile_data(profile_url, max_posts):
    # Path to your Chrome profile
    chrome_profile_path = os.path.expanduser('~/.config/google-chrome/Profile')

    options = Options()
    options.add_argument(f"user-data-dir={chrome_profile_path}")
    options.add_argument("--start-maximized")

    # Initialize the WebDriver with the existing profile
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(profile_url)

    # Wait until the posts are loaded
    wait = WebDriverWait(driver, 20)

    post_links = set()  # Use a set to avoid duplicates
    last_height = driver.execute_script("return document.body.scrollHeight")

    while len(post_links) < max_posts:
        posts = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, '/p/')]")))
        for post in posts:
            post_links.add(post.get_attribute('href'))
            if len(post_links) >= max_posts:
                break

        # Scroll down to load more posts
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait for new posts to load

        # Check if we have reached the bottom of the page
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    insta_profile_posts = []

    for link in list(post_links)[:max_posts]:
        driver.get(link)
        time.sleep(2)  # Allow time for the post page to load

        # Extract post information
        try:
            # Use BeautifulSoup to parse the page source
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Check if the post is a photo or video
            media_url = ""
            media_element = soup.find('meta', property='og:image')
            if media_element:
                media_url = media_element['content']
            else:
                media_url = driver.find_element(By.XPATH, "//img").get_attribute('src')

            # Extract caption
            caption = ""
            caption_element = soup.find('span',
                                        class_='x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs xt0psk2 x1i0vuye xvs91rp xo1l8bm x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj')
            if caption_element:
                caption = caption_element.text

            # Extract hashtags
            hashtags = [a.text for a in soup.find_all('a') if '/explore/tags/' in a['href']]

            post_data = {
                'link': link,
                'media_url': media_url,
                'caption': caption,
                'hashtags': hashtags,
                'profile_url': profile_url
            }

            insta_profile_posts.append(post_data)
            pprint.pprint(post_data)
            # print('-' * 90)
        except Exception as e:
            print(f"Error fetching post data for {link}: {e}")
            print(f"Page source: {driver.page_source}")

    driver.quit()
    return insta_profile_posts


# Main execution
if __name__ == "__main__":
    url = "https://www.instagram.com/zainnoor179/?hl=en"

    # Fetch the first 3 posts
    profile_data = fetch_profile_data(url, max_posts=3)
    # pprint.pprint(profile_data)