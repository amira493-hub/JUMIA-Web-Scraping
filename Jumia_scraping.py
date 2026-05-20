from selenium import webdriver
# service to say the type of browser, here it's chrom for example
from selenium.webdriver.chrome.service import Service
# inside of chrome there are some options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

def scrape_jumia_live(target_count):
    print(f"Starting live scraping of {target_count} phones of prices from 10k to 20k...\n")

    #Setup Chrome options because my browser name is chrome بيسطب الاوبشتز بتاعة كروم
    chrome_options = Options()
    # To get the website full screen, (add arguments is one of chrome options)
    chrome_options.add_argument("--start-maximized")
    
    #Initialize the webdriver or  chrome driver here
    driver = webdriver.Chrome(
                              service = Service(ChromeDriverManager().install()),
                              options = chrome_options
                              )

    scrapped_data = []
    page_number = 1

    # to avoid the errors
    try:
        while len(scrapped_data) < target_count:
            print(f"Navigating to page number {page_number}")

            # 1. the command to navigate or go to Jumia's website with the price filter
            url = f"https://www.jumia.com.eg/smartphones?price=10000-20000&page={page_number}"
            driver.get(url)
            # 2. pause using sleep; to go slowly into the site for me to be able to see the navigation
            print('Page Loaded. wating for 5 seconds')
            time.sleep(5)

            # 3. simulate human scrolling to load all dynamic images/elements
            print("scrolling now")
            # the scroll loop will work as 25%, 75%, 100%
            for scroll in range(1,4):
                driver.execute_script(f'window.scrollTo(0, document.body.scrollHeight/{scroll});')
                time.sleep(1.5)
            
            # making the code understands how the data is stored
            # 4. Find elements using class_Name, XPATH, or CSS selectors which are of the different wasy each website is storing it's data 
            product_elements = driver.find_elements(By.XPATH, '//*[@id="jm"]/main/div[2]/div[3]/section/div[2]//article')
            print(f'Found {len(product_elements)} products on the page.\n')

            if len(product_elements) == 0:
                print("No more products found. Exiting the loop.")

            # 5. Extract data
            for item in product_elements:
                if len(scrapped_data) >= target_count:
                    break

                try:
                    #extract the name, price, product_url  
                    name = item.find_element(By.CLASS_NAME, "name").text.strip()
                    price = item.find_element(By.CLASS_NAME, "prc").text.strip()
                    product_link = item.find_element(By.CLASS_NAME, "core").get_attribute('href').strip()

                    # Data Cleaning Step
                    price = float(price.replace(",","").replace('EGP', "").strip())
                    # data validation step
                    if 10000 < price < 20000:
                        scrapped_data.append({
                            'Name': name,
                            'Price': price,
                            'Product Link': product_link
                        })
                        print(f"{len(scrapped_data)} / {target_count} valid: {name[:30]}... | EGP {price}") # this means to the 30 character or letters of the name
                    else:
                        print(f"skipped out of range Ad: EGP {price}")
                except Exception as e:
                    print(f"The issue is {e}")
            
            page_number +=1
            
        
    finally:
        print("")
    #     # Keep browser open for 5 seconds before closing to make sure it worked
    #     time.sleep(5)
    #     print("\nScraping complete. Closing browser in 5 seconds...")
    #     driver.quit()


    df = pd.DataFrame(scrapped_data)

    file_name = "jumia phones_10k_20k.csv"
    #index is about the ordering of the rows
    # the encoding is to be able to read also letter not only numbers
    df.to_csv(file_name, index = False, encoding = "utf-8-sig")
    print(f"\nSUCCESS! Cleaned data saved to {file_name}")
    return df



print(f"\nFinal Dataset Preview: {scrape_jumia_live(100).head()}")
