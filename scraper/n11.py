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



def n11_scrape(product_name):

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

    driver.get("https://www.n11.com/")
    time.sleep(2)

    


    arama_kutusu = driver.find_element(By.ID, "searchData")
    arama_kutusu.send_keys(product_name)
    arama_kutusu.send_keys(Keys.ENTER)
    time.sleep(2)
    # -----------------------------------------


    

    

    # -----------------------------------------------------------
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    # Tüm ürün linklerini içeren <a> taglarını seçelim
    # Örnek: <a> etiketi içinde "class" varsa veya CSS selector ile seçilebilir
    product_links_0 = soup.find_all("a", class_="plink") 
    product_link=None
    a=0
    for a_tag in product_links_0:
        if(a==1):
            break
        href = a_tag.get("href")
        # Eğer link tam URL değilse site adresini ekle
        if href and not href.startswith("http"):
            href = "https://www.n11.com" + href
        product_link=href
        a=a+1

    driver.get(product_link)
    time.sleep(2)  
        # -----------------------------------------------------------
    

# -----------------------------------------------------------

    try:
        seller_name=driver.find_element(By.CLASS_NAME,"unf-p-seller-name").text.strip()
    except:
        seller_name="N/A" 
    
    try:
        seller_rating=driver.find_element(By.CLASS_NAME,"shopPoint").text.strip()
    except:
        seller_rating="N/A"
    
    try:
        product_rating=driver.find_element(By.CLASS_NAME,"ratingScore").text.strip()
    except:
        product_rating="N/A"
    
    try:
        price=driver.find_element(By.CLASS_NAME,"newPrice").text.strip()
    except:
        price="N/A"

    try:
        product_name_in_site=driver.find_element(By.CLASS_NAME, "proName").text.strip()
    except:
        product_name_in_site="N/A" 

    results.append({
        "product_name":product_name_in_site,
        "seller":seller_name,
        "seller_rating":seller_rating,
        "product_rating":product_rating,
        "price":price
    })

    

    time.sleep(2)
    try:
        # "Tüm satıcıları gör" butonunu kontrol et
        element = driver.find_element(By.XPATH, "//span[contains(text(),'Tümü')]")
        element.click()
        time.sleep(2) 
        

        while True:
            driver.execute_script("window.scrollBy(0, 1000);")
        
            time.sleep(2)  # Sayfanın yüklenmesini bekle

            # Satıcıları çek (örnek class ismine göre)
            seller_box=driver.find_elements(By.CSS_SELECTOR,".unf-cmp .unf-cmp-body")
            for seller in seller_box:
                # Burada seller_name, price gibi bilgileri çekersin
                try:
                    seller_name = seller.find_element(By.CLASS_NAME, "b-n-title").text.strip()
                except:
                    seller_name="N/A"
                
                try:
                    seller_rating=seller.find_element(By.CLASS_NAME,"shopPoint").text.strip()
                except:
                    seller_rating="N/A"
                
                try:
                    price = seller.find_element(By.CLASS_NAME, "b-p-new").text.strip()
                except:
                    price="N/A"
                
                results.append({
                    "product_name":product_name_in_site,
                    "seller":seller_name,
                    "seller_rating":seller_rating,
                    "product_rating":product_rating,
                    "price":price
                })



            # "Sonraki" butonunu bulmaya çalış
            time.sleep(1)
            try:
                print("aaaaaaaaaaaaaaaaaaaaaaaaaaa")
                next_button = driver.find_element(By.CSS_SELECTOR, ".unf-cmp .pagination .next.navigation") # Güncel class ismini kullan
                next_button.click()
                print("bbbbbbbbbbbbbbbbbbbbbbbbb")
                
                
                time.sleep(2)
            except:
                print("ccccccccccccccccccccccccccc")
                break  # Buton yoksa çık


        
    except:
        print("Diğer satıcılar bulunmamakta")
        time.sleep(2) 
        pass

    driver.quit()
    
    return results