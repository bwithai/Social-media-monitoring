import os
import pprint
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException, \
    ElementClickInterceptedException, ElementNotInteractableException

from utils import clean_fb_post_text


def remove_duplicates(images):
    unique_images = []
    seen_urls = set()
    for img_url in images:
        if img_url not in seen_urls:
            if "https://" in img_url:
                unique_images.append(img_url)
                seen_urls.add(img_url)
    return unique_images


def get_fb_posts(username, days=30):
    url = f"https://www.facebook.com/{username}"
    chrome_profile_path = os.path.expanduser('~/.config/google-chrome/Profile')

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={chrome_profile_path}")
    options.add_argument("start-maximized")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)
    driver.get(url)

    SCROLL_PAUSE_TIME = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    seen_posts = set()
    collected_data = []

    while True:
        try:
            posts = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z"))
            )

            new_posts_found = False

            if posts:
                for post in posts:
                    try:
                        # Check for "See more" button and click it
                        try:
                            time.sleep(2)
                            see_more_button = post.find_element(By.XPATH, './/div[contains(text(), "See more")]')
                            driver.execute_script("arguments[0].scrollIntoView(true);", see_more_button)
                            driver.execute_script("arguments[0].click();", see_more_button)
                        except (
                                NoSuchElementException, ElementClickInterceptedException,
                                ElementNotInteractableException) as e:
                            print('', end='')
                            # pass  # Continue if no "See more" button or unable to click

                        description = post.text.strip()

                        if description in seen_posts:
                            continue

                        seen_posts.add(description)
                        new_posts_found = True

                        try:
                            datetime_element = post.find_element(By.XPATH,
                                                                 './/a[contains(@href, "timestamp")]/span/span')
                            post_datetime = datetime_element.get_attribute("title")
                        except NoSuchElementException:
                            post_datetime = None

                        links = list({part for part in description.split() if part.startswith("https")})

                        images = post.find_elements(By.CSS_SELECTOR, "img")
                        post_images = [img.get_attribute('src') for img in images if
                                       'emoji' not in img.get_attribute('src') and 'https://' in img.get_attribute(
                                           'src') and 'profile_images' not in img.get_attribute('src')]

                        hashtags = [part for part in description.split() if part.startswith('#')]

                        post_data = {
                            'original_description': description,
                            "clean_description": clean_fb_post_text(description),
                            'hashtags': hashtags,
                            "datetime": post_datetime,
                            "links": links,
                            "images": post_images
                        }
                        # pprint.pprint(post_data)
                        # print("+"*90)
                        #
                        # test = input("Press Enter to close the browser...")
                        # if test == "e":
                        #     driver.quit()
                        #     break
                        # else:
                        #     continue

                        collected_data.append(post_data)

                    except NoSuchElementException:
                        print("Some elements not found in the post")

            if len(collected_data) >= days:
                driver.quit()
                return collected_data

            driver.execute_script("window.scrollBy(0, window.innerHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height and not new_posts_found:
                break
            last_height = new_height

        except TimeoutException:
            print("Timed out waiting for posts to load by get_posts(FB)")
            break
        except WebDriverException as e:
            raise Exception(f"WebDriver error occurred by get_posts(FB): {e}")
        except Exception as e:
            print(f"An error occurred by get_posts(FB): {e}")
            break

    driver.quit()
    return collected_data

# Call the function to get Facebook posts
# get_fb_posts("bookaholicsco", 2){person_comment_text}
# data = get_fb_posts("agha.rameez.3", 10)
# pprint.pprint(data)
# print("total post scraped: ", len(data))
