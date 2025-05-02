from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from helper import process_query
import uvicorn
import os

app = FastAPI()


class QueryRequest(BaseModel):
    query: str


@app.post("/query/")
async def query_product(request: Request):
    """
    Accepts JSON input like: {"query": "your question here"}
    """
    try:
        body = await request.json()
        query = body.get("query")

        if not query:
            raise HTTPException(
                status_code=400, detail="Missing 'query' in request body.")

        result = process_query(query)
        return {"status": "success", "result": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/health/")
async def health_check():
    """
    Simple health check endpoint for Render or other platforms.
    """
    return {"status": "healthy"}

# Run the app when executed directly (e.g., python app.py)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Default to 8000 for local dev
    uvicorn.run("app:app", host="0.0.0.0", port=port,
                reload=True)  # reload=True for dev
