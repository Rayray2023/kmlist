import requests
from bs4 import BeautifulSoup
import urllib.parse

url = "https://ind.nl/en/public-register-recognised-sponsors/public-register-work"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 尋找所有可能是下載清單的連結 (.csv, .xlsx, .pdf)
print("尋找官方完整名單下載連結：")
for link in soup.find_all("a", href=True):
    href = link["href"]
    if any(ext in href.lower() for ext in [".csv", ".xlsx", ".pdf", "register"]):
        full_url = urllib.parse.urljoin(url, href)
        print(f"- 連結文字: {link.text.strip()} | 下載網址: {full_url}")
