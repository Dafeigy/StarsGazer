from flask import Flask, render_template, request
import utils.getStarsRepo as gAPI
from config import *
import os
from config import database_token,database_url
from upstash_vector import Index
import random


# GITHUB_USER=os.environ['GITHUB_USER']
GITHUB_USER='dafeigy'
base_url = f"https://github.com/{GITHUB_USER}?tab=stars"
index = Index(url=database_url, token=database_token)
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/updateStatus")
def updateRepoStatus():
    global index
    
    all_urls = gAPI.find_next(base_url)
    res = []
    try:
        for each in all_urls:
            res += gAPI.process_single_page(each)
    except Exception as e:
        return {"data": "Failed => Github"}
    print(f"[Github]Sync starred repos from Github user {GITHUB_USER}: Success.")
    try:
        vectors = [
            (f"id{index+1}",f"{value['RepoName']}: {value['Description']}",value) for index,value in enumerate(res)
        ]
        
        vecdb_res = index.upsert(
            vectors=vectors
        )
        print(f"[Upstash] Upload data to vecdb: {vecdb_res}.")
    except Exception as e:
        # return {"data": "Failed => vecdb"}
        return res

    return {"data": len(vectors)}

@app.route("/search")
def search():
    return all_res[random.randint(0,5):random.randint(5,10)]
if __name__ == '__main__':
    app.run(debug=True)
