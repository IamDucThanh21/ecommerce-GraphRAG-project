import csv
import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth

# --- 1. SETUP ---
def setup_driver():
    options = Options()
    options.add_argument("--headless=new") 
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

def crawl_comments(driver, wait):
    all_comment_data = []
    current_comment_count = 0

    try:
        # Initial scroll to comment section
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
        time.sleep(2)

        while True:
            # --- PHASE 1: Click "Show More" until it's gone ---
            while True:
                show_more_btns = driver.find_elements(By.CSS_SELECTOR, ".button__cmt-showmore")
                if show_more_btns and show_more_btns[0].is_displayed():
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", show_more_btns[0])
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", show_more_btns[0])
                    print("   Clicked 'Show More'...")
                    time.sleep(2) # Give it time to fetch data
                else:
                    break

            # --- PHASE 2: Extract current visible comments ---
            comment_items = driver.find_elements(By.CSS_SELECTOR, "#page_comment_list > .item-comment")
            
            # Only process new comments we haven't seen yet in this session
            for idx in range(current_comment_count, len(comment_items)):
                item = comment_items[idx]
                try:
                    # num_comment (Global count)
                    current_comment_count += 1
                    
                    # Main Comment
                    comment_el = item.find_element(By.CSS_SELECTOR, ".box-cmt__box-question .content")
                    comment_text = driver.execute_script("return arguments[0].textContent", comment_el).strip()
                    
                    # Replies
                    replies_dict = {}
                    reply_elements = item.find_elements(By.CSS_SELECTOR, ".item-comment__box-rep-comment .item-rep-comment")
                    for r_idx, r_item in enumerate(reply_elements, start=1):
                        rep_text = driver.execute_script("return arguments[0].textContent", r_item.find_element(By.CLASS_NAME, "content")).strip()
                        replies_dict[f"reply_{r_idx}"] = {"content": rep_text}

                    all_comment_data.append({
                        "num_comment": current_comment_count,
                        "comment": comment_text,
                        "reply": json.dumps(replies_dict, ensure_ascii=False),
                        "count_reply": len(reply_elements)
                    })
                except:
                    continue

            # --- PHASE 3: Check for "Next Page" button ---
            # Look for the pagination 'next' arrow (usually a specific SVG or class)
            try:
                # CellphoneS pagination often uses a 'pagination' class
                next_page = driver.find_elements(By.CSS_SELECTOR, ".pagination .pagination-next, .btn-next-comment")
                if next_page and next_page[0].is_enabled():
                    print(f"   Moving to next page of comments... Total so far: {len(all_comment_data)}")
                    driver.execute_script("arguments[0].click();", next_page[0])
                    time.sleep(3) # Wait for page transition
                else:
                    print("   No more pages found.")
                    break
            except:
                break

    except Exception as e:
        print(f"   Crawl stopped: {e}")
        
    return all_comment_data

# --- 3. URL RETRIEVAL (Placeholder - use your existing function) ---
def get_all_product_urls(driver, wait, brand):
    # This should be your existing function that clicks 'Show More'
    # Returning a dummy list for structure demonstration
    return ["https://cellphones.com.vn/mobile/apple.html"] 

# --- 4. MAIN LOOP ---
def main():
    driver = setup_driver()
    wait = WebDriverWait(driver, 20)
    brand = "apple"
    
    # Ensure directory exists
    os.makedirs('crawl_data/comment-data/data', exist_ok=True)
    
    fields = ['num_comment', 'comment', 'reply', 'count_reply']
    
    try:
        urls = get_all_product_urls(driver, wait, brand)
        
        for index, url in enumerate(urls):
            sku = url.split("/")[-1].replace(".html", "")
            comment_file = f'crawl_data/comment-data/data/comments_{sku}.csv'
            
            print(f"[{index + 1}/{len(urls)}] Crawling comments for: {url}")
            driver.get(url)
            
            # Extract the comments
            product_comments = crawl_comments(driver, wait)
            
            if product_comments:
                with open(comment_file, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.DictWriter(f, fieldnames=fields)
                    writer.writeheader()
                    writer.writerows(product_comments)
                print(f"   Saved {len(product_comments)} comments to {comment_file}")
            
            time.sleep(2)

    except Exception as e:
        print(f"Main Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()