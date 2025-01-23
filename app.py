from flask import Flask, render_template, request
import utils.getStarsRepo as gAPI
import os

# GITHUB_USER=os.environ['GITHUB_USER']
GITHUB_USER='dafeigy'
base_url = f"https://github.com/{GITHUB_USER}?tab=stars"
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/updateStatus")
def updateRepoStatus():
    all_urls = gAPI.find_next(base_url)
    res = []
    for each in all_urls:
        res += gAPI.process_single_page(each)
    vectors = [
        (f"id{index+1}",f"{value['RepoName']}: {value['Description']}",value) for index,value in enumerate(res)
    ]
    return {"All": len(vectors)}


if __name__ == '__main__':
    app.run(debug=True)
