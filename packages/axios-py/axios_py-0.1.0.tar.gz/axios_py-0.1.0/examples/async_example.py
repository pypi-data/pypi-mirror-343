"""
Example showing async and rate limiting features
"""

import asyncio
from axios import Axios, AxiosRequestConfig

async def main():
    # Create an Axios instance
    async with Axios() as axios:
        # Set global rate limit to 2 requests per second
        axios.set_rate_limit(requests_per_second=2.0, burst_size=2)
        
        # Set specific rate limit for an endpoint
        axios.set_rate_limit(
            endpoint="https://jsonplaceholder.typicode.com/posts",
            requests_per_second=1.0,
            burst_size=1
        )
        
        # Make multiple async requests
        tasks = [
            axios.aget("https://jsonplaceholder.typicode.com/posts/1"),
            axios.aget("https://jsonplaceholder.typicode.com/posts/2"),
            axios.aget("https://jsonplaceholder.typicode.com/posts/3")
        ]
        
        # Execute requests concurrently
        responses = await asyncio.gather(*tasks)
        
        # Process responses
        for response in responses:
            print(f"Status: {response.status}")
            print(f"Data: {response.data}")
            print("---")
            
        # Make a POST request with rate limiting
        data = {
            "title": "Test Post",
            "body": "This is a test post",
            "userId": 1
        }
        response = await axios.apost(
            "https://jsonplaceholder.typicode.com/posts",
            data=data
        )
        print("\nPOST Response:")
        print(f"Status: {response.status}")
        print(f"Data: {response.data}")

if __name__ == "__main__":
    asyncio.run(main()) 