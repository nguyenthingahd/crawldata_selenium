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
url = "https://www.youtube.com/@programmingwithmosh/videos"

# load the web page
driver.get(url)

# set maximum time to load the web page in seconds
driver.implicitly_wait(10)


# collect data that are withing the id of contents
contents = driver.find_element(By.ID, "contents")

#1 Get all the by video tite link using id video-title-link
video_elements = contents.find_elements(By.ID, "video-title-link")
print(video_elements)
#2 collect title and link for each youtube video
titles = []
links = []

for video in video_elements:

    #3 Extract the video title
    video_title = video.get_attribute("title")
    # print(video_title)
    #4 append the video title
    titles.append(video_title)

    #5 Extract the video link
    video_link = video.get_attribute("href")

#6 append the video link
links.append(video_link)
# print(links)

#1 Get all the by Tag
img_elements = contents.find_elements(By.TAG_NAME, "img")

#2 collect img link and link for each youtube video
img_links = []

for img in img_elements:

    #3 Extract the img link
    img_link = img.get_attribute("src")
    if img_link:
        #4 append the img link
        img_links.append(img_link)

        #1 find the element with the specific ID you want to scrape
meta_data_elements = contents.find_elements(By.ID, 'metadata-line')

#2 collect data from span tag
meta_data = []

for element in meta_data_elements:
    #3 collect span HTML element
    span_tags = element.find_elements(By.TAG_NAME, 'span')

    #4 collect span data
    span_data = []
    for span in span_tags:
        #5 extract data for each span HMTL element.
        span_data.append(span.text)
    #6 append span data to the list
    meta_data.append(span_data)

# print out the scraped data.
# print(meta_data)

#1 Iterate over the list of lists and collect the first and second item of each sublist
views_list = []
published_list = []

for sublist in meta_data:
    #2 append number of views in the views_list
    views_list.append(sublist[0])

    #3 append time published in the published_list
    published_list.append(sublist[1])

# save in pandas dataFrame
data = pd.DataFrame(

list(zip(titles, links, img_links, views_list, published_list)),

columns=['Title', 'Link', 'Img_Link', 'Views', 'Published']
)

# show the top 10 rows
data.head(10)

# export data into a csv file.
data.to_csv("../data/youtube_data.csv",index=False)

driver.quit()

