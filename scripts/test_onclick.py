from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

output_dir = 'data'
os.makedirs(output_dir, exist_ok=True)

try:
    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://thuvienphapluat.vn/van-ban/Thue-Phi-Le-Phi/Thong-tu-111-2013-TT-BTC-Huong-dan-Luat-thue-thu-nhap-ca-nhan-va-Nghi-dinh-65-2013-ND-CP-205356.aspx")
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
        # Iterate through all paragraph elements
        for p in p_elements:
            try:
                # Get the text of the paragraph
                text = p.text
                # logging.info(f'Text: {text}')

                # Save text to file
                file.write(text + '\n')
                # Print text to console
                # print(text)
            except Exception as e:
                logging.error(f'Error processing paragraph: {e}')
except Exception as e:
    logging.error(f'Error initializing WebDriver or processing the page: {e}')
finally:
    # Ensure the driver is closed even if an error occurs
    driver.quit()
