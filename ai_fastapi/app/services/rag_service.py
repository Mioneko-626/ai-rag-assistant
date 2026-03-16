from app.core.config import db, llm
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document
import os


# 初始化加载逻辑
def init_knowledge():
    # 这里加个简单的检查，避免重复存入
    if not os.path.exists("/app/chroma_db"):
        with open("/app/knowledge.txt", "r", encoding="utf-8") as f:
            text = f.read()
        splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
        docs = [Document(page_content=x) for x in splitter.split_text(text)]
        db.add_documents(docs)


# 关键：这里必须使用 yield 把内容像水流一样“蹦”出来
def get_answer_stream(prompt: str):
    retrieved_docs = db.similarity_search(prompt, k=2)
    context = "\n".join([doc.page_content for doc in retrieved_docs])

    # 使用 stream() 替代 invoke()
    for chunk in llm.stream(f"已知知识: {context}\n\n问题: {prompt}"):
        yield chunk.content