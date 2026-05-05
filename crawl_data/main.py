import csv
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth

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


def get_color_variants(driver):
    """Extracts all color variants using textContent for better reliability."""
    variants_dict = {}
    try:
        # 1. Wait for the container to exist
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "list-variants"))
        )
        
        # 2. Locate all variant items
        variant_items = driver.find_elements(By.CSS_SELECTOR, ".box-product-variants li.item-variant")
        
        for index, item in enumerate(variant_items, start=1):
            try:
                # 3. Use get_attribute("textContent") instead of .text
                # This bypasses Selenium's visibility check which often fails in swipers/boxes
                color_name_el = item.find_element(By.CSS_SELECTOR, ".item-variant-name")
                color_name = driver.execute_script("return arguments[0].textContent", color_name_el).strip()
                
                price_el = item.find_element(By.CSS_SELECTOR, ".item-variant-price")
                price = driver.execute_script("return arguments[0].textContent", price_el).strip()
                
                # 4. Get the URL
                link_element = item.find_element(By.TAG_NAME, "a")
                image_url = link_element.get_attribute("href")
                
                key = f"product_color_{index}"
                variants_dict[key] = {
                    "color": color_name,
                    "image_url": image_url,
                    "price": price
                }
            except Exception as e:
                continue
                
    except Exception as e:
        print(f"Color Variants Error: {e}")
    
    return json.dumps(variants_dict, ensure_ascii=False)

def get_description(driver, wait):
    """Handles Case 1 (Tabs) and Case 2 (Direct Content) for descriptions."""
    try:
        # Scroll down a bit to trigger any lazy-loading scripts
        driver.execute_script("window.scrollTo(0, 800);")
        time.sleep(1.5)

        # --- STEP 1: Check for Case 1 (The Tab) ---
        tab_xpath = "//div[contains(@class, 'tabs')]//span[contains(text(), 'Mô tả sản phẩm')]"
        tabs = driver.find_elements(By.XPATH, tab_xpath)
        
        if tabs and tabs[0].is_displayed():
            print("Case 1 detected: Clicking 'Mô tả sản phẩm' tab.")
            driver.execute_script("arguments[0].click();", tabs[0])
            time.sleep(1) # Wait for tab content to swap
        else:
            print("Case 2 detected: No tab found, attempting direct crawl.")

        # --- STEP 2: Handle 'Xem thêm' (Expand Content) ---
        # This button exists in both cases to reveal the full text
        try:
            show_more_selector = ".btn-show-more, .button__content-show-more"
            show_more = driver.find_elements(By.CSS_SELECTOR, show_more_selector)
            if show_more and show_more[0].is_displayed():
                driver.execute_script("arguments[0].click();", show_more[0])
                time.sleep(1)
        except:
            pass

        # --- STEP 3: Extract the Text ---
        # We target the most specific content IDs first, then the general left block
        try:
            # Try to get the specific content div from your HTML snippet
            content_element = driver.find_element(By.CSS_SELECTOR, "#cpsContent, .cps-block-content")
        except:
            # Fallback to the larger left container
            content_element = driver.find_element(By.CLASS_NAME, "block-content-product-left")
            
        return content_element.text.strip()

    except Exception as e:
        print(f"Description Error: {e}")
        return "N/A"

def get_all_specifications(driver, wait):
    """Opens teleport-modal_content and scrapes all technical-content-sections."""
    all_specs = {}
    try:
        # 1. Click the button to open the technical specs modal
        tech_btn_selector = "button.button__show-modal-technical"
        tech_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, tech_btn_selector)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tech_btn)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", tech_btn)
        
        # 2. Wait for the teleport modal content to appear
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "teleport-modal_content")))
        time.sleep(2) 

        # 3. Locate all specification sections
        sections = driver.find_elements(By.CSS_SELECTOR, ".technical-content-section")
        
        for section in sections:
            # Get the category name (e.g., 'Màn hình', 'Camera sau')
            try:
                category_name = section.find_element(By.CSS_SELECTOR, "p.title").text.strip()
            except:
                continue
            
            # Get all rows in the table for this category
            rows = section.find_elements(By.CSS_SELECTOR, "tr.technical-content-item")
            category_data = []
            
            for row in rows:
                try:
                    # The first <td> is the spec name, the second <td> is the value
                    cols = row.find_elements(By.TAG_NAME, "td")
                    if len(cols) >= 2:
                        spec_name = cols[0].text.strip()
                        spec_value = cols[1].text.strip()
                        category_data.append({"name": spec_name, "value": spec_value})
                except:
                    continue
            
            all_specs[category_name] = category_data

        # 4. Close the modal
        close_btn = driver.find_elements(By.CSS_SELECTOR, ".modal-close, .btn-close, .is-close")
        if close_btn:
            driver.execute_script("arguments[0].click();", close_btn[0])
            
    except Exception as e:
        print(f"Specs Modal Error: {e}")
    
    return json.dumps(all_specs, ensure_ascii=False)

