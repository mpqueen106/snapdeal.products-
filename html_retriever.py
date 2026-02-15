import time
import re
from datetime import datetime
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# ================= CONFIG =================
OUTPUT_CSV = "snapdeal_products.csv"
HEADLESS = False
WAIT_TIME = 15
MAX_PRODUCTS = 10

URLS = {
    "Accessories": "https://www.snapdeal.com/search?keyword=accessories&sort=rlvncy",
    "Footwear": "https://www.snapdeal.com/search?keyword=footwear&sort=rlvncy",
    "Men Clothing": "https://www.snapdeal.com/search?keyword=men%20clothing&sort=rlvncy",
}
# ==========================================


# ---------- DRIVER SETUP ----------
options = Options()

if HEADLESS:
    options.add_argument("--headless=new")

options.add_argument("--start-maximized")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Prevent blocking
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/114.0.0.0 Safari/537.36"
)

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, WAIT_TIME)


# ---------- FUNCTIONS ----------
def parse_rating(style):
    if not style:
        return ""
    match = re.search(r"(\d+(?:\.\d+)?)%", style)
    if match:
        return round(float(match.group(1)) / 20, 1)
    return ""


def scrape_page(section):
    products = []

    try:
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-tuple-listing"))
        )
    except TimeoutException:
        print("No products found")
        return products

    cards = driver.find_elements(By.CSS_SELECTOR, "div.product-tuple-listing")

    for card in cards[:MAX_PRODUCTS]:
        try:
            name = card.find_element(By.CSS_SELECTOR, "p.product-title").text
        except:
            name = ""

        try:
            price = card.find_element(By.CSS_SELECTOR, "span.product-price").text
        except:
            price = ""

        try:
            rating_style = card.find_element(By.CSS_SELECTOR, ".filled-stars").get_attribute("style")
            rating = parse_rating(rating_style)
        except:
            rating = ""

        try:
            img = card.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
        except:
            img = ""

        try:
            url = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        except:
            url = ""

        products.append({
            "Scraped At": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Section": section,
            "Product Name": name,
            "Price": price,
            "Rating": rating,
            "Image URL": img,
            "Product URL": url,
        })

    return products


# ================= MAIN =================
all_data = []

for section, link in URLS.items():
    print(f"\nScraping {section}...")
    driver.get(link)
    time.sleep(3)

    data = scrape_page(section)
    all_data.extend(data)

# ---------- SAVE CSV ----------
df = pd.DataFrame(all_data)
df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

print("\n✅ Finished Successfully!")
print(f"File saved as: {OUTPUT_CSV}")

driver.quit()