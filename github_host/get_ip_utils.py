#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Contact :   liuyuqi.gov@msn.cn
@Time    :   2019/08/03 17:02:15
@License :   Copyright © 2017-2022 liuyuqi. All Rights Reserved.
@Desc    :   get ip from ip address
'''

from email import header
import requests
from bs4 import BeautifulSoup
import re
import json
import time


def getIpFromipapi(site):
    '''
    return trueip: None or ip
    '''
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebkit/737.36(KHTML, like Gecke) Chrome/52.0.2743.82 Safari/537.36',
               'Host': 'ip-api.com'}
    url = "http://ip-api.com/json/%s?lang=zh-CN" % (site)
    trueip = set()
    for i in range(3):
        try:
            res = requests.get(url, headers=headers, timeout=5)
            res = json.loads(res.text)
            if res["status"] == "success":
                if not trueip:
                    trueip.add(res["query"])
            time.sleep(2)
        except Exception as e:
            print("查询" + site + " 时出现错误: " + str(e))
    return trueip


def getIpFromChinaz(site):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebkit/737.36(KHTML, like Gecke) Chrome/52.0.2743.82 Safari/537.36',
               'Host': 'ipw.cn'}
    url = "http://ipw.cn/ipv6webcheck/?site=" + site
    trueip = None
    try:
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        result = soup.find_all('span', {"target": "_blank"})
        for c in result:
            ip = re.findall(r"\b(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}\b", c.text)
            if len(ip) != 0:
                trueip = ip[0]
    except Exception as e:
        print("查询" + site + " 时出现错误: " + str(e))
    return trueip


def getIpFromWhatismyipaddress(site):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebkit/737.36(KHTML, like Gecke) Chrome/52.0.2743.82 Safari/537.36',
               'Host': 'ip.tool.chinaz.com'}
    url = "https://whatismyipaddress.com//hostname-ip"
    data = {
        "DOMAINNAME": site,
        "Lookup IP Address": "Lookup IP Address"
    }
    trueip = None
    try:
        res = requests.post(url, headers=headers, data=data, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        result = soup.find_all('span', class_="Whwtdhalf w15-0")
        for c in result:
            ip = re.findall(r"\b(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}\b", c.text)
            if len(ip) != 0:
                trueip = ip[0]
    except Exception as e:
        print("查询" + site + " 时出现错误: " + str(e))
    return trueip


def getIpmain(site):
    '''
    return trueip: None or ip
    '''
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.4844.51 Safari/537.36',
               'Host': 'sites.ipaddress.com'}
    url = "https://sites.ipaddress.com/" + site
    trueip = None
    try:
        print (url)
        res = requests.get(url, headers=headers, timeout=20, allow_redirects=False)
        soup = BeautifulSoup(res.text, 'html.parser')
        result = soup.find_all(id='tabpanel-dns-a')
        for c in result:
            trueip = re.findall(r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}', c.text)
            print(trueip)
        if not trueip:
            trueip = getIpFromipapi(site)
            print("未查询到" + site + " 已切换源,最终返回为" + str(trueip) )
            return trueip
    except Exception as e:
        print("查询" + site + " 时出现错误: " + str(e) )
    print("查询" + site + " 完成: " + str(trueip) )
    return trueip
