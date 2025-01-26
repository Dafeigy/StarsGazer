import aiohttp
import asyncio
import os
import requests
from bs4 import BeautifulSoup
import lxml

import time
GITHUB_TOKEN=os.environ['GITHUB_TOKEN']
GITHUB_USER='karminski'
user_id = "1567626"
proxy = "http://127.0.0.1:7890"
urls = [
        f"https://api.github.com/user/{user_id}/starred?per_page=100&page={i}"
        for i in range(1, 25)
]

async def fetch_with_(url, headers, proxy):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, proxy=proxy) as response:
            return await response.json()

async def fetch_multiple_urls(headers, proxy):
    tasks = [fetch_with_(url, headers, proxy) for url in urls]
    return await asyncio.gather(*tasks)

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"{GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
}
async def main():
    results = await fetch_multiple_urls(headers, proxy)
    results = [subitem for item in results for subitem in item]
    return results

def get_single_sync(url):
    req = requests.get(url, headers=headers,proxies={"https":"127.0.0.1:7890","http":"127.0.0.1:7890"})
    return req.json()
if __name__ == "__main__":
    st = time.time()
    sync_results = []
    print("Using Sync method to get results now...")
    for index, each in enumerate(urls):
        # print(f"Sync Processing {index + 1}")
        sync_results.append(get_single_sync(each))
    sync_results = [subitem for item in sync_results for subitem in item]
    print(f"All Sync results len: {len(sync_results)}")
    print(f"Sync Time Cost:{time.time() - st} seconds")
    st = time.time()
    print("Using Async method to get results now...")
    loop = asyncio.get_event_loop()
    task = loop.create_task(main())
    loop.run_until_complete(task)
    async_results = task.result()
    print(f"All Async results len: {len(async_results)}")
    print(f"Async Time Cost:{time.time() - st} seconds")