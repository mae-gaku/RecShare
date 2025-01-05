# NOTE: https://qiita.com/nmorishita/items/dfe482d8eb7a1d6f0d9f#rag

from llama_index import SimpleDirectoryReader, VectorStoreIndex, ServiceContext
from llama_index.text_splitter import SentenceSplitter

# Documentの作成
documents = SimpleDirectoryReader("./data").load_data()

# Nodeの作成
text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=10)

# ServiceContextの作成
service_context = ServiceContext.from_defaults(text_splitter=text_splitter)

# indexの作成
index = VectorStoreIndex.from_documents(
    documents, service_context=service_context
)

# Indexを保存
index.storage_context.persist(persist_dir="<persist_dir>")

# Queryを実行
query_engine = index.as_query_engine()
response = query_engine.query(
    "Write an email to the user given their background information."
)
print(response)


