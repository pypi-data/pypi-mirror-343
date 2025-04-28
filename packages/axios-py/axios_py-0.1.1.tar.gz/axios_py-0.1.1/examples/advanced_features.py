"""
Advanced features examples for axios-py
"""

from axios import Axios, AxiosRequestConfig
import time

def main():
    # Create an Axios instance
    axios = Axios()

    # Timeout example
    try:
        config = AxiosRequestConfig(timeout=0.1)  # 100ms timeout
        response = axios.get("https://httpbin.org/delay/1", config)
    except Exception as e:
        print("Timeout error:", str(e))

    # Response type handling
    config = AxiosRequestConfig(response_type="text")
    response = axios.get("https://jsonplaceholder.typicode.com/posts/1", config)
    print("\nText response:", response.data)

    # Custom status validation
    def validate_status(status):
        return 200 <= status < 300 or status == 404

    config = AxiosRequestConfig(
        validate_status=validate_status
    )
    response = axios.get("https://jsonplaceholder.typicode.com/posts/999", config)
    print("\nResponse with custom status validation:", response.status)

    # Multiple requests with different configurations
    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/3"
    ]

    for url in urls:
        config = AxiosRequestConfig(
            headers={"X-Request-ID": str(time.time())}
        )
        response = axios.get(url, config)
        print(f"\nResponse from {url}:", response.data)

    # Error handling example
    try:
        response = axios.get("https://nonexistent-domain.com")
    except Exception as e:
        print("\nError handling example:", str(e))

if __name__ == "__main__":
    main() 