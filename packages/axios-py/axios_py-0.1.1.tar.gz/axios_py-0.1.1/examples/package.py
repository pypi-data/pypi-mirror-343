from axios import Axios

# Create an instance
axios = Axios()

# Make a GET request
response = axios.get("https://api.example.com/data")
print(response.data)

# Make a POST request
response = axios.post(
    "https://api.example.com/data",
    data={"key": "value"}
)
print(response.data)