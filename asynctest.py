import aiohttp
import asyncio
import os
proxy = "http://127.0.0.1:7890"
GITHUB_TOKEN=os.environ['GITHUB_TOKEN']
async def fetch_with_(url, headers, proxy):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, proxy=proxy) as response:
            return await response.json()

async def fetch_multiple_urls(urls, headers, proxy):
    tasks = [fetch_with_(url, headers, proxy) for url in urls]
    return await asyncio.gather(*tasks)

urls = [
    f"https://api.github.com/user/1567626/starred?per_page=100&page={i}"
    for i in range(1, 25)
]
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"{GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
}

# 运行异步任务并打印结果
async def main():
    results = await fetch_multiple_urls(urls, headers, proxy)
    return results

if __name__ == "__main__":
    import time
    st = time.time()
    loop = asyncio.get_event_loop()
    task = loop.create_task(main())
    loop.run_until_complete(task)
    results = task.result()
    print(f"Time cost:{time.time() - st} seconds")