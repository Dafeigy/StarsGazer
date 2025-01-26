import aiohttp
import asyncio
import os
import requests
from bs4 import BeautifulSoup
import lxml
GITHUB_TOKEN=os.environ['GITHUB_TOKEN']
GITHUB_USER='karminski'
proxy = "http://127.0.0.1:7890"

def get_params(GITHUB_USER):
    url = f"https://github.com/{GITHUB_USER}?tab=stars"
    req = requests.get(url, 
                       headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0","content-type": "text/html; charset=utf-8"}, 
                       proxies={"https": "127.0.0.1:7890", "http": "127.0.0.1:7890"}
                       )
    soup=BeautifulSoup(req.text, 'lxml')
    stars_num = soup.find("a", attrs={"aria-current":"page"}).find("span",class_="Counter").get("title").replace(",","")
    user_id = soup.find("a", attrs={"itemprop": "image"}).get("href").replace("https://avatars.githubusercontent.com/u/",'')[:-4]
    return user_id, int(stars_num)//100+1

async def fetch_with_(url, headers, proxy):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, proxy=proxy) as response:
            return await response.json()

async def fetch_multiple_urls(github_user, headers, proxy):
    user_id, stars_num = get_params(github_user)
    urls = [
    f"https://api.github.com/user/{user_id}/starred?per_page=100&page={i}"
    for i in range(1, stars_num+1)
]
    tasks = [fetch_with_(url, headers, proxy) for url in urls]
    return await asyncio.gather(*tasks)


headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"{GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
}

# 运行异步任务并打印结果
async def main():
    results = await fetch_multiple_urls(GITHUB_USER, headers, proxy)
    results = [subitem for item in results for subitem in item]
    return results

if __name__ == "__main__":
    import time
    st = time.time()
    loop = asyncio.get_event_loop()
    task = loop.create_task(main())
    loop.run_until_complete(task)
    results = task.result()
    print(len(results))
    print(f"Time cost:{time.time() - st} seconds")