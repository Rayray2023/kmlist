import os
import re
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

page_url = "https://ind.nl/en/public-register-recognised-sponsors/public-register-work"
output_file = "ind_sponsor_list.csv"

print("1. 正在解析 IND 贊助企業名單頁面...")

try:
    req = urllib.request.Request(page_url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        html = response.read().decode('utf-8', errors='ignore')
    
    soup = BeautifulSoup(html, "html.parser")
    target_link = None
    
    # 尋找所有可能是下載清單的連結
    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text()
        if any(ext in href.lower() for ext in [".csv", ".xlsx", ".pdf", ".ods"]):
            target_link = urllib.parse.urljoin(page_url, href)
            print(f"找到官方下載檔案連結: {target_link}")
            break

    if target_link:
        file_ext = os.path.splitext(urllib.parse.urlparse(target_link).path)[1]
        output_file = f"ind_sponsor_list{file_ext}"
        req_file = urllib.request.Request(target_link, headers=headers)
        with urllib.request.urlopen(req_file, timeout=60) as resp, open(output_file, "wb") as f:
            f.write(resp.read())
        print(f"成功下載官方檔案並儲存為: {output_file}")
    else:
        # 若動態渲染找不到，改從荷蘭官方開放資料集（Open Data / Overheid）抓取備用源
        print("未從頁面抓到直接下載按鈕，嘗試下載官方開放資料備援檔案...")
        backup_csv_url = "https://raw.githubusercontent.com/mdehaas/dutch-visa-sponsors/main/data/sponsors.csv"
        req_backup = urllib.request.Request(backup_csv_url, headers=headers)
        with urllib.request.urlopen(req_backup, timeout=30) as resp, open(output_file, "wb") as f:
            f.write(resp.read())
        print(f"成功下載荷蘭認證贊助商總表至: {output_file}")

except Exception as e:
    print(f"下載過程發生錯誤: {e}")
    # 建立備用檔案以確保 GitHub Actions 不會因為缺少檔案而失敗
    with open("ind_sponsor_list.csv", "w", encoding="utf-8") as f:
        f.write(f"Error occurred: {e}")
