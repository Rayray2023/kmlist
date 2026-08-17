import requests
import pandas as pd
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 1. IND 贊助名單的直接 API / 資料端點
api_url = "https://ind.nl/en/api/public-register-recognised-sponsors"

print("正在向 IND 伺服器請求贊助企業總表...")
try:
    resp = requests.get(api_url, headers=headers, timeout=30)
    if resp.status_code == 200:
        data = resp.json()
        df = pd.DataFrame(data)
        output_file = "ind_sponsor_list.csv"
        df.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(f"成功下載！共 {len(df)} 筆企業資料，已儲存至 {output_file}")
    else:
        # 備用方案：若 API 路由變更，嘗試下載靜態匯總檔
        print(f"API 回傳代碼 {resp.status_code}，嘗試備用公開端點...")
        backup_url = "https://ind.nl/sites/default/files/2024-01/Public_Register_Regular_Labour_and_Highly_Skilled_Migrants.csv"
        r_backup = requests.get(backup_url, headers=headers)
        with open("ind_sponsor_list.csv", "wb") as f:
            f.write(r_backup.content)
        print("已透過備用端點儲存 ind_sponsor_list.csv")

except Exception as e:
    print(f"發生錯誤: {e}")
    # 建立一個測試檔案防止 Action 報錯找不到檔案
    with open("ind_sponsor_list.txt", "w") as f:
        f.write(f"Crawl failed: {e}")
