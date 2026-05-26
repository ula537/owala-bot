from datetime import datetime
import requests
from playwright.sync_api import sync_playwright

# ===== Telegram =====
TOKEN = "8183572724:AAH8H7-VQwfkQZm4DCCNiwaC9oAWt6E_3SQ"
CHAT_ID = "8806826310"

# ===== 商品網址 =====
PRODUCT_URL = "https://www.finders.com.tw/products/owala-freesip-tritan-25oz"

# ===== 發送 Telegram =====
def send_telegram(message):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=data)

# ===== 檢查庫存 =====
def check_stock():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        page.goto(
            PRODUCT_URL,
            wait_until="domcontentloaded",
            timeout=30000
        )

        page.wait_for_timeout(5000)

        html = page.content()

        browser.close()

        in_stock = (
            "加入購物車" in html
            and "售完" not in html
            and "貨到通知" not in html
        )

        return in_stock

# ===== 執行 =====
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print(f"[{now}] 檢查中...")

try:

    in_stock = check_stock()

    if in_stock:

        print("🔥 有貨")

        send_telegram(
            f"🔥 Owala 補貨啦！\n\n"
            f"時間：{now}\n"
            f"{PRODUCT_URL}"
        )

    else:

        print("❌ 沒貨")

except Exception as e:

    print("錯誤:", e)
