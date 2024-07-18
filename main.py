import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def remove_duplicates(images):
    unique_images = []
    seen_urls = set()
    for img_url in images:
        if img_url not in seen_urls:
            if "https://" in img_url:
                unique_images.append(img_url)
                seen_urls.add(img_url)
    return unique_images


def get_fb_posts():
    # Path to your Chrome profile on Windows
    chrome_profile_path = os.path.expanduser(
        'C:\\Users\\pc\\AppData\\Local\\Google\\Chrome\\User Data\\Facebook-Profile')

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={chrome_profile_path}")
    options.add_argument("start-maximized")

    # Initialize the WebDriver with the existing profile
    driver = webdriver.Chrome(options=options)

    # Wait until the posts are loaded
    wait = WebDriverWait(driver, 20)

    # Open Facebook page
    driver.get("https://www.facebook.com/bookaholicsco")

    SCROLL_PAUSE_TIME = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    seen_posts = set()
    collected_data = []

    while True:
        try:
            # Wait until the posts are loaded using the specific CSS selector
            posts = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z")))

            new_posts_found = False

            if posts:
                # Iterate through each post element
                for post in posts:
                    try:
                        # Extract post description
                        description = post.text.strip()

                        # Check for duplicates
                        if description in seen_posts:
                            continue

                        seen_posts.add(description)
                        new_posts_found = True

                        # Extract datetime (if available)
                        try:
                            datetime_element = post.find_element(By.XPATH, './/a[contains(@href, "timestamp")]/span/span')
                            post_datetime = datetime_element.get_attribute("title")
                        except NoSuchElementException:
                            post_datetime = None

                        # Extract links (if available)
                        links = post.find_elements(By.CSS_SELECTOR, "a")
                        post_links = [link.get_attribute("href") for link in links if link.get_attribute("href")]

                        # Extract images (if available)
                        images = post.find_elements(By.CSS_SELECTOR, "img")
                        post_images = [img.get_attribute("src") for img in images if img.get_attribute("src")]

                        post_data = {
                            "Description": description,
                            "Datetime": post_datetime,
                            "Links": post_links,
                            "Images": remove_duplicates(post_images)
                        }

                        collected_data.append(post_data)

                    except NoSuchElementException:
                        print("Some elements not found in the post")

            # Scroll down to the bottom of the page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load the page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height and not new_posts_found:
                break
            last_height = new_height

        except TimeoutException:
            print("Timed out waiting for posts to load")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    driver.quit()

    # Save collected data to a JSON file
    with open('facebook_posts.json', 'w', encoding='utf-8') as f:
        json.dump(collected_data, f, ensure_ascii=False, indent=4)


# Call the function to get Facebook posts
get_fb_posts()
