import json
import os
import random
import string
import time
import requests
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

SETTINGS_FILE = "settings.json"
ACCOUNTS_FILE = "accounts.txt"

# === توليد إيميل عشوائي ===
def generate_email():
    prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{prefix}@gmail.com"

# === حفظ الإعدادات في ملف JSON ===
def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

# === تحميل الإعدادات من ملف JSON أو إدخالها يدويًا ===
def load_or_ask_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    else:
        settings = {
            "REF_ID": input("🔗 Enter your referral ID: ").strip(),
            "PASSWORD": input("🔐 Enter the password to use for all accounts: ").strip(),
            "NUM_ACCOUNTS": int(input("🔢 How many accounts do you want to register? ")),
            "NUM_THREADS": int(input("🚀 Threads to use: "))
        }
        save_settings(settings)
        return settings

# === إعداد متصفح جديد ===
def create_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.binary_location = os.path.join(os.getcwd(), "chromium", "chrome.exe")
    driver_path = os.path.join(os.getcwd(), "chromedriver.exe")
    service = Service(executable_path=driver_path)
    return webdriver.Chrome(service=service, options=options)

# === تسجيل حساب داخل متصفح نشط ===
def register_account(driver, index, ref_id, password):
    try:
        start_time = time.time()

        driver.get(f"https://gamersunivers.com/?ref={ref_id}")
        time.sleep(2)
        driver.get("https://gamersunivers.com/page/register.html")
        time.sleep(2)

        token_input = driver.find_element(By.ID, "regToken")
        token = token_input.get_attribute("value")

        cookies = driver.get_cookies()

        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        email = generate_email()
        payload = {
            "a": "register",
            "token": token,
            "password": password,
            "password2": password,
            "email": email,
            "tos": "true",
            "recaptcha": ""
        }

        response = session.post("https://gamersunivers.com/system/ajax.php", data=payload)
        elapsed = time.time() - start_time
        print(f"[{index}] 📨 {email} → {response.text} ({elapsed:.2f}s)")

        # احفظ الإيميل في ملف
        with open(ACCOUNTS_FILE, "a") as f:
            f.write(email + "\n")

        driver.delete_all_cookies()
        driver.refresh()
        time.sleep(1)

    except Exception as e:
        print(f"[{index}] ❌ Error:", e)

# === تنفيذ الحسابات داخل كل ثريد ===
def thread_worker(start_index, count, ref_id, password):
    driver = create_driver()
    for i in range(count):
        register_account(driver, start_index + i + 1, ref_id, password)
    driver.quit()

def start_threads(settings):
    total_start = time.time()
    num_accounts = settings["NUM_ACCOUNTS"]
    num_threads = settings["NUM_THREADS"]
    ref_id = settings["REF_ID"]
    password = settings["PASSWORD"]

    accounts_per_thread = num_accounts // num_threads
    remainder = num_accounts % num_threads

    threads = []
    current_index = 0
    for i in range(num_threads):
        count = accounts_per_thread + (1 if i < remainder else 0)
        t = Thread(target=thread_worker, args=(current_index, count, ref_id, password))
        threads.append(t)
        t.start()
        current_index += count

    for t in threads:
        t.join()

    total_elapsed = time.time() - total_start
    print(f"\n✅ All accounts registered in {total_elapsed:.2f} seconds.")
    print(f"📄 Saved emails to: {ACCOUNTS_FILE}")

if __name__ == "__main__":
    settings = load_or_ask_settings()
    start_threads(settings)
