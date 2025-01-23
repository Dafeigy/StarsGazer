import requests
from bs4 import BeautifulSoup
import lxml
from typing import List, Optional


proxy = {
    'https': "127.0.0.1:7890",
    'http': "127.0.0.1:7890"
}
def find_next(base_url: str, 
             max_depth: int = 100, 
             current_depth: int = 0,
             url_list: Optional[List[str]] = None) -> List[str]:
    """
    递归爬取所有URL
    :param base_url: 当前要爬取的URL
    :param max_depth: 最大递归深度，防止无限递归
    :param current_depth: 当前递归深度
    :param url_list: 存储所有URL的列表
    :return: 包含所有URL的列表
    """
    # 初始化URL列表
    if url_list is None:
        url_list = []
    
    # 添加当前URL到列表
    url_list.append(base_url)
    
    if current_depth >= max_depth:
        print(f"达到最大递归深度 {max_depth}")
        return url_list

    try:
        req = requests.get(base_url, headers=headers,proxies=proxy, verify=False)
        req.raise_for_status()
        
        soup = BeautifulSoup(req.text, 'lxml')
        search_field = soup.find("div", class_="BtnGroup")
        
        if not search_field:
            return url_list
            
        urls = search_field.find_all("a", attrs={"rel": "nofollow"})
        
        for each in urls:
            if each.text == "Next":
                next_url = each.get("href")
                # print(f"当前深度: {current_depth}, 找到下一个URL: {next_url}")
                return find_next(base_url=next_url, 
                              max_depth=max_depth,
                              current_depth=current_depth + 1,
                              url_list=url_list)
        
        return url_list
        
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return url_list

def process_single_page(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
        "content-type": "text/html; charset=utf-8"
        }
    req = requests.get(url, headers=headers,verify=False,proxies=proxy)
    soup = BeautifulSoup(req.text, "lxml")
    search_field = soup.find('div', class_ = "col-lg-12")
    temp = [each.find("p") for each in search_field.findAll("div", class_='py-1')]
    descriptions = [each.text.strip().replace("\n","") if each else "Woops! there is No description about this project" for each in temp]
    base_url = "https://github.com"
    links = [base_url+each.find("a")['href'] for each in search_field.findAll("h3")]
    names = [each.split("/")[-1] for each in links]
    update_time = [each.get("datetime") for each in search_field.findAll("relative-time")]
    return [{"RepoName":name, "Description":des, "Link": link, "UpdateTime": update}for name, des, link, update in zip(names, descriptions, links, update_time)]
# 请求头配置
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
    "content-type": "text/html; charset=utf-8"
}

def get_repo_details(url):
    """
    TODO: This will be my new year project
    """
    pass
# 示例用法
if __name__ == "__main__":
    start_url = "https://github.com/dafeigy?tab=stars"
    all_urls = find_next(start_url)
    print("收集到的所有URL:")
    for url in all_urls:
        print(url)
