import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains



def trendyol_scrape(product_name):

    results = []

    
    global product_name_in_site
    global sellers_data
    sellers_data = []  # önce boşaltabilirsin

    options = webdriver.ChromeOptions()
    
    options.add_argument("--force-device-scale-factor=1") 
    options.add_argument("--disable-notifications") 
    options.add_argument("--incognito")
    options.add_argument("--start-maximized")  # Tarayıcıyı tam ekran başlatır

    options.add_experimental_option("prefs", {


        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_setting_values.geolocation": 2
    })

    # driver path belirtmeden, webdriver_manager ile otomatik kurulum:
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)


    


    driver.get("https://www.trendyol.com")
    time.sleep(2)


    arama_kutusu = driver.find_element(By.CLASS_NAME, "V8wbcUhU")
    arama_kutusu.send_keys(product_name)
    arama_kutusu.send_keys(Keys.ENTER)
    time.sleep(2)
    # -----------------------------------------
    wait = WebDriverWait(driver, 5)

    

    # -----------------------------------------------------------
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    # Tüm ürün linklerini içeren <a> taglarını seçelim
    # Örnek: <a> etiketi içinde "class" varsa veya CSS selector ile seçilebilir
    product_links_0 = soup.find_all("a", class_="p-card-chldrn-cntnr card-border") 
    product_link=None
    a=0
    for a_tag in product_links_0:
        if(a==1):
            break
        href = a_tag.get("href")
        # Eğer link tam URL değilse site adresini ekle
        if href and not href.startswith("http"):
            href = "https://www.trendyol.com" + href
        product_link=href
        a=a+1

    driver.get(product_link)
    time.sleep(2)  
    
    actions = ActionChains(driver)
    actions.move_by_offset(10, 10).click().perform()  # sol üst köşeye yakın boşluk

    time.sleep(0.6)
    
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    c=0

    try:
        
        show_all_button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "show-all"))
    )
        
        show_all_button.click()
        print("Show all button clicked.")
        c=1
        time.sleep(1)
        # --- Ana Satıcının Bilgileri ---
        try:
            product_name_in_site = driver.find_element(By.CLASS_NAME, "pr-new-br").text.strip()
        except:
            product_name_in_site = "N/A"
        try:
            seller_name_main = driver.find_element(By.CLASS_NAME, "seller-name-text").text.strip()
        except:
            seller_name_main = "N/A"

        try:
            seller_rating_main = driver.find_element(By.CLASS_NAME, "sl-pn").text.strip()
        except:
            seller_rating_main = "N/A"

        try:
            price_main = driver.find_element(By.CLASS_NAME, "prc-dsc").text.strip()
        except:
            price_main = "N/A"
        
        try:
            product_rating_main = driver.find_element(By.CLASS_NAME, "value").text.strip()
        except:
            product_rating_main = "N/A"

        
        results.append({
            "product_name":product_name_in_site,
            "seller": seller_name_main,
            "seller_rating": seller_rating_main,
            "product_rating": product_rating_main,
            "price": price_main
        })

        time.sleep(0.5)
        element = driver.find_element(By.CSS_SELECTOR, ".omc-mr-btn.gnr-cnt-br")
        element.click()
        time.sleep(0.5)

        seller_boxes = driver.find_elements(By.CSS_SELECTOR, ".omc-cntr .pr-mc-w.gnr-cnt-br")
        

        for box in seller_boxes:
            try:
                seller_name = box.find_element(By.CLASS_NAME, "seller-name-text").text.strip()
            except:
                seller_name = "N/A"

            try:
                seller_rating = box.find_element(By.CLASS_NAME, "sl-pn").text.strip()
            except:
                seller_rating = "N/A"

            try:
                price = box.find_element(By.CLASS_NAME, "prc-dsc").text.strip()
            except:
                price = "N/A"

            results.append({
                "product_name":product_name_in_site,
                "seller":seller_name,
                "seller_rating":seller_rating,
                "product_rating":product_rating_main,
                "price":price
            })


            
    
    except:
        try:
            product_name_in_site = driver.find_element(By.CLASS_NAME, "pr-new-br").text.strip()
        except:
            product_name_in_site = "N/A"
        
        if(c==0):
            time.sleep(1)
            # --- Ana Satıcının Bilgileri ---
            try:
                seller_name_main = driver.find_element(By.CLASS_NAME, "seller-name-text").text.strip()
            except:
                seller_name_main = "N/A"

            try:
                seller_rating_main = driver.find_element(By.CLASS_NAME, "sl-pn").text.strip()
            except:
                seller_rating_main = "N/A"

            try:
                price_main = driver.find_element(By.CLASS_NAME, "prc-dsc").text.strip()
            except:
                price_main = "N/A"
            
            try:
                product_rating_main = driver.find_element(By.CLASS_NAME, "value").text.strip()
            except:
                product_rating_main = "N/A"

            results.append({
                "product_name":product_name_in_site,
                "seller": seller_name_main,
                "seller_rating": seller_rating_main,
                "product_rating": product_rating_main,
                "price": price_main
            })

            
            print("!!!There is no other seller")
            time.sleep(0.5)
        elif(c==1):
            time.sleep(1)
            #--diğer satıcı bilgileri-------------

            seller_boxes = driver.find_elements(By.CSS_SELECTOR, ".omc-cntr .pr-mc-w.gnr-cnt-br")

            for box in seller_boxes:
                try:
                    seller_name = box.find_element(By.CLASS_NAME, "seller-name-text").text.strip()
                except:
                    seller_name = "N/A"

                try:
                    seller_rating = box.find_element(By.CLASS_NAME, "sl-pn").text.strip()
                except:
                    seller_rating = "N/A"

                try:
                    price = box.find_element(By.CLASS_NAME, "prc-dsc").text.strip()
                except:
                    price = "N/A"

                results.append({
                    "product_name":product_name_in_site,
                    "seller":seller_name,
                    "seller_rating":seller_rating,
                    "product_rating":product_rating_main,
                    "price":price
                })
                
    driver.quit()
    return results
        