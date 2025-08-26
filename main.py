import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime


conn = sqlite3.connect("news.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS headlines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    headline TEXT,
    date_scraped TEXT
)
""")
conn.commit()


url = "https://inshorts.com/en/read"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

headlines = soup.find_all("span", itemprop="headline")

for h in headlines[:10]:  # Top 10
    title = h.get_text(strip=True)
    cursor.execute("INSERT INTO headlines (headline, date_scraped) VALUES (?, ?)",
                   (title, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

conn.commit()

cursor.execute("SELECT * FROM headlines")
rows = cursor.fetchall()

print("\n--- Latest Headlines ---\n")
for row in rows:
    print(f"{row[0]}. {row[1]}")

conn.close()
