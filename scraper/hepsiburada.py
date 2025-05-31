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




def hepsiburada_scrape(product_name):

    results = []

    

    global sellers_data
    global product_name_in_site
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

    driver.get(f"https://www.hepsiburada.com/ara?q={product_name}")
    time.sleep(2)

  
    

    # -----------------------------------------------------------
    
    
    
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    # Tüm ürün linklerini içeren <a> taglarını seçelim
    # Örnek: <a> etiketi içinde "class" varsa veya CSS selector ile seçilebilir
    product_links_0 = soup.find_all("a", class_="productCardLink-module_productCardLink__GZ3eU") 
    product_link=None
    a=0
    for a_tag in product_links_0:
        if(a==1):
            break
        href = a_tag.get("href")
        # Eğer link tam URL değilse site adresini ekle
        if href and not href.startswith("http"):
            href = "https://www.hepsiburada.com" + href
        product_link=href
        a=a+1

    driver.get(product_link)
    time.sleep(2)  

    #-------Getting seller informations-----------------

    try:
        product_rating=driver.find_element(By.CLASS_NAME,"JYHIcZ8Z_Gz7VXzxFB96").text.strip()
    except:
        product_rating="N/A" 

    try:
        product_name_in_site=driver.find_element(By.CSS_SELECTOR, '[data-test-id="title"]').text.strip()
    except:
        product_name_in_site="N/A" 
    
    time.sleep(2) 
    try:
        
        # "Tüm satıcıları gör" butonunu kontrol et
        element = driver.find_element(By.CLASS_NAME, "M6iJLUpgHKlEPzGcOggE")
        element.click()
        time.sleep(2) 
        "ciEqaMdv5xbgmqxYG3vq"
        seller_boxes = driver.find_elements(By.CLASS_NAME, "VwUAvtsSpdiwukfc0VGp")
        print(len(seller_boxes))
        
        for box in seller_boxes:
            
            try:
                seller_name = box.find_element(By.CSS_SELECTOR, '[data-test-id="merchant-name"]').text
                
            except:
                seller_name = "N/A"
            if(seller_name=="Hepsiburada"):
                seller_rating="10"
            else:
                try:
                    seller_rating = box.find_element(By.CSS_SELECTOR,'[data-test-id="merchant-rating"]').text.strip()
                except:
                    seller_rating = "N/A"

            try:
                price = box.find_element(By.CSS_SELECTOR, '[data-test-id="price-current-price"]').text.strip()
            except:
                price = "N/A"

            results.append({
                "product_name":product_name_in_site,
                "seller":seller_name,
                "seller_rating":seller_rating,
                "product_rating":product_rating,
                "price":price
            })
            
            



    except :
        print("a")
        time.sleep(1) 
        print("Buton bulunamadı, tek satıcı olabilir.")

        try:
            seller_name=driver.find_element(By.CLASS_NAME,"rzVCX6O5Vz9bkKB61N2W").text.strip()
        except:
            seller_name="N/A"
        
        if(seller_name=="Hepsiburada"):
            seller_rating="10"
        else:
            try:
                seller_rating=driver.find_element(By.CSS_SELECTOR, '[data-test-id="merchant-rating"]').text.strip()
            except:
                seller_rating="N/A"

        try:
            price=driver.find_element(By.CLASS_NAME,"z7kokklsVwh0K5zFWjIO").text.strip()
        except:
            price="N/A"
    
       
        results.append({
            "product_name":product_name_in_site,
            "seller":seller_name,
            "seller_rating":seller_rating,
            "product_rating":product_rating,
            "price":price
        })
    driver.quit()
    return results
