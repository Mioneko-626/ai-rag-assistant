from fastapi import FastAPI
from openai import OpenAI
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from contextlib import asynccontextmanager
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document

PERSIST_DIR = "/app/chroma_db"

load_dotenv()
api_key = os.getenv("SILICONFLOW_API_KEY") # 确保你的.env里叫这个名
base_url = "https://api.siliconflow.cn/v1"

embeddings = OpenAIEmbeddings(
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url="https://api.siliconflow.cn/v1",
    model="BAAI/bge-m3"
)

# 3. 初始化数据库 (仓库)
db = Chroma(
    persist_directory=PERSIST_DIR,
    embedding_function=embeddings
)

# 4. 初始化 LLM (大脑)
llm = ChatOpenAI(
    api_key=api_key,
    base_url=base_url,
    model="deepseek-ai/DeepSeek-V3"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 强制重新读取并存库，不管文件夹在不在
    print("正在加载知识库...")
    with open("/app/knowledge.txt", "r", encoding="utf-8") as f:
        text = f.read()

    from langchain_text_splitters import CharacterTextSplitter
    from langchain_core.documents import Document

    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    docs = [Document(page_content=x) for x in text_splitter.split_text(text)]

    # 使用 add_documents，如果是空的会自动存入
    db.add_documents(docs)
    print("知识库已刷新，包含文本长度:", len(text))

    yield
    print("服务正在关闭...")

app = FastAPI(lifespan=lifespan)


# --- 修正点2：重写 chat 函数，实现 RAG 闭环 ---
@app.post("/chat/")
async def chat(prompt: str):
    retrieved_docs = db.similarity_search(prompt, k=2)
    context = "\n".join([doc.page_content for doc in retrieved_docs])

    # 直接用这个 llm
    response = llm.invoke(f"已知知识库信息: {context}\n\n问题: {prompt}")
    return {"reply": response.content}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

