from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

output_dir = 'data'
os.makedirs(output_dir, exist_ok=True)

try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://thuvienphapluat.vn/van-ban/Thue-Phi-Le-Phi/Thong-tu-92-2015-TT-BTC-huong-dan-thue-gia-tri-gia-tang-thue-thu-nhap-ca-nhan-282089.aspx?anchor=khoan_1_11')  # Thay đổi URL thành trang đăng nhập của bạn
    wait = WebDriverWait(driver, 10)
    # Locate the div with id 'tab1' and class 'contentDoc'
    div_element = wait.until(EC.presence_of_element_located((By.ID, 'tab1')))

    # Find all paragraph elements within the div
    p_elements = div_element.find_elements(By.TAG_NAME, 'p')

    # Initialize ActionChains
    actions = ActionChains(driver)

    # Prepare file for saving data
    output_file_path = os.path.join(output_dir, 'extracted_data.txt')
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for p in p_elements:
            try:
                text = p.text
                file.write(text + '\n')
            except Exception as e:
                logging.error(f'Error processing paragraph: {e}')
except Exception as e:
    logging.error(f'Error initializing WebDriver or processing the page: {e}')
finally:
    driver.quit()
