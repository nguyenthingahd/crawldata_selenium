import requests
from bs4 import BeautifulSoup
listlink = []
def crawl(baseUrl, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    titles = soup.findAll('div', class_='post-title')
    print(titles)
    links = [link.find('a').attrs["href"] for link in titles]
    for link in links:
        if link not in listlink:
            listlink.append(link)
            try:
                # print(link)
                news = requests.get(baseUrl + link)
                print(news)
                soup = BeautifulSoup(news.content, "html.parser")
                body = soup.find("div", class_="singular-content")
                text = ""
                content = body.findChildren("p", recursive=False)
                text_file = open("data.txt", "a")
                for i in range(0, len(content)):
                    str = content[i].text
                    # for j in range(1, len(str)):
                    #     if str[j] == '.' and str[j-1].isnumeric() and str[j+1].isnumeric():
                    #         print(str[j])
                    #         str[j] = ""
                    sentences = str.split(".")
                    for text in sentences:
                        if len(text) > 1 and len(text) < 190:
                            text = text.replace("- ", "")
                            text = text.replace("\"", "")
                            text = text.strip()
                            text = text + ".\n"
                            text_file.write(text)
                    # text += str
                # text = text.replace("\n", " ")
                # text_file = open("dantri.txt", "a")
                # text_file.write(text)
                text_file.close()
            except:
                pass
if __name__ == "__main__":
    # f = open("url.txt")
    # str = f.read()
    # lst = str.split("\n")
    url = "https://phenikaa-uni.edu.vn/vi/category/gioi-thieu/bao-chi-noi-ve-chung-toi"
    baseUrl = "https://phenikaa-uni.edu.vn/vi"
    
    crawl(baseUrl, url)
    # for i in range(2, 10):
    #     urll = f"{baseUrl}/-page{i}"  # Use f-string to format the URL
    #     crawl(baseUrl, urll)
