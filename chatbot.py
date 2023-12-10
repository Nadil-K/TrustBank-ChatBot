from llama_index.llms import OpenAI
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
import os

documents = SimpleDirectoryReader("./competition").load_data()

embed_model = HuggingFaceEmbedding(model_name='BAAI/bge-large-en-v1.5')

llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo")
service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model, chunk_size=800, chunk_overlap=20)
index = VectorStoreIndex.from_documents(documents, service_context=service_context, show_progress=True)
index.storage_context.persist()

query_engine = index.as_query_engine(similarity_top_k=2, response_mode='tree_summarize')

# response = query_engine.query(
#     "what are the benefits that I can have regarding risk management and portfolio monitoring? What are the charges?"
# )

def answer(question):
    return query_engine.query(question)

if __name__ == "__main__":
    while True:
        question = input("Ask a question: ")
        print(answer(question))