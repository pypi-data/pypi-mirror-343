from fastapi import FastAPI, Depends, HTTPException, Request
import uvicorn
import os
import httpx
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

# 创建 FastAPI 应用
app = FastAPI(title="LangSearch MCP Server")

# 检查 API Key
def get_api_key():
    api_key = os.environ.get("LANGSEARCH_API_KEY")
    if not api_key:
        raise HTTPException(status_code=401, detail="API Key not found in environment variables")
    return api_key

# Web 搜索的模型
class WebSearchRequest(BaseModel):
    query: str
    limit: int = 10
    offset: int = 0

# 文档重排序的模型
class Document(BaseModel):
    text: str

class RerankRequest(BaseModel):
    query: str
    documents: List[Document]

# 实现 Web 搜索 API
@app.post("/api/web-search")
async def web_search(request: WebSearchRequest, api_key: str = Depends(get_api_key)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.langsearch.com/v1/web-search",
                json={
                    "query": request.query,
                    "limit": request.limit,
                    "offset": request.offset
                },
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
            )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"LangSearch API 错误: {response.text}"
            )
        
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理请求时出错: {str(e)}")

# 实现文档重排序 API
@app.post("/api/rerank")
async def rerank_documents(request: RerankRequest, api_key: str = Depends(get_api_key)):
    try:
        # 准备文档
        docs = [{"text": doc.text} for doc in request.documents]
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.langsearch.com/v1/rerank",
                json={
                    "query": request.query,
                    "documents": docs
                },
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
            )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"LangSearch API 错误: {response.text}"
            )
        
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理请求时出错: {str(e)}")

# 健康检查端点
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

def main():
    """Entry point for the MCP server."""
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting LangSearch MCP server on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
