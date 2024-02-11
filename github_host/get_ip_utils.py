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
import os
import re
import json
import time
import socket
import threading
from urllib.parse import urlparse, urljoin
from urllib.robotparser import RobotFileParser
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# 创建一个 Session 对象
session = requests.Session()

# 创建一个 Retry 对象
retry_strategy = Retry(
    total=3,  
    backoff_factor=1, 
    status_forcelist=[429, 500, 502, 503, 504],  
    allowed_methods=["GET", "POST"] # 不清楚POST使用session好不好，留个接口
)

# 将 Retry 对象添加到已经创建的 Session 对象中
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)






# 遵循robots.txt
def check_robots_txt(url):
    can_fetch = True
    # 获取 GitHub Actions 仓库和运行 ID
    run_id = os.getenv('GITHUB_RUN_ID')
    repo_info = os.getenv('GITHUB_REPOSITORY')  # 获取仓库信息
    bot_agent = f'MyGithubActionsBot/1.0 (+https://github.com/{repo_info}; run_id={run_id})'
    
    hostname = urlparse(url).hostname
    robots_url = urljoin(hostname, "/robots.txt")
    
    rp = RobotFileParser()
    rp.set_url(robots_url)
    
    try:
        rp.read()
        can_fetch = rp.can_fetch(bot_agent, url)  # 使用原始url进行权限查询
        if not can_fetch:
            print(f"{hostname} :命中robots.txt，已跳过")
    except Exception as e:
        print(f"检查robots.txt失败: {e}  默认允许")       
    return can_fetch
    
def getIpipaddress(site):
    '''
    return trueip: None or ip
    '''
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.4844.51 Safari/537.36',
               'Host': 'sites.ipaddress.com'}
    url = "https://sites.ipaddress.com/" + site
    trueip = []
    try:
        if not check_robots_txt(url):
            trueip = getIpFromip138(site)
            return trueip
        res = session.get(url, headers=headers, timeout=20, allow_redirects=False)
        soup = BeautifulSoup(res.text, 'html.parser')
        result = soup.find_all(id='tabpanel-dns-a')
        for c in result:
            trueip = re.findall(r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}', c.text)
        if not trueip:
            
            print("sites.ipaddress未查询到" + site + " 已切换源")
            trueip = getIpFromip138(site)
            return trueip
    except Exception as e:
        print("sites.ipaddress查询" + site + " 时出现错误: " + str(e) )
        trueip = getIpFromip138(site)
    print("sites.ipaddress查询" + site + " 完成: " + str(trueip) )
    return trueip


def getIpFromip138(site):
    '''
    return trueip: None or ip
    '''
    url = 'https://site.ip138.com/domain/read.do'
    params = {
        'domain': site,
        'time': int(time.time() * 1000)
        }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.129/130 Safari/537.36',
        'Referer': 'https://site.ip138.com/' + site
            }
    trueip = []
    if check_robots_txt(url):
        trueip = getIpFromipapi(site)
        return trueip
    for i in range(3):
        try:
            res = session.get(url, params=params, headers=headers)
            res = res.json()
            if res["status"] == True:
                for item in res["data"]:
                    trueip.append(item["ip"])
                break
            time.sleep(1)
        except Exception as e:
            print("site.ip138查询" + site + " 时出现错误: " + str(e))
            trueip = getIpFromipapi(site)
    if not trueip:
        print("site.ip138未查询到" + site + "已切换源")
        trueip = getIpFromipapi(site)
    print("site.ip138查询" + site + " 完成: " + str(trueip) )
    return trueip


def getIpFromipapi(site):
    '''
    return trueip: None or ip
    '''
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebkit/737.36(KHTML, like Gecke) Chrome/52.0.2743.82 Safari/537.36',
               'Host': 'ip-api.com'}
    url = "http://ip-api.com/json/%s?lang=zh-CN" % (site)
    trueip = set()
    '''
    该网站允许调用(45次/min)，默认不检查
    if not check_robots_txt(url):
        trueip = getIpFromip138(site)
        return trueip
    '''
    for i in range(3):
        try:
            res = session.get(url, headers=headers, timeout=5)
            res = json.loads(res.text)
            if res["status"] == "success":
                if not trueip:
                    trueip.add(res["query"])
            time.sleep(2)
        except Exception as e:
            print("ip-api.com查询" + site + " 时出现错误: " + str(e))
    print("ip-api.com查询" + site + " 完成: " + str(trueip) )
    return trueip


def getIpFromChinaz(site):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebkit/737.36(KHTML, like Gecke) Chrome/52.0.2743.82 Safari/537.36',
               'Host': 'ipw.cn'}
    url = "http://ipw.cn/ipv6webcheck/?site=" + site
    trueip = None
    try:
        res = session.get(url, headers=headers, timeout=5)
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


class getIpcheck:
    def __init__(self, site):
        self.hosts = getIpipaddress(site)
        self.ports = [443, 80]

    class HostChecker:
        def __init__(self):
            self.lock = threading.Lock()
            self.good_hosts = []
            
        def tcping(self, host, port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)  # 设置超时时间
                sock.connect((host, port))
                print(f"TCP ping to {host}:{port} succeeded")
                with self.lock:
                    self.good_hosts.append(host)
            except socket.error as e:
                print(f"TCP ping to {host}:{port} failed: {e}")
            finally:
                sock.close()

    def check_hosts(self):
        checker = self.HostChecker()
        for port in self.ports:
            checker.good_hosts = []  # 清空好的主机列表
            threads = []  # 创建并启动线程
            for host in self.hosts:
                thread = threading.Thread(target=checker.tcping, args=(host, port))
                thread.start()
                threads.append(thread)
            for thread in threads:  # 等待所有线程完成
                thread.join()

            failure_rate = 1.1
            if self.hosts:
            # 计算失败的测试的比例
                bad_hosts = [host for host in self.hosts if host not in checker.good_hosts]
                failure_rate = len(bad_hosts) / len(self.hosts)

            if failure_rate < 0.9:
                self.hosts = checker.good_hosts

            # 如果有任何好的主机，就停止尝试其他端口
            if checker.good_hosts:
                break
        print(f'最终返回为: {self.hosts}')

def getIpmain(site):
    checker = getIpcheck(site)
    checker.check_hosts()
    return checker.hosts




