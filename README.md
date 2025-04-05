
# 📬 X (Twitter) Email Scraper – No API Needed

This is a Python-based email scraper for Twitter (now X), using `selenium` and `BeautifulSoup`. It extracts email addresses from:

- 🧵 Tweet replies  
- 👤 User profiles  
- 🔥 Hashtag search results

## 🚀 Features

- No Twitter API or tokens required
- Uses real browser automation (via Selenium)
- Extracts and saves emails to CSV
- Headless mode supported
- Saves your browser session, so login persists

## 🛠 Requirements

- Python 3.7+
- Google Chrome
- `pip install -r requirements.txt`

## 📦 Installation

```bash
git clone https://github.com/devbullions/x-email-scraper.git
cd x-email-scraper
pip install -r requirements.txt



✅ Usage
bash
Copy
Edit
python main.py
Then choose:

1. Scrape from tweet replies
2. Scrape from a user profile
3. Scrape from hashtag
When prompted, to scroll through X automatic, then hit Enter to let it scrape.

📁 Output
All found emails are saved to a CSV file like:

python-repl
Copy
Edit
emails.csv
emails1.csv
...
🤖 Author
Built by Williams Divine. Contributions welcome. Let's upgrade together!
Also pls give a stars

🧠 TODO / Coming Soon
 Automatically scroll using bot

 Headless mode toggle via CLI

 GUI interface with Streamlit or Gradio

 Auto-login using cookies/session

 Export to JSON / Excel

⚠️ Note: Use ethically. This tool is for educational and outreach purposes only.


