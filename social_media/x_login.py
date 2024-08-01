import os
from selenium import webdriver

# Path to your Chrome profile
chrome_profile_path = os.path.expanduser('~/.config/google-chrome/Profile')

options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={chrome_profile_path}")
options.add_argument("start-maximized")

# Initialize the WebDriver with the existing profile
driver = webdriver.Chrome(options=options)

url = f"https://x.com/"
driver.get(url)

input("Press Enter to close the browser...")
# Close the browser
driver.quit()

# jalalayn, Jalalhaddad