def get_product_images(driver):
    """Extracts up to 3 image links, excluding videos."""
    images = []
    try:
        # Find all slides in the product gallery
        slides = driver.find_elements(By.CSS_SELECTOR, ".swiper-slide a.spotlight")
        
        for slide in slides:
            img_url = slide.get_attribute("href")
            
            # Filter: Check if it's a valid product image link and not a video/thumbnail
            if img_url and "media/catalog/product" in img_url:
                if img_url not in images:
                    images.append(img_url)
            
            # Stop once we have 3 images
            if len(images) >= 3:
                break
    except Exception as e:
        print(f"Image extraction error: {e}")
    
    return json.dumps(images, ensure_ascii=False)

# --- 4. ITEM PROCESSING ---
def crawl_item_details(driver, wait, url):
    driver.execute_script("window.open(arguments[0], '_blank');", url)
    driver.switch_to.window(driver.window_handles[1])
    item_data = {}
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        
        # Basic Info
        item_data['name'] = driver.find_element(By.TAG_NAME, "h1").text.strip()
        item_data['sku'] = url.split("/")[-1].replace(".html", "")
        
        # Prices
        try:
            item_data['sale_price'] = driver.find_element(By.CLASS_NAME, "sale-price").text.strip()
            item_data['base_price'] = driver.find_element(By.CLASS_NAME, "base-price").text.strip()
        except:
            item_data['sale_price'] = item_data['base_price'] = "N/A"

        # Content Scraping (using the updated Case 1/Case 2 logic)
        item_data['description'] = get_description(driver, wait)
        item_data['specifications'] = get_all_specifications(driver, wait)
        
        # Images (Top gallery)
        item_data['images'] = get_product_images(driver)
        
        # New: Color Variants
        item_data['colors'] = get_color_variants(driver)

    except Exception as e:
        print(f"Failed to crawl {url}: {e}")
    
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return item_data

def get_all_product_urls(driver, wait, brand):
    """Clicks 'Xem thêm' until all products are loaded, then returns all URLs."""
    print("Loading all products...")
    driver.get(f"https://cellphones.com.vn/laptop/{brand}.html")
    time.sleep(5) # Initial load

    while True:
        try:
            # Look for the 'Xem thêm' button
            # We use a broad selector to catch different versions of the button
            load_more_btn = driver.find_elements(By.CSS_SELECTOR, ".button__show-more-product, .btn-show-more")
            
            if load_more_btn and load_more_btn[0].is_displayed():
                # Scroll to the button to ensure it's clickable
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", load_more_btn[0])
                time.sleep(1)
                
                # Click using JS to avoid 'ElementClickIntercepted' errors
                driver.execute_script("arguments[0].click();", load_more_btn[0])
                print("Clicked 'Xem thêm', loading more...")
                
                # Wait for new items to render
                time.sleep(3) 
            else:
                print("No more 'Xem thêm' button found. All products loaded.")
                break
        except Exception as e:
            print(f"Finished loading or encountered error: {e}")
            break

    # Once the loop breaks, get all links
    product_links = driver.find_elements(By.CSS_SELECTOR, ".product-info > a")
    urls = [link.get_attribute("href") for link in product_links if link.get_attribute("href")]
    
    # Remove duplicates while preserving order
    return list(dict.fromkeys(urls))

# --- 5. MAIN LOOP ---
def main():
    driver = setup_driver()
    wait = WebDriverWait(driver, 20)
    brand = "msi"
    filename = f'crawl_data/data/laptop/cellphones_{brand}.csv'
    
    # ADD 'images' to the fields list
    fields = ['name', 'sku', 'base_price', 'sale_price', 'description', 'specifications', 'images', 'colors']
    
    try:
        all_urls = get_all_product_urls(driver, wait, brand)
        print(f"Total products found: {len(all_urls)}")

        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            
            for index, url in enumerate(all_urls):
                print(f"[{index + 1}/{len(all_urls)}] Processing: {url}")
                result = crawl_item_details(driver, wait, url)
                
                if result:
                    writer.writerow(result)
                    f.flush()
                    print(f"   Success: {result['name']} with {len(json.loads(result['images']))} images")
                
                time.sleep(2)

    except Exception as e:
        print(f"Main Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()