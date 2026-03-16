import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma

load_dotenv()
API_KEY = os.getenv("SILICONFLOW_API_KEY")
BASE_URL = "https://api.siliconflow.cn/v1"

embeddings = OpenAIEmbeddings(api_key=API_KEY, base_url=BASE_URL, model="BAAI/bge-m3")
db = Chroma(persist_directory="/app/chroma_db", embedding_function=embeddings)
llm = ChatOpenAI(api_key=API_KEY, base_url=BASE_URL, model="deepseek-ai/DeepSeek-V3")