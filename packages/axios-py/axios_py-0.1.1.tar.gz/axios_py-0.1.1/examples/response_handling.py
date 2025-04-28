"""
Response handling examples for axios-py
"""

from axios import Axios, AxiosRequestConfig
from typing import Dict, Any

def process_response(response):
    """Example of processing response data"""
    data = response.data
    headers = response.headers
    status = response.status
    
    print(f"\nStatus: {status}")
    print(f"Headers: {headers}")
    print(f"Data: {data}")
    
    return data

def main():
    # Create an Axios instance
    axios = Axios()

    # Basic response handling
    response = axios.get("https://jsonplaceholder.typicode.com/posts/1")
    data = process_response(response)

    # Handling different response types
    config = AxiosRequestConfig(response_type="text")
    response = axios.get("https://jsonplaceholder.typicode.com/posts/1", config)
    print("\nText response type:", type(response.data))

    # Working with response headers
    response = axios.get("https://jsonplaceholder.typicode.com/posts/1")
    content_type = response.headers.get("content-type", "")
    print("\nContent-Type:", content_type)

    # Processing multiple responses
    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2"
    ]

    all_data = []
    for url in urls:
        response = axios.get(url)
        data = process_response(response)
        all_data.append(data)

    print("\nAll collected data:", all_data)

    # Error handling with response
    try:
        response = axios.get("https://jsonplaceholder.typicode.com/posts/999")
        if response.status == 404:
            print("\nResource not found")
        else:
            process_response(response)
    except Exception as e:
        print("\nError occurred:", str(e))

if __name__ == "__main__":
    main() 