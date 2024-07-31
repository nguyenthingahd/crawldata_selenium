from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Khởi tạo ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Mở trang web
driver.get('https://thuvienphapluat.vn/van-ban/Thue-Phi-Le-Phi/Thong-tu-92-2015-TT-BTC-huong-dan-thue-gia-tri-gia-tang-thue-thu-nhap-ca-nhan-282089.aspx?anchor=khoan_1_11')  # Thay đổi URL thành trang đăng nhập của bạn
username_field = driver.find_element(By.ID, 'usernameTextBox') 
password_field = driver.find_element(By.ID, 'passwordTextBox')  
username_field.send_keys('thienthuehn')  
password_field.send_keys('0989044955')  

# Gửi biểu mẫu
password_field.send_keys(Keys.RETURN)



# Đóng trình duyệt
driver.quit()
