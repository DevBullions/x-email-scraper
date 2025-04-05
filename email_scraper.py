import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import os


def start_driver(headless=False):
    # ✅ Define a consistent user data directory
    user_data_dir = os.path.join(os.getcwd(), "x_scraper_profile")

    options = Options()

    if headless:
        options.add_argument("--headless=new")

    # Chrome crash preventers
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--remote-debugging-port=9222")

    # ✅ Persist profile directory so login is saved
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument("--profile-directory=Default")  # Can change if you want multiple

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    return driver


def scroll_and_collect(driver, max_wait=3):
    emails = set()
    last_height = driver.execute_script("return document.body.scrollHeight")
    stagnant_scrolls = 0

    while True:
        # Scroll to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Get tweets and extract emails
        tweets = driver.find_elements(By.XPATH, '//div[@data-testid="tweetText"]')
        for tweet in tweets:
            found_emails = extract_emails(tweet.text)
            emails.update(found_emails)

        # Check if we’ve reached the bottom
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            stagnant_scrolls += 1
            if stagnant_scrolls >= max_wait:  # If same height 3 times, assume end
                break
        else:
            stagnant_scrolls = 0
            last_height = new_height

    return list(emails)


def extract_emails(text):
    # Regular expression for matching email addresses
    email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return re.findall(email_regex, text)


def save_to_csv(emails):
    # Create a DataFrame
    df = pd.DataFrame(emails, columns=['Email'])

    # Check if emails.csv exists, and create a new filename
    filename = "emails.csv"
    file_counter = 1
    while os.path.exists(filename):
        filename = f"emails{file_counter}.csv"
        file_counter += 1

    # Save the emails to CSV
    df.to_csv(filename, index=False)
    print(f"📧 Emails saved to: {filename}")



def scrape_tweet_replies(tweet_url):
    print(f"💬 Scraping replies from tweet: {tweet_url}")
    driver = start_driver(headless=False)
    driver.get(tweet_url)

    print("🔐 Please log in and scroll through replies...")
    input("👉 Press Enter here once you're done scrolling and ready to scrape:\n")

    emails = scroll_and_collect(driver)  # Fixed to match the new function
    driver.quit()
    return emails



def scrape_profile(username):
    print(f"📌 Scraping profile: @{username}")
    driver = start_driver(headless=False)
    driver.get(f"https://x.com/{username}")
    time.sleep(5)
    emails = scroll_and_collect(driver, scroll_times=20)
    driver.quit()
    return emails

def scrape_hashtag(hashtag):
    print(f"📌 Scraping hashtag: #{hashtag}")
    driver = start_driver(headless=False)
    driver.get(f"https://x.com/search?q=%23{hashtag}&src=typed_query")
    time.sleep(5)
    emails = scroll_and_collect(driver, scroll_times=20)
    driver.quit()
    return emails

if __name__ == "__main__":
    print("📬 EMAIL SCRAPER FOR TWITTER/X (No API Needed)")
    print("1. Scrape from tweet replies")
    print("2. Scrape from a user profile")
    print("3. Scrape from hashtag")

    choice = input("Choose option (1/2/3): ")

    if choice == "1":
        url = input("Enter tweet URL: ")
        emails = scrape_tweet_replies(url)
    elif choice == "2":
        username = input("Enter username (without @): ")
        emails = scrape_profile(username)
    elif choice == "3":
        tag = input("Enter hashtag (without #): ")
        emails = scrape_hashtag(tag)
    else:
        print("Invalid choice")
        exit()

    print("\n📧 Emails Found:")
    for email in emails:
        print(" -", email)

    save_to_csv(emails)
    print("✅ Done.")
