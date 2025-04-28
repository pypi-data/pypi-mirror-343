"""
Complete example demonstrating all features of axios-py
"""

from axios import Axios, AxiosRequestConfig
import json
from typing import Dict, Any, List

class BlogAPI:
    """Example class demonstrating axios-py usage in a real-world scenario"""
    
    def __init__(self, base_url: str = "https://jsonplaceholder.typicode.com"):
        self.axios = Axios()
        self.base_url = base_url
        
    def get_posts(self, user_id: int = None) -> List[Dict[str, Any]]:
        """Get all posts or posts by user ID"""
        config = AxiosRequestConfig()
        if user_id:
            config.params = {"userId": user_id}
            
        response = self.axios.get(f"{self.base_url}/posts", config)
        return response.data
        
    def get_post(self, post_id: int) -> Dict[str, Any]:
        """Get a specific post by ID"""
        response = self.axios.get(f"{self.base_url}/posts/{post_id}")
        return response.data
        
    def create_post(self, title: str, body: str, user_id: int) -> Dict[str, Any]:
        """Create a new post"""
        data = {
            "title": title,
            "body": body,
            "userId": user_id
        }
        response = self.axios.post(f"{self.base_url}/posts", data=data)
        return response.data
        
    def update_post(self, post_id: int, title: str = None, body: str = None) -> Dict[str, Any]:
        """Update an existing post"""
        data = {}
        if title:
            data["title"] = title
        if body:
            data["body"] = body
            
        response = self.axios.put(f"{self.base_url}/posts/{post_id}", data=data)
        return response.data
        
    def delete_post(self, post_id: int) -> bool:
        """Delete a post"""
        response = self.axios.delete(f"{self.base_url}/posts/{post_id}")
        return response.status == 200
        
    def get_post_with_retry(self, post_id: int, max_retries: int = 3) -> Dict[str, Any]:
        """Get a post with retry logic"""
        for attempt in range(max_retries):
            try:
                config = AxiosRequestConfig(timeout=5)
                response = self.axios.get(f"{self.base_url}/posts/{post_id}", config)
                return response.data
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                continue

def main():
    # Create API client
    api = BlogAPI()
    
    try:
        # Get all posts
        print("Getting all posts...")
        posts = api.get_posts()
        print(f"Found {len(posts)} posts")
        
        # Get posts by user
        print("\nGetting posts by user 1...")
        user_posts = api.get_posts(user_id=1)
        print(f"User 1 has {len(user_posts)} posts")
        
        # Get specific post
        print("\nGetting post with ID 1...")
        post = api.get_post(1)
        print(f"Post title: {post['title']}")
        
        # Create new post
        print("\nCreating new post...")
        new_post = api.create_post(
            title="Test Post",
            body="This is a test post",
            user_id=1
        )
        print(f"Created post with ID: {new_post['id']}")
        
        # Update post
        print("\nUpdating post...")
        updated_post = api.update_post(
            post_id=1,
            title="Updated Title",
            body="Updated content"
        )
        print(f"Updated post: {updated_post['title']}")
        
        # Delete post
        print("\nDeleting post...")
        success = api.delete_post(1)
        print(f"Delete successful: {success}")
        
        # Get post with retry
        print("\nGetting post with retry...")
        post = api.get_post_with_retry(1)
        print(f"Retrieved post: {post['title']}")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main() 