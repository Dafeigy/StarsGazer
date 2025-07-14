from upstash_vector import Index,Vector
import os

GITHUB_USER=os.environ['GITHUB_USER']
GITHUB_TOKEN=os.environ['GITHUB_TOKEN']
database_token=os.environ['DATABASE_TOKEN']
database_url=os.environ["DATABASE_URL"]

base_url = f"https://github.com/{GITHUB_USER}?tab=stars"
index = Index(url=database_url, token=database_token)
res = index.delete(
    ids=[f"id{i}" for i in range(1,120)]
)

# How many vectors are deleted out of the given ids.
print(res.deleted)