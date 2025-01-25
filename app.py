from flask import Flask, render_template, request
import utils.getStarsRepo as gAPI
import os
from upstash_vector import Index


# GITHUB_USER=os.environ['GITHUB_USER']
GITHUB_USER=os.environ['GITHUB_USER']
database_token=os.environ['DATABASE_TOKEN']
database_url=os.environ["DATABASE_URL"]
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
            (f"id{index+1}",f"{value['RepoName']}: {value['Description']}",value) for index,value in enumerate(res[::-1])
        ]
        
        vecdb_res = index.upsert(
            vectors=vectors
        )
        print(f"[Upstash] Upload data to vecdb: {vecdb_res}.")
        return {"RepoNums": len(vectors)}
    except Exception as e:
        # return {"data": "Failed => vecdb"}
        return res


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
