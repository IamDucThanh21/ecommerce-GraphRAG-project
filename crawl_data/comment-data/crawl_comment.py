import csv
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import pandas as pd

# --- 1. SETUP ---
def setup_driver():
    options = Options()
    options.add_argument("--headless=new") # Remove this line to watch the browser work
    options.add_argument("--window-size=1920,1080")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=options)
    
    stealth(driver,
        languages=["vi-VN", "vi"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    return driver

def get_all_comments(driver, sku):
    """Get all comments: [username, num_star, content]"""

    comments_data = []

    try:
        # wait render after click seemore
        time.sleep(3)

        comments = driver.find_elements(
            By.CSS_SELECTOR,
            ".boxReview-comment-item"
        )

        for comment in comments:
            try:
                # Name
                name = ""

                name_el = comment.find_elements(By.CSS_SELECTOR,".block-info__name .name")

                if name_el:
                    name = name_el[0].get_attribute("textContent").strip()

                # Number of stars
                num_star = str(len(comment.find_elements(By.CSS_SELECTOR,".item-review-rating__star .icon.is-active")))

                # Comment content
                content = ""

                content_el = comment.find_elements(By.CSS_SELECTOR,".comment-content p")

                if content_el:
                    content = content_el[0].get_attribute("textContent").strip()

                # Date time reaction
                date_time = ""

                date_el = comment.find_elements(By.CSS_SELECTOR,".date-time")

                if date_el:
                    date_time = date_el[0].get_attribute("textContent").strip()

                    # Remove extra whitespace/newline
                    date_time = " ".join(date_time.split())

                # Tags
                tags = []

                tag_elements = comment.find_elements(By.CSS_SELECTOR,".item-review-rating__item-attribute")

                for tag in tag_elements:
                    tag_text = tag.get_attribute("textContent").strip()

                    if tag_text:
                        tags.append(" ".join(tag_text.split()))

                comments_data.append({
                    'sku': sku,
                    'name_create': name,
                    'content': content,
                    'num_star': num_star,
                    'date_time': date_time,
                    'tags': '|'.join(tags)
                })

            except Exception as e:
                print(f"Skip comment: {e}")

    except Exception as e:
        print(f"Error getting comments: {e}")

    # driver.close()
    # driver.switch_to.window(driver.window_handles[0])

    return comments_data

def get_comment_urls(driver, wait, sku):
    """Clicks 'Xem thêm' until all products are loaded, then returns all URLs."""
    print("Loading all comments...")
    driver.get(f"https://cellphones.com.vn/{sku}/review")
    time.sleep(5) # Initial load

    while True:
        try:
            # Find 'Xem thêm đánh giá' button
            load_more_btn = driver.find_elements(By.CSS_SELECTOR,"a.button__view-more-review.load-more")

            if load_more_btn and load_more_btn[0].is_displayed():

                # Scroll to button
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",load_more_btn[0])
                time.sleep(1)

                # Click using JS
                driver.execute_script("arguments[0].click();",load_more_btn[0])

                # print("Clicked 'Xem thêm đánh giá'...")

                # Wait render new comments
                time.sleep(2)

            else:
                # print("No more 'Xem thêm đánh giá' button found.")
                break

        except Exception as e:
            print(f"Finished loading reviews or error: {e}")
            break
    

    # return get_all_comments(driver)

# --- 5. MAIN LOOP ---
def main():
    driver = setup_driver()
    wait = WebDriverWait(driver, 20)

    brand_list = [
        # 'apple', 'sony', 'jbl', 'samsung', 'soundpeats', 'xiaomi',
        # 'marshall', 'anker', 'havit', 'edifier', 'huawei', 'baseus',
        # 'shokz', 'bose', 'oppo', 'sennheiser', 'hyperx', 'trusmi',
        # 'asus', 'alpha-works', 'soul', 'earfun', 'kz', 'dareu',                      done
        # 'riversong', 'logitech', 'robot', 'devia', 'divoom', 'aukey',
        # 'oneodio', 'beats', 'nothing', 'qcy', 'stargo', 'ugreen',
        'tronsmart', 'realme', 'fender', 'akg', 'bowers-wilkins',
        'nakamichi', 'goojodoq'
    ]
    # smartphone= ['sony', 'tecno', 'xiaomi', 'apple', 'honor', 'huawei', 'infinix', 'itel', 'masstel', 'meizu', 'nokia', 'nubia', 'oppo', 'realme', 'samsung'] 
    # laptop = ['acer', 'apple', 'asus','dell','gigabyte','hp','lenovo','lg','msi','samsung','surface']
    # tablet = ['boox', 'honor', 'huawei', 'ipad', 'kindle', 'lenovo', 'may-doc-sach', 'nubia', 'oppo', 'samsung', 'teclast', 'xiaomi']

    fields = ['sku', 'name_create', 'content', 'num_star', 'date_time', 'tags']
    
    try:
        for brand in brand_list:
            print(f"Processing brand: {brand}")
            filename = f'crawl_data/comment-data/earphone-audio/cellphones_comment_{brand}.csv'
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()

                sku_csv_filename = f'crawl_data/data_v2/earphone-audio/cellphones_{brand}.csv'
                skus = pd.read_csv(sku_csv_filename)['sku'].tolist()
                
                for sku in skus:
                    get_comment_urls(driver, wait, sku)
                    comments = get_all_comments(driver, sku)
                    print(f"   Found {len(comments)} comments for SKU: {sku}")
                    for cmt in comments:
                        # print(cmt)
                        writer.writerow({
                            'sku': cmt['sku'],
                            'name_create': cmt['name_create'],
                            'content': cmt['content'],
                            'num_star': cmt['num_star'],
                            'date_time': cmt['date_time'],
                            'tags': cmt['tags']
                        })
                        f.flush()

                    print(f"----------Success: {sku}")
                    
                    # if comments:
                    #     writer.writerows(comments)
                    #     f.flush()
                    #     print(f"   Success: {comments['sku']}")

                    time.sleep(2)

    except Exception as e:
        print(f"Main Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()