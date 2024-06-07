from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Define the URL
url = "https://phenikaa-uni.edu.vn/vi"

# load the web page
driver.get(url)

# set maximum time to load the web page in seconds
driver.implicitly_wait(10)

# collect data that are withing the id of contents
contents = driver.find_element(By.CLASS_NAME, 'row')
# print(contents)

titles = []
# for content in contents:
#     title_elements = content.find_elements(By.TAG_NAME, 'a')
    
#     for title_element in title_elements:
#         titles.append(title_element.text)
# for title in titles:
#     print(title)
title_elements = contents.find_elements(By.TAG_NAME, "a")

# titles = []
links = []

for t in title_elements:
    info_title = t.get_attribute("title")
    # print(info_title)
    titles.append(info_title)
    # print(info_title)

    info_link = t.get_attribute("href")

links.append(info_link)

# print(links)

img_elements = contents.find_elements(By.TAG_NAME, "img")

img_links = []

for img in img_elements:
    img_link = img.get_attribute("src")
    if img_link:
        img_links.append(img_link)

# print(img_links)

post_description_elements = contents.find_elements(By.CLASS_NAME, 'post-description')
post_description = []

for info_element in post_description_elements:
    post_description_elements = post_description_elements

    post_description.append(info_element.text)

# print(post_description)



# # save in pandas dataFrame
data = pd.DataFrame(
    list(zip(titles, links, img_links, post_description)),
    columns=['Title', 'Link', 'Img_Link', 'Post_Description']
)

# print(data.head(10))

# export data into a csv file.
data.to_csv("../data/phenikaa.csv",index=False)

driver.quit()

