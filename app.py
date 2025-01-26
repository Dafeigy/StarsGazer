from flask import Flask, render_template, request
import os
import requests
from bs4 import BeautifulSoup
from upstash_vector import Index,Vector
import aiohttp
import asyncio

GITHUB_USER=os.environ['GITHUB_USER']
GITHUB_TOKEN=os.environ['GITHUB_TOKEN']
database_token=os.environ['DATABASE_TOKEN']
database_url=os.environ["DATABASE_URL"]
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"{GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
}

def get_params(GITHUB_USER):
    url = f"https://github.com/{GITHUB_USER}?tab=stars"
    req = requests.get(url, headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0","content-type": "text/html; charset=utf-8"})
    soup=BeautifulSoup(req.text, 'lxml')
    stars_num = soup.find("a", attrs={"aria-current":"page"}).find("span",class_="Counter").get("title").replace(",","")
    user_id = soup.find("a", attrs={"itemprop": "image"}).get("href").replace("https://avatars.githubusercontent.com/u/",'')[:-4]
    return user_id, int(stars_num)//100+1

async def fetch_with_(url, headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()

async def fetch_multiple_urls(github_user, headers):
    user_id, stars_num = get_params(github_user)
    urls = [
    f"https://api.github.com/user/{user_id}/starred?per_page=100&page={i}"
    for i in range(1, stars_num+1)
]
    tasks = [fetch_with_(url, headers) for url in urls]
    return await asyncio.gather(*tasks)

base_url = f"https://github.com/{GITHUB_USER}?tab=stars"
index = Index(url=database_url, token=database_token)
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/asyncupdate")
async def asyncupdate():
    try:
        results = await fetch_multiple_urls(GITHUB_USER, headers)
    except Exception as e:
        print(e)
        return {"res":"Error Fetching <=Github", "len": "null"}
    results = [subitem for item in results for subitem in item]
    chunk_list = [results[i:i+1000] for i in range(0, len(results), 1000)]
    try:
        for cindex, each in enumerate(chunk_list):
            vectors = [
                (f"id{cindex*1000 + index+1}",f"{value['full_name']}: {value['description']}",value) for index,value in enumerate(each)
            ]
            vecdb_res = index.upsert(
                    vectors=vectors
                )
        print(f"[Upstash] Upload data to vecdb: {vecdb_res}.")
        return {"res":vecdb_res,"len":len(results)}
    except Exception as e:
        print(e)
        return {"res": "[Vecdb] Error Indexing data."}
    
    # return {"RepoNums": len(vectors)}
    

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    user_query = data.get('keyword')
    if user_query:
        res = index.query(
            data=user_query,
            top_k=5,
            include_vectors=True,
            include_metadata=True
        )
        return res
    else:
        return {"result": "Error. Cannot get search keywords."}
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
