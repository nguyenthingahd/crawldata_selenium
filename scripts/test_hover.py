from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import requests
from urllib.parse import urlparse
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

output_dir = 'output_links'
os.makedirs(output_dir, exist_ok=True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
url = "https://phenikaa-uni.edu.vn/vi"
driver.get(url)
driver.implicitly_wait(10)

# Extract links
a_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'sub-links')]//ul//li//a[@href]")
links = [a.get_attribute('href') for a in a_elements]

# Function to save page content
def save_page_content(url, text_dir, img_dir):
    try:
        driver.get(url)
        time.sleep(2)
        
        # Extract text content
        try:
            text_content = driver.find_element(By.CLASS_NAME, 'row').text
        except Exception as e:
            logging.error(f"Error extracting text content from {url}: {e}")
            text_content = ''
        
        # Extract and save images
        img_elements = driver.find_elements(By.TAG_NAME, 'img')
        img_links = [img.get_attribute('src') for img in img_elements]
        
        # Extract file name from URL
        filename = os.path.basename(urlparse(url).path)
        text_filename = os.path.join(text_dir, f'{filename}.txt')
        
        with open(text_filename, 'a', encoding='utf-8') as f:
            f.write(f'URL: {url}\n\n')
            f.write(f'File Name: {filename}\n\n')  
            f.write('Text content:\n')
            f.write(text_content + '\n\n')
        
        for img_link in img_links:
            try:
                img_name = os.path.basename(urlparse(img_link).path)
                img_path = os.path.join(img_dir, img_name)
                if not os.path.exists(img_path):  # Check if image already downloaded
                    with open(img_path, 'wb') as img_file:
                        img_file.write(requests.get(img_link).content)
            except Exception as e:
                logging.error(f"Error downloading image {img_link} from {url}: {e}")

        # Extract links from <div class="post_img"> and navigate to them
        post_img_divs = driver.find_elements(By.CLASS_NAME, 'post_img')
        for div in post_img_divs:
            a_tags = div.find_elements(By.TAG_NAME, 'a')
            for a in a_tags:
                href = a.get_attribute('href')
                if href:
                    print(f'Found link in post_img div: {href}')
                    navigate_and_extract(href, img_dir)
                    
    except Exception as e:
        logging.error(f"Error processing {url}: {e}")

# Function to navigate to a link and extract image and text content
def navigate_and_extract(link, img_dir):
    try:
        driver.get(link)
        time.sleep(2)
        
        # Extract and save images in 'news-detail-thumb' class
        news_detail_thumb_divs = driver.find_elements(By.CLASS_NAME, 'news-detail-thumb')
        for div in news_detail_thumb_divs:
            img_elements = div.find_elements(By.TAG_NAME, 'img')
            for img in img_elements:
                img_link = img.get_attribute('src')
                try:
                    img_name = os.path.basename(urlparse(img_link).path)
                    img_path = os.path.join(img_dir, img_name)
                    if not os.path.exists(img_path):
                        with open(img_path, 'wb') as img_file:
                            img_file.write(requests.get(img_link).content)
                except Exception as e:
                    logging.error(f"Error downloading image {img_link} from {link}: {e}")
        
        # Extract and print text content in 'news-item-content-text' class
        news_item_text_divs = driver.find_elements(By.CLASS_NAME, 'news-item-text')
        for div in news_item_text_divs:
            text_content = div.text
            print(f'Text content from {link}:')
            print(text_content)                                                       

    except Exception as e:
        logging.error(f"Error navigating to {link}: {e}")

# Process each main link
for index, link in enumerate(links):
    if link in ["https://vrtour.phenikaa-uni.edu.vn/", "https://tuyensinh.phenikaa-uni.edu.vn/dang-ky", "https://uwebristol.edu.vn/"]:
        logging.info(f'Skipped link: {link}')
        continue

    logging.info(f'Processing link: {link}')
    text_dir = os.path.join(output_dir, 'Text')
    os.makedirs(text_dir, exist_ok=True)
    
    img_dir = os.path.join(output_dir, 'Img')
    os.makedirs(img_dir, exist_ok=True)
    
    save_page_content(link, text_dir, img_dir)
    logging.info(f'Content saved for link: {link}')

# Close WebDriver
driver.quit()
