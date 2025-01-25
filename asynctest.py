import aiohttp
import asyncio

async def fetch_with_(url, headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
                return await response.json() 

async def fetch_multiple_urls(urls, headers):
    tasks = [fetch_with_(url, headers) for url in urls]
    return await asyncio.gather(*tasks)

urls = [f"https://api.github.com/user/1567626/starred?per_page=100&page={i}" for i in range(1, 25)]
headers= {
    "Accept": "application/vnd.github+json",
    "Authorization": "Bearer xxxxxxxxxxxxxx",
    "X-GitHub-Api-Version": "2022-11-28"
}

# 运行异步任务并打印结果
async def main():
    results = await fetch_multiple_urls(urls, headers)
    for result in results:
        print(result)

# 运行异步主函数
asyncio.run(main())