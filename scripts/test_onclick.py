from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
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

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://thuvienphapluat.vn/van-ban/Thue-Phi-Le-Phi/Thong-tu-111-2013-TT-BTC-Huong-dan-Luat-thue-thu-nhap-ca-nhan-va-Nghi-dinh-65-2013-ND-CP-205356.aspx")

# Login process
try:
    username_field = driver.find_element(By.ID, 'usernameTextBox') 
    password_field = driver.find_element(By.ID, 'passwordTextBox')  
    login_button = driver.find_element(By.ID, "loginButton")

    username_field.send_keys('thienthuehn')  
    password_field.send_keys('0989044955')  
    login_button.click()
    time.sleep(1)
    
    try:
        agree_button = driver.find_element(By.XPATH, "//span[@class='ui-button-text' and text()='Đồng ý']")
        agree_button.click()
    except Exception as e:
        print("Phần tử 'Đồng ý' không xuất hiện hoặc có lỗi:", e)

    # Navigate to the content page
    driver.get('https://thuvienphapluat.vn/van-ban/Thue-Phi-Le-Phi/Thong-tu-111-2013-TT-BTC-Huong-dan-Luat-thue-thu-nhap-ca-nhan-va-Nghi-dinh-65-2013-ND-CP-205356.aspx')  
    wait = WebDriverWait(driver, 10)
    div_element = wait.until(EC.presence_of_element_located((By.ID, 'tab1')))

    # Find all paragraph elements within the div
    p_elements = div_element.find_elements(By.TAG_NAME, 'p')

    # Initialize ActionChains
    actions = ActionChains(driver)

    # Prepare file for saving data
    output_file_path = os.path.join(output_dir, 'extracted_data.txt')
    with open(output_file_path, 'w', encoding='utf-8') as file:
        seen_content = set()
        for p in p_elements:
            text = p.text.strip()

            # Check for links
            links = p.find_elements(By.XPATH, ".//a[contains(@onclick, 'LS_Tip_Type_Bookmark') and not(contains(@onclick, 'LS_Tip_Type_Bookmark_bm')) and not(contains(@onclick, 'LS_Tip_Type_Bookmark_dc'))]")

            if links:
                # If links are found, process them
                for link in links:
                    driver.execute_script("arguments[0].click();", link)
                    
                    # Wait for the popup or content to be visible
                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, '.ctOld.scroll_left'))
                    )
                    ct_old = driver.find_element(By.CSS_SELECTOR, '.ctOld.scroll_left')
                    text_ct_old = ct_old.text.strip()

                    ct_new = driver.find_element(By.CSS_SELECTOR, '.ct.scroll_right')
                    text_ct_new = ct_new.text.strip()

                    # Create a unique content string
                    content_string = f"{text_ct_old}\n\n{text_ct_new}\n{'*'*50}\n"

                    if content_string not in seen_content:
                        file.write(content_string)
                        seen_content.add(content_string)
                    time.sleep(5)
                    close_button = driver.find_element(By.XPATH, "//span[@class='ui-icon ui-icon-closethick' and text()='close']")
                    close_button.click()
            else:
                file.write(text + '\n')

except Exception as e:
    logging.error(f'Error initializing WebDriver or processing the page: {e}')
finally:
    driver.quit()
