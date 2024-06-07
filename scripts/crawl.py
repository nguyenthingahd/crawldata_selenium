import requests
from bs4 import BeautifulSoup

# URL of the webpage to scrape
url = "https://phenikaa-uni.edu.vn/vi/category/tin-tuc/tin-tuc-thong-bao"

# Send a GET request to the webpage
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the section containing the news items
    news_section = soup.find('div', class_='news_list')

    # Check if the news section is found
    if news_section:
        # Find all news items within the section
        news_items = news_section.find_all('div', class_='news_item')
        
        # List to hold the extracted news data
        news_data = []

        # Loop through each news item and extract relevant data
        for item in news_items:
            title = item.find('a').get_text(strip=True)
            link = item.find('a')['href']
            date = item.find('span', class_='news_date').get_text(strip=True)
            
            news_data.append({
                'title': title,
                'link': link,
                'date': date
            })
        
        # Print the extracted news data
        for news in news_data:
            print(f"Title: {news['title']}")
            print(f"Link: {news['link']}")
            print(f"Date: {news['date']}")
            print('-' * 50)
    else:
        print("News section not found on the webpage.")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
