from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time, random

driver = webdriver.Chrome()

def cal(list1):
    sum1 = 0
    
    for x in list1 :
        clear_format = x.replace(',' , '')
        sum1 += int(clear_format)
    
    rounded= round(sum1/len(list1) / 10000000)
    
    return (rounded*10000000)

# ... (import statements and the 'cal' function remain the same) ...

def avg_price(car_name):
    
    print(f"🚙  Searching for '{car_name}' prices on bama.ir...")
    driver.get(f"https://bama.ir/car/{car_name}?sort=5")
    
    time.sleep(random.randint(3, 4))
    
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    print("⏳  Loading all ads, please wait", end="")
    while True:
        driver.execute_script("window.scrollTo(0 , document.body.scrollHeight);")
        time.sleep(random.randint(2, 4))
        print(".", end="", flush=True) # Shows the process is active
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            print("\n✅  Page loaded successfully! Processing data...")
            break
        last_height = new_height
        
    html_data = driver.page_source
    driver.quit()
    
    soup = BeautifulSoup(html_data, 'html.parser')
    
    # ... (The part that saves html_data.txt remains the same) ...
    
    all_ads = {}
    ad_blocks = soup.select('.bama-ad-holder')
    
    for ad_block in ad_blocks:
        price_tag = ad_block.select_one('.bama-ad__price')      
        if not price_tag:
            continue
        price_text = price_tag.get_text(strip=True)
        
        year_tag = ad_block.select_one('.bama-ad__detail-row span:nth-child(1)')
        if not year_tag:
           continue
        year_text = year_tag.get_text(strip=True)
        
        if year_text not in all_ads:
            all_ads[year_text] = []
        
        all_ads[year_text].append(price_text)
    
    # --- Final Results Section ---
    
    # Check if any results were actually found
    if not any(all_ads.values()):
        print(f"\n🤷  Sorry, no ads with a specified price were found for '{car_name}'.")
        return

    print(f"\n--- 💰 Average Price Results for '{car_name.title()}' ---")
    
    # Sort the years for a cleaner display
    sorted_years = sorted(all_ads.keys())

    for year in sorted_years:
        prices_list = all_ads[year]
        if not prices_list:
            continue
        
        average = cal(prices_list)
        
        # Clean and formatted final output
        print(f"  📅  Year: {year} | Approx. Price: {average:,.0f}")

    print("." * 45)

# --- Example of how to call the function ---
avg_price("saina-manuals-mtgas")
        
    
   


    


