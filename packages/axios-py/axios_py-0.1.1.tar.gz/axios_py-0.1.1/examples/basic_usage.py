"""
Basic usage examples for axios-py
"""

from axios import Axios, AxiosRequestConfig

def main():
    # Create an Axios instance
    axios = Axios()

    # Basic GET request
    response = axios.get("https://jsonplaceholder.typicode.com/posts/1")
    print("GET Response:", response.data)

    # GET with query parameters
    config = AxiosRequestConfig(
        params={"userId": 1}
    )
    response = axios.get("https://jsonplaceholder.typicode.com/posts", config)
    print("\nGET with params:", response.data)

    # POST request with JSON data
    data = {
        "title": "Test Post",
        "body": "This is a test post",
        "userId": 1
    }
    response = axios.post("https://jsonplaceholder.typicode.com/posts", data=data)
    print("\nPOST Response:", response.data)

    # PUT request
    update_data = {
        "title": "Updated Post",
        "body": "This post has been updated"
    }
    response = axios.put("https://jsonplaceholder.typicode.com/posts/1", data=update_data)
    print("\nPUT Response:", response.data)

    # DELETE request
    response = axios.delete("https://jsonplaceholder.typicode.com/posts/1")
    print("\nDELETE Response Status:", response.status)

    # Custom headers
    config = AxiosRequestConfig(
        headers={
            "Authorization": "Bearer token123",
            "Custom-Header": "value"
        }
    )
    response = axios.get("https://jsonplaceholder.typicode.com/posts/1", config)
    print("\nResponse with custom headers:", response.data)

if __name__ == "__main__":
    main() 