import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def do_impression_on(tweet_url, reply_message):
    response = ""
    # Path to your Chrome profile
    chrome_profile_path = os.path.expanduser('~/.config/google-chrome/Profile')

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={chrome_profile_path}")
    options.add_argument("start-maximized")

    # Initialize the WebDriver with the existing profile
    driver = webdriver.Chrome(options=options)

    try:
        # Open the tweet URL
        driver.get(tweet_url)

        # Wait until the like button is loaded
        wait = WebDriverWait(driver, 20)

        # Locate the like button
        like_button = wait.until(
            EC.presence_of_element_located((By.XPATH, '//button[@aria-label[contains(., "Like")]]'))
        )

        # Locate the repost button
        repost_button = wait.until(
            EC.presence_of_element_located((By.XPATH, '//button[@aria-label[contains(., "Repost")]]'))
        )

        # Check if the tweet is already liked
        aria_label = like_button.get_attribute("aria-label")
        if "liked" not in aria_label.lower():
            driver.execute_script("arguments[0].click();", like_button)
            response += "Tweet liked.\n"
            time.sleep(3)
        else:
            response += "Tweet already liked.\n"

        # Check if the tweet is already reposted
        aria_label = repost_button.get_attribute("aria-label")
        if "reposted" not in aria_label.lower():
            driver.execute_script("arguments[0].click();", repost_button)
            time.sleep(1)
            confirm_retweet_button = wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-testid='retweetConfirm']"))
            )
            driver.execute_script("arguments[0].click();", confirm_retweet_button)
            time.sleep(2)
            response += "Tweet reposted.\n"
        else:
            response += "Tweet already reposted.\n"

        # Wait for potential overlays to disappear
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div[data-testid="twc-cc-mask"]'))
        )

        # Wait and enter the reply message
        reply_text_area = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//div[@aria-label="Post text"]'))
        )
        driver.execute_script("arguments[0].click();", reply_text_area)

        # Enter the reply message with a delay between each keystroke
        for char in reply_message:
            reply_text_area.send_keys(char)
            time.sleep(0.1)  # Adjust the delay as needed

        # Locate and click the send reply button
        send_reply_button = wait.until(
            EC.element_to_be_clickable((By.XPATH,
                                        '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[1]/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div[2]/div/div/div/button'))
        )
        time.sleep(2)
        send_reply_button.click()
        # driver.execute_script("arguments[0].click();", send_reply_button)
        response += "Reply sent."

        time.sleep(5)
        driver.quit()
        return response

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.quit()
        return response


# Example usage
# tweet_url = "https://x.com/elonmusk/status/1804188196546449660"  # Replace with the actual tweet URL
# tweet_url = "https://x.com/elonmusk/status/1479236333516165121"  # Replace with the actual tweet URL
# reply_message = "exactly it is"  # Replace with the actual reply message
# do_impression_on(tweet_url, reply_message)
