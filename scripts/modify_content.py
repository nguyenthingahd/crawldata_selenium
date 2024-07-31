from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import logging
import time

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

output_dir = 'data'
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, 'modify_content.txt')

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://thuvienphapluat.vn/van-ban/Thue-Phi-Le-Phi/Thong-tu-92-2015-TT-BTC-huong-dan-thue-gia-tri-gia-tang-thue-thu-nhap-ca-nhan-282089.aspx")

# Login process
username_field = driver.find_element(By.ID, 'usernameTextBox') 
password_field = driver.find_element(By.ID, 'passwordTextBox')  
login_button = driver.find_element(By.ID, "loginButton")

username_field.send_keys('thienthuehn')  
password_field.send_keys('0989044955')  
login_button.click()
time.sleep(1)
try:
    agree_button = driver.find_element(By.XPATH, "//span[@class='ui-button-text' and text()='Đồng ý']")
    # Nếu tìm thấy phần tử, nhấp chuột vào nó
    agree_button.click()
    print("Đã nhấp vào nút 'Đồng ý'")
except Exception as e:
    print("Phần tử 'Đồng ý' không xuất hiện hoặc có lỗi:", e)

# Wait for the popup and click on the button if it appears
try:
    popup_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'ui-button-text'))
    )
    popup_button.click()
except Exception as e:
    logging.info("No popup appeared or error occurred: %s", e)

wait = WebDriverWait(driver, 10)

seen_content = set()

# Lấy tất cả các phần tử có sự kiện onclick
elements = driver.find_elements(By.XPATH, "//a[contains(@onclick, 'LS_Tip_Type_Bookmark') and not(contains(@onclick, 'LS_Tip_Type_Bookmark_bm')) and not(contains(@onclick, 'LS_Tip_Type_Bookmark_dc'))]")
elements_list = [element for element in elements]
logging.info(f"Number of elements found: {len(elements_list)}")

with open(output_file, 'w', encoding='utf-8') as file:
    for i, element in enumerate(elements_list):
        try:
            driver.execute_script("arguments[0].click();", element)
            
            # Wait for the popup or content to be visible
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.ctOld.scroll_left'))
            )
            
            ct_old = driver.find_element(By.CSS_SELECTOR, '.ctOld.scroll_left')
            text_ct_old = ct_old.text.strip()

            ct_new = driver.find_element(By.CSS_SELECTOR, '.ct.scroll_right')
            text_ct_new = ct_new.text.strip()

            # Create a unique content string
            content_string = f"{text_ct_old}\n\n{text_ct_new}\n{'-'*50}\n"

            if content_string not in seen_content:
                file.write(content_string)
                # Update the set
                seen_content.add(content_string)
            time.sleep(1)

        except Exception as e:
            logging.error(f"Lỗi khi xử lý phần tử {i + 1}: {e}")

driver.quit()
