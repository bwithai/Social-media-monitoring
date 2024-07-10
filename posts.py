from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os


def scroll_and_load(driver):
    scroll_pause_time = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def scrape_tiktok_posts(username):
    chrome_profile_path = os.path.expanduser(r'C:\Users\deskt\AppData\Local\Google\Chrome\User Data')

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={chrome_profile_path}")
    options.add_argument("--lang=en")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(f'https://www.tiktok.com/@{username}')

        # Wait until the tweets are loaded
        wait = WebDriverWait(driver, 20)

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            '#main-content-others_homepage > div > div.css-833rgq-DivShareLayoutMain.ee7zj8d4 > div.css-1qb12g8-DivThreeColumnContainer.eegew6e2'))
        )

        time.sleep(10)
        scroll_and_load(driver)

        post_data = []
        post_urls = []

        posts = driver.find_elements(By.CSS_SELECTOR,
                                     '#main-content-others_homepage > div > div.css-833rgq-DivShareLayoutMain.ee7zj8d4 > div.css-1qb12g8-DivThreeColumnContainer.eegew6e2 > div > div')
        for post in posts:
            try:
                video_url = post.find_element(By.CSS_SELECTOR, 'div.css-x6f6za-DivContainer-StyledDivContainerV2.eq741c50 a').get_attribute('href')
                post_urls.append(video_url)
            except Exception as e:
                print(f"Error extracting post URL: {e}")
                continue

        for post_url in post_urls:
            try:
                driver.get(post_url)
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'div.css-1elr43g-DivActionBarWrapper.eqrezik8'))
                )

                post_info = {}
                post_info['video_url'] = post_url
                post_info['description'] = driver.find_element(By.CSS_SELECTOR,
                                                               '#main-content-video_detail > div > div.css-12kupwv-DivContentContainer.ege8lhx2 > div.css-1senhbu-DivLeftContainer.ege8lhx3 > div.css-1sb4dwc-DivPlayerContainer.eqrezik4 > div.css-3lfoqn-DivDescriptionContentWrapper-StyledDetailContentWrapper.eqrezik16 > div.css-r4nwrj-DivVideoInfoContainer.eqrezik3 > div.css-bs495z-DivWrapper.e1mzilcj0 > div > h1 > span').text.strip()

                post_info['likes'] = driver.find_element(By.CSS_SELECTOR,
                                                         '#main-content-video_detail > div > div.css-12kupwv-DivContentContainer.ege8lhx2 > div.css-1senhbu-DivLeftContainer.ege8lhx3 > div.css-1sb4dwc-DivPlayerContainer.eqrezik4 > div.css-704ozy-DivVideoContainer.eqrezik7 > div.css-1elr43g-DivActionBarWrapper.eqrezik8 > div.css-1npmxy5-DivActionItemContainer.er2ywmz0 > button:nth-child(1) > strong').text

                post_info['comments'] = driver.find_element(By.CSS_SELECTOR,
                                                            '#main-content-video_detail > div > div.css-12kupwv-DivContentContainer.ege8lhx2 > div.css-1senhbu-DivLeftContainer.ege8lhx3 > div.css-1sb4dwc-DivPlayerContainer.eqrezik4 > div.css-704ozy-DivVideoContainer.eqrezik7 > div.css-1elr43g-DivActionBarWrapper.eqrezik8 > div.css-1npmxy5-DivActionItemContainer.er2ywmz0 > button:nth-child(2) > strong').text

                post_info['shares'] = driver.find_element(By.CSS_SELECTOR,
                                                          '#main-content-video_detail > div > div.css-12kupwv-DivContentContainer.ege8lhx2 > div.css-1senhbu-DivLeftContainer.ege8lhx3 > div.css-1sb4dwc-DivPlayerContainer.eqrezik4 > div.css-704ozy-DivVideoContainer.eqrezik7 > div.css-1elr43g-DivActionBarWrapper.eqrezik8 > div.css-1npmxy5-DivActionItemContainer.er2ywmz0 > button:nth-child(4) > strong').text

                description_container = driver.find_element(By.CSS_SELECTOR,
                                                            '#main-content-video_detail > div > div.css-12kupwv-DivContentContainer.ege8lhx2 > div.css-1senhbu-DivLeftContainer.ege8lhx3 > div.css-1sb4dwc-DivPlayerContainer.eqrezik4 > div.css-3lfoqn-DivDescriptionContentWrapper-StyledDetailContentWrapper.eqrezik16 > div.css-r4nwrj-DivVideoInfoContainer.eqrezik3 > div.css-bs495z-DivWrapper.e1mzilcj0 > div')
                hashtags = description_container.find_elements(By.CSS_SELECTOR, 'h1 > a')

                all_hashtags = []
                for hashtag in hashtags:
                    all_hashtags.append(hashtag.text)

                post_info['hashtags'] = all_hashtags

                post_data.append(post_info)
                driver.back()
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,
                                                    '#main-content-others_homepage > div > div.css-833rgq-DivShareLayoutMain.ee7zj8d4 > div.css-1qb12g8-DivThreeColumnContainer.eegew6e2'))
                )

            except Exception as e:
                print(f"Error extracting post data: {e}")
                continue

        json_filename = f'tiktok_posts.json'
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(post_data, f, ensure_ascii=False, indent=4)

        print(f"Posts saved to {json_filename}")

    finally:
        driver.quit()


username = input("Enter TikTok username: ")
scrape_tiktok_posts(username)
