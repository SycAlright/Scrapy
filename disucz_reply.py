import time
import requests
from bs4 import BeautifulSoup
import xlwt

# Url
URL= 'https://hostloc.com'

# Cookie
COOKIE = {
    "Session": "Your_Cookie"
}

# Uid
UID = 45820

# Scrapy
START = 1
END = 50

# --Core--

Reply = []


def get_html(page):
    url = URL + '/home.php?mod=space&uid=' + str(UID) + '&do=thread&view=me&type=reply&order=dateline&page=' + \
        str(page)
    r = requests.get(url, cookies=COOKIE)
    r.encoding = 'utf-8'
    html = r.text
    return html


def parse_html(html):
    bs = BeautifulSoup(html, "lxml")
    res = bs.select('td.xg1>a')
    for item in res:
        text = item.get_text()
        url = item.get("href")
        print([text, url])
        Reply.append([text, url])


def xls_save(name):
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet(str(UID), cell_overwrite_ok=True)
    sheet.write(0, 0, '回复')
    sheet.write(0, 1, '链接')
    i = 1
    for data in Reply:
        sheet.write(i, 0, data[0])
        sheet.write(i, 1, data[1])
        i = i + 1
    book.save('data['+name+'].xls')


def main():
    print("采集UID："+str(UID))
    for i in range(START, END):
        print("==当前："+str(i)+"页==")
        html = get_html(i)
        parse_html(html)
        if(i % 2 == 0):
            print("$$ Sleep $$")
            time.sleep(3)
    print("# Save Data")
    xls_save(str(START)+'-'+str(END))


if __name__ == "__main__":
    main()
