import requests
import re
import uuid
from bs4 import BeautifulSoup


url = "https://search.yahoo.co.jp/image/search?p=%s&rkf=1&oq=&dim=&ctype=face&imw=0&imh=0&imc=&ei=UTF-8&b=%s"
# url = "https://search.yahoo.co.jp/image/search?p=%s&oq=&ei=UTF-8&b=%s&ktot=8"
keywords = {"ikuta": "生田絵梨花","asuka": "齋藤飛鳥","maiyan" :"白石麻衣","nanase": "西野七瀬","hashimoto": "橋本奈々未"}

pages = []
page = 1
count = 0
 
for x in range(1, 281, 20):
    print(x)
    pages.append(x)
    count += 1

print(pages)

for key in keywords:
        print(key + ': ' + keywords[key] + ' の画像を収集中...')
        for p in pages:
                r = requests.get(url%(keywords[key],p))
                soup = BeautifulSoup(r.text,'lxml')
                imgs = soup.find_all('img',alt='「' + keywords[key] + '」の画像検索結果')
                for img in imgs:
                        r = requests.get(img['src'])
                        with open(str('./' + key + '/')+str(uuid.uuid4())+str('.jpeg'),'wb') as file:
                                file.write(r.content)


print('画像スクレイピング完了！')