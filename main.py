import requests
from bs4 import BeautifulSoup
import urllib.parse

url = "https://ind.nl/en/public-register-recognised-sponsors/public-register-work"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

target_url = None
file_ext = ".pdf"

for link in soup.find_all("a", href=True):
    href = link["href"]
    if any(ext in href.lower() for ext in [".csv", ".xlsx", ".pdf"]):
        target_url = urllib.parse.urljoin(url, href)
        if ".csv" in href.lower():
            file_ext = ".csv"
        elif ".xlsx" in href.lower():
            file_ext = ".xlsx"
        break

if target_url:
    print(f"開始下載檔案: {target_url}")
    file_data = requests.get(target_url, headers=headers).content
    filename = f"ind_sponsor_list{file_ext}"
    with open(filename, "wb") as f:
        f.write(file_data)
    print(f"下載完成，已儲存為 {filename}")
else:
    print("未找到可下載的檔案連結。")
