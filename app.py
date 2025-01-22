from flask import Flask, render_template, request
import utils.getStarsRepo as search_util

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    results = search_util.search_repos(query)
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
