# axios-py

A Python HTTP client inspired by Axios, featuring both synchronous and asynchronous support.

## Features

- Promise-like interface with async/await support
- Unified API for sync & async requests
- Request and response interceptors
- Global & per-request configuration
- Automatic JSON parsing
- Retry mechanism with exponential backoff
- Cancelable requests
- Timeout control
- File upload/download progress tracking
- FastAPI integration
- Rate limiting support

## Installation

```bash
pip install axios-py
```

For FastAPI support:
```bash
pip install axios-py[fastapi]
```

## Quick Start

### Basic Usage

```python
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
```

### Async Usage

```python
import asyncio
from axios import Axios

async def main():
    async with Axios() as axios:
        # Make async requests
        response = await axios.aget("https://api.example.com/data")
        print(response.data)

asyncio.run(main())
```

### FastAPI Integration

```python
from fastapi import FastAPI, Depends
from axios import Axios, AxiosRequestConfig
from axios.fastapi import get_axios

app = FastAPI()

# Create an Axios dependency
axios_dependency = get_axios()

@app.get("/data")
async def get_data(axios: Axios = Depends(axios_dependency)):
    response = await axios.aget("https://api.example.com/data")
    return response.data
```

## Documentation

For detailed documentation, please visit [the documentation site](https://axios-py.readthedocs.io/).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 