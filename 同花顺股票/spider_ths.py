import json
from bs4 import BeautifulSoup
import asyncio
import httpx
import re
import execjs

class spider:
    # 初始信息 二次请求 html容器  headers cookies
    def __init__(self):
        self.ShangzhengA_html_store = [
            f'https://q.10jqka.com.cn/index/index/board/hs/field/zdf/order/desc/page/{i}/ajax/1/' for i in
            range(1, 112)]
        self.ShenzhengA_html_store = [
            f'https://q.10jqka.com.cn/index/index/board/ss/field/zdf/order/desc/page/{i}/ajax/1/' for i in
            range(1, 144)]
        self.get_cookie = ''
        self.cookies = ''
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # 'Cookie': 'spversion=20130314; searchGuide=sg; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1715907344,1715947317,1716690899; u_ukey=A10702B8689642C6BE607730E11E6E4A; u_uver=1.0.0; u_dpass=Hxvdj8iqlVUvdgMW0Ep6HL4iOUyllLrI59EvTljsUO%2BZvJl6k2Iq2vpl%2B5oGAEMt%2FsBAGfA5tlbuzYBqqcUNFA%3D%3D; u_did=0D6163B457E54ECB920ED8DDB0270F65; u_ttype=WEB; historystock=600121%7C*%7C688629%7C*%7C688695%7C*%7C601020; v=A5teaEh_eXuuoIWPQSu4ntebLPQAcK9yqYRzJo3YdxqxbLXqFUA_wrlUA3ee',
            'Pragma': 'no-cache',
            'Referer': 'https://q.10jqka.com.cn/index/index/board/hs/field/zdf/order/desc/page/7/ajax/1/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }
        self.headers2 = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # 'Cookie': 'spversion=20130314; searchGuide=sg; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1715907344,1715947317,1716690899; u_ukey=A10702B8689642C6BE607730E11E6E4A; u_uver=1.0.0; u_dpass=Hxvdj8iqlVUvdgMW0Ep6HL4iOUyllLrI59EvTljsUO%2BZvJl6k2Iq2vpl%2B5oGAEMt%2FsBAGfA5tlbuzYBqqcUNFA%3D%3D; u_did=0D6163B457E54ECB920ED8DDB0270F65; u_ttype=WEB; historystock=600121%7C*%7C688629%7C*%7C688695%7C*%7C601020; reviewJump=nojump; usersurvey=1; v=A98aJOSrxcCobMHc_w606rM3aDhsRDPmTZg32nEsew7VAPEmeRTDNl1oxy6C',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
        }
        self.path = r'page/(\d+)/ajax'
        self.path_sy=r'<p id="main">({.*})</p>'
        self.res=[]

    def gets_cookie(self):
        with open('./cookie_jm.js', 'r', encoding='utf8') as f:
            content = f.read()
        ctx = execjs.compile(content)
        res = ctx.call('get_cookie')
        return res
    #爬取第一次所有请求页面
    async def get_all_html(self):
        task = []
        for url in self.ShangzhengA_html_store:
            self.get_cookie = self.gets_cookie().split(';')[0][2:]
            self.cookies = {
                'spversion': '20130314',
                'searchGuide': 'sg',
                'Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1': '1715907344,1715947317,1716690899',
                'u_ukey': 'A10702B8689642C6BE607730E11E6E4A',
                'u_uver': '1.0.0',
                'u_dpass': 'Hxvdj8iqlVUvdgMW0Ep6HL4iOUyllLrI59EvTljsUO%2BZvJl6k2Iq2vpl%2B5oGAEMt%2FsBAGfA5tlbuzYBqqcUNFA%3D%3D',
                'u_did': '0D6163B457E54ECB920ED8DDB0270F65',
                'u_ttype': 'WEB',
                'historystock': '600121%7C*%7C688629%7C*%7C688695%7C*%7C601020',
                'v': self.get_cookie,
            }
            t = asyncio.create_task(self.request_two(url, self.headers, self.cookies, 'ShenzhengA',num=1))
            task.append(t)

        for url in self.ShenzhengA_html_store:
            self.get_cookie = self.gets_cookie().split(';')[0][2:]
            self.cookies = {
                'spversion': '20130314',
                'searchGuide': 'sg',
                'Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1': '1715907344,1715947317,1716690899',
                'u_ukey': 'A10702B8689642C6BE607730E11E6E4A',
                'u_uver': '1.0.0',
                'u_dpass': 'Hxvdj8iqlVUvdgMW0Ep6HL4iOUyllLrI59EvTljsUO%2BZvJl6k2Iq2vpl%2B5oGAEMt%2FsBAGfA5tlbuzYBqqcUNFA%3D%3D',
                'u_did': '0D6163B457E54ECB920ED8DDB0270F65',
                'u_ttype': 'WEB',
                'historystock': '600121%7C*%7C688629%7C*%7C688695%7C*%7C601020',
                'v': self.get_cookie,
            }
            t = asyncio.create_task(self.request_two(url, self.headers, self.cookies, 'ShenzhengA',num=1))
            task.append(t)
        await asyncio.wait(task)

    # 请求  num代表第n次请求
    async def request_two(self,url, headers, cookies, type='ShangzhengA',num=2):
        sem = asyncio.Semaphore(4)
        # 爬取请求
        if type == 'ShangzhengA':
            async with sem:
                async with httpx.AsyncClient(headers=headers,cookies=cookies,verify=False,timeout=20) as client:
                    rsp=await client.get(url)
                    if num==2:
                        rsp.encoding='gbk'
                        return rsp.text
                    else:
                        number = re.findall(self.path, url)[0]
                        with open(f'./shenzheng_a/ShenzhengA_{number}.html', 'w', encoding='utf8') as f:
                            f.write(rsp.text)
                            print(f'ShenzhengA{number}ok')

        else:
            async with sem:
                async with httpx.AsyncClient(headers=headers, cookies=cookies, verify=False,timeout=20) as client:
                    rsp = await client.get(url)
                    if num == 2:
                        rsp.encoding = 'gbk'
                        return rsp.text
                    else:
                        number = re.findall(self.path, url)[0]
                        with open(f'./shenzheng_a/ShenzhengA_{number}.html', 'w', encoding='utf8') as f:
                            f.write(rsp.text)
                            print(f'ShenzhengA{number}ok')
                        # time.sleep(0.5)


    #二次请求添加协程任务
    async def process(self, type='ShangzhengA'):
        tasks=[]
        if  type=='ShangzhengA':
            for i in range(1, 112):
                t=asyncio.create_task(self.get_deep_(path=f'shangzheng_a/ShangzhengA_{i}.html'))
                tasks.append(t)

        else:
            for i in range(1,144):
                t = asyncio.create_task(self.get_deep_(path=f'shenzheng_a/ShenzhengA_{i}.html'))
                tasks.append(t)

        result=await asyncio.gather(*tasks)
        return result


    # 二次请求协程单任务处理方式
    async def get_deep_(self,path):
        with open(path,'r',encoding='utf8') as f:
            content = f.read()
            bsp = BeautifulSoup(content, 'html.parser')
            tr = bsp.find('tbody').find_all('tr')
            td = [tr_.find_all('td') for tr_ in tr]
            all = []
            for td_ in td:
                dicts = {}
                dicts['股票代号'] = td_[1].find('a').text
                dicts['股票名称'] = td_[2].find('a').text
                dicts['股票价格'] = td_[3].text
                dicts['涨幅跌'] = td_[4].text
                dicts['换手'] = td_[7].text
                dicts['量比'] = td_[8].text
                dicts['流通市值'] = td_[10].text
                dicts['市盈率'] = td_[11].text
                dicts['分红href'] = f"https://basic.10jqka.com.cn/{td_[1].find('a').text}/bonus.html"
                dicts['收益href'] = f"https://basic.10jqka.com.cn/{td_[1].find('a').text}/finance.html"
                if dicts['股票价格'] != '--' and eval(dicts['股票价格']) <= 15 and eval(dicts['流通市值'][:-1]) <= 20:
                    all.append(dicts)
                    # print(all)
                else:
                    continue
            if len(all) != 0:
                for j in all:
                    self.get_cookie = self.gets_cookie().split(';')[0][2:]
                    self.cookies = {
                        'spversion': '20130314',
                        'searchGuide': 'sg',
                        'Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1': '1715907344,1715947317,1716690899',
                        'u_ukey': 'A10702B8689642C6BE607730E11E6E4A',
                        'u_uver': '1.0.0',
                        'u_dpass': 'Hxvdj8iqlVUvdgMW0Ep6HL4iOUyllLrI59EvTljsUO%2BZvJl6k2Iq2vpl%2B5oGAEMt%2FsBAGfA5tlbuzYBqqcUNFA%3D%3D',
                        'u_did': '0D6163B457E54ECB920ED8DDB0270F65',
                        'u_ttype': 'WEB',
                        'historystock': '600121%7C*%7C688629%7C*%7C688695%7C*%7C601020',
                        'v': self.get_cookie,
                    }

                    rsp = await self.request_two(j['分红href'], headers=self.headers2, cookies=self.cookies)
                    soup = BeautifulSoup(rsp, 'html.parser')
                    text = soup.find('tbody').find_all('tr')[0].find_all('td')[4].text
                    j['分红'] = text
                    self.get_cookie = self.gets_cookie().split(';')[0][2:]
                    self.cookies = {
                        'spversion': '20130314',
                        'searchGuide': 'sg',
                        'Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1': '1715907344,1715947317,1716690899',
                        'u_ukey': 'A10702B8689642C6BE607730E11E6E4A',
                        'u_uver': '1.0.0',
                        'u_dpass': 'Hxvdj8iqlVUvdgMW0Ep6HL4iOUyllLrI59EvTljsUO%2BZvJl6k2Iq2vpl%2B5oGAEMt%2FsBAGfA5tlbuzYBqqcUNFA%3D%3D',
                        'u_did': '0D6163B457E54ECB920ED8DDB0270F65',
                        'u_ttype': 'WEB',
                        'historystock': '600121%7C*%7C688629%7C*%7C688695%7C*%7C601020',
                        'v': self.get_cookie,
                    }
                    rsp2 = await self.request_two(j['收益href'], headers=self.headers2, cookies=self.cookies)
                    # soup2 = BeautifulSoup(rsp2, 'html.parser')
                    try:
                        mes=re.findall(self.path_sy,rsp2)[0]
                        with open('./aaa.js','r',encoding='utf8') as f:
                            content=f.read()
                        compile=execjs.compile(content)
                        text2=compile.call('get_sy',mes)
                        # text2 = soup2.find_all('th', class_='tl', string='基本每股收益(元)')[0].find_next_sibling().text
                    except:
                        text2 = '无'
                    j['收益'] = text2
                    if j['收益'] == '无' or j['分红'] == '不分配不转增' or eval(j['收益']) <= 0:
                        j['问题']=1
                        # all.remove(j)
                    else:
                        print('----')
                        print(all)
                        continue
        return all


    # 保存为json格式
    async def save_json(self,type='ShangzhengA'):
        if type == 'ShangzhengA':
            res = await self.process()
        else:
            res = await self.process(type='ShenzhengA')
        all=[]
        for i in res:
            all+=i
        for i in all:
            del i['收益href']
            del i['分红href']
            if i.get('问题')==1:
                continue
            else:
                self.res.append(i)
        with open(type+'.json','w',encoding='utf8') as f:
            f.write(json.dumps(self.res,ensure_ascii=False))
    # 信息保存


if __name__ == '__main__':
    a = spider()
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(a.get_all_html())
    # loop = asyncio.get_event_loop()
    loop.run_until_complete(a.save_json(type='ShenzhengA'))
    # loop.run_until_complete(a.save_json())
    # print(a.res)

