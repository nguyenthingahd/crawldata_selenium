from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

output_dir = 'data'
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, 'modify_content.txt')

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://thuvienphapluat.vn/van-ban/Thue-Phi-Le-Phi/Thong-tu-111-2013-TT-BTC-Huong-dan-Luat-thue-thu-nhap-ca-nhan-va-Nghi-dinh-65-2013-ND-CP-205356.aspx")
wait = WebDriverWait(driver, 10)

# Lấy tất cả các phần tử có sự kiện onclick
elements = driver.find_elements(By.XPATH, "//a[contains(@onclick, 'LS_Tip_Type_Bookmark')]")
elements_list = [element for element in elements]

logging.info(f"Number of elements found: {len(elements_list)}")

with open(output_file, 'w', encoding='utf-8') as file:
    for i, element in enumerate(elements_list):
        try:
            # Click on the element to open the popup or content
            driver.execute_script("arguments[0].click();", element)
            
            # Wait for the popup or content to be visible
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.ctOld.scroll_left'))
            )

            # Lấy nội dung từ phần tử có class="ctOld scroll_left"
            ct_old = driver.find_element(By.CSS_SELECTOR, '.ctOld.scroll_left')
            text_ct_old = ct_old.text

            # Lấy nội dung từ phần tử có class="ct scroll_right"
            ct_new = driver.find_element(By.CSS_SELECTOR, '.ct.scroll_right')
            text_ct_new = ct_new.text

            # Ghi kết quả vào file
            # file.write(f"Phần tử {i + 1} - Nội dung gốc:\n")
            file.write(text_ct_old + "\n\n")
            # file.write("Nội dung sửa đổi, hướng dẫn:\n")
            file.write(text_ct_new + "\n")
            file.write("\n" + "-"*50 + "\n")

        except Exception as e:
            logging.error(f"Lỗi khi xử lý phần tử {i + 1}: {e}")

# Clean up
driver.quit()
