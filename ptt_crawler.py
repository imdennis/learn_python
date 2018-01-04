
# coding: utf-8

# In[1]:

import requests
from bs4 import BeautifulSoup


# In[2]:

class PttCrawler:
    
    def __init__(self, board, page, write=False):
        self.ptt_url = 'https://www.ptt.cc'
        self.board = board
        self.page = page
        self.session = requests.Session()
        self.session.cookies.update({
            'over18': '1'
        })
        self.session.headers.update({
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4)"
            "AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30"
        })
        
        self.write = write
        
    def bsHelper(self,bsobj):
        titles = bsobj.findAll("div", {"class": "title"})
        linklist = []
        for title in titles:
            try:
                linklist.append(title.a.attrs["href"])
            except:
                continue
        return linklist
    
    def fetchLink(self):
        url = self.ptt_url + "/bbs"+ self.board +"index.html"
        result_linklist= []
        for i in range(self.page):
            html = self.session.get(url).text
            bsobj = BeautifulSoup(html, "lxml")

            prev = bsobj.findAll("a", {"class":"btn wide"})[1]
            url = self.ptt_url + prev.attrs["href"]
            result_linklist.extend(self.bsHelper(bsobj))
        return result_linklist 
    
    def fetchPost(self,url):
        html = self.session.get(self.ptt_url + url).text
        bsobj = BeautifulSoup(html, "lxml")
        head = bsobj.findAll("span", {"class": "article-meta-value"})
        try:
            author = head[0].text
        except:
            author = None
        try:
            title = head[2].text
        except:
            title = None
        try:
            date = head[3].text
        except:
            date = None
        main_content = bsobj.find("div", {"id": "main-content"})
        try:
            content = main_content.text;
            target_content=u'※ 發信站: 批踢踢實業坊(ptt.cc),'
            content = content.split(target_content)
            content = content[0].split(date)
            main_content = content[1].replace('\n', '').replace('\t', '  ')
        except:
            content = None
        return {"date":date, "author": author, "title": title, "content": main_content}
    
    def run(self):
        result = [self.fetchPost(link) for link in self.fetchLink()]
        return result


# In[4]:

#pttBot = PttCrawler("/Gossiping/", 2)
#pttBot.run();


# In[ ]:



