import requests
from bs4 import BeautifulSoup
import time

base_url = "https://www.ptt.cc"
current_url = "/bbs/Stock/index.html"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

with open("stock.txt", "w", encoding="utf-8") as f:
    pages = 5

    for i in range(pages):
        f.write(f"第 {i+1} 頁：\n")
        url = base_url + current_url
        try:
            req = requests.get(url, headers=headers, timeout=10)
            req.raise_for_status()
        except:
            print(f"第 {i+1} 頁連線失敗: {req}")
            break

        req.encoding = "utf-8"
        sp = BeautifulSoup(req.text, "html.parser")
        articles = sp.find_all("div", class_="r-ent")

        for data in articles:
            try:
                title_block = data.find("div", class_="title")
                title_tag = title_block.find("a")
                link = base_url + title_tag.get("href")
                title = title_tag.text.strip()
                meta_tag = data.find("div", class_="meta")
                author = meta_tag.find("div", class_="author").text
                date = meta_tag.find("div", class_="date").text.strip()
                f.write(f"{title}, {author}, {date}, {link}\n")
            except:
                title = "DELETE"
                print(title)

        btn_group = sp.find("div", class_="btn-group btn-group-paging")
        if btn_group:
            prev_page = btn_group.find_all("a")[1]
            if prev_page:
                current_url = prev_page.get("href")
            else:
                break
        else:
            break

        time.sleep(1.5)
    
    print("DONE")