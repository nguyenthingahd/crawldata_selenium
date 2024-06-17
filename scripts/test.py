from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://phenikaa-uni.edu.vn/vi/events/category/su-kien')
pagination_container = driver.find_element(By.CLASS_NAME, 'pagination')
print(pagination_container)
# active_links = pagination_container.find_elements(By.CSS_SELECTOR, '.active')
# for link in active_links:
#     link.click()
driver.quit()