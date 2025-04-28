"""
Example FastAPI application using axios-py
"""

from fastapi import FastAPI, Depends
from axios import Axios, AxiosRequestConfig
from axios.fastapi import get_axios
import asyncio

app = FastAPI(title="Axios-py FastAPI Example")

# Create a global Axios configuration
global_config = AxiosRequestConfig(
    headers={"User-Agent": "axios-py-fastapi-example"},
    timeout=30.0
)

# Create an Axios dependency with global config
axios_dependency = get_axios(global_config)

@app.get("/posts")
async def get_posts(axios: Axios = Depends(axios_dependency)):
    """Get all posts from JSONPlaceholder"""
    response = await axios.aget("https://jsonplaceholder.typicode.com/posts")
    return response.data

@app.get("/posts/{post_id}")
async def get_post(post_id: int, axios: Axios = Depends(axios_dependency)):
    """Get a specific post by ID"""
    response = await axios.aget(f"https://jsonplaceholder.typicode.com/posts/{post_id}")
    return response.data

@app.post("/posts")
async def create_post(
    title: str,
    body: str,
    userId: int,
    axios: Axios = Depends(axios_dependency)
):
    """Create a new post"""
    data = {
        "title": title,
        "body": body,
        "userId": userId
    }
    response = await axios.apost(
        "https://jsonplaceholder.typicode.com/posts",
        data=data
    )
    return response.data

@app.put("/posts/{post_id}")
async def update_post(
    post_id: int,
    title: str,
    body: str,
    axios: Axios = Depends(axios_dependency)
):
    """Update an existing post"""
    data = {
        "title": title,
        "body": body
    }
    response = await axios.aput(
        f"https://jsonplaceholder.typicode.com/posts/{post_id}",
        data=data
    )
    return response.data

@app.delete("/posts/{post_id}")
async def delete_post(post_id: int, axios: Axios = Depends(axios_dependency)):
    """Delete a post"""
    response = await axios.adelete(f"https://jsonplaceholder.typicode.com/posts/{post_id}")
    return {"status": response.status, "message": "Post deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 