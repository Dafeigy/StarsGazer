from upstash_vector import Index
from config import database_url,database_token
index = Index(url=database_url, token=database_token)

index.upsert(
  vectors=[
      ("id1", "Enter data as string", {"metadata_field": "metadata_value"}),
  ]
)

index.query(
  data="Enter data as string",
  top_k=1,
  include_vectors=True,
  include_metadata=True
)