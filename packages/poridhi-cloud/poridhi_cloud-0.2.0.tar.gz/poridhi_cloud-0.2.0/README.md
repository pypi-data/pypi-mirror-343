# Poridhi Cloud Python SDK

## Overview

The Poridhi Cloud Python SDK provides a comprehensive interface for interacting with the Poridhi Cloud infrastructure. It supports getting machine information, deploying LLMs, and model inference.



## Installation

```bash
pip install poridhi-cloud
```

## Quick Start

### Initializing the Client

```python
from poridhi_cloud import PoridihCloud

# Initialize with default settings
client = PoridihCloud()

# Or specify a custom base URL and API key
client = PoridihCloud(
    base_url='https://api-url',
    api_key='your-api-key-here'
)
```

### Getting Available Machines

```python
# Get information about available machines
machines = client.get_machineId()
print(machines)
```

### Deploy Your Model

```python
# Allocate a worker with specific resources
worker = client.allocate_worker(
    cpu=1,
    memory=3096,
    gpu='nvidia-tesla-t4',
    gpu_count=1,
    image='k33g/ollama-deepseek-coder-runner:0.0.0',
    port=11434,
    machine_id="your-machine-id",
    duration=3600  # Optional duration in seconds
)
print(worker)
```

`After deployment, please wait a few seconds for your deployment to be ready. Collect your workerId from the response JSON.`

### Streaming Text Generation
**Note: Make sure you have an endpoint /api/generate for streaming text generation with JSON request/response format**
```python
# Stream text generation
# Real-time chunk-by-chunk streaming
for token in client.stream_generate(
    worker_id='your-worker-id',
    model='deepseek-coder',
    prompt='Write a Python function to calculate fibonacci numbers',
   
):
    print(token, end='', flush=True)
```

## Authentication

The SDK supports Bearer token authentication using an API key. You can provide the API key in two ways:

1. Directly when initializing the client:
   ```python
   client = PoridihCloud(api_key='your-api-key-here')
   ```

2. Through an environment variable:
   ```bash
   export PORIDHI_CLOUD_API_KEY='your-api-key-here'
   ```

## Configuration

### Environment Variables

- `PORIDHI_CLOUD_URL`: Base URL for the Poridhi Cloud API
- `PORIDHI_CLOUD_API_KEY`: API key for authentication

### Initialization Options

```python
client = PoridihCloud(
    base_url='http://your-server-url',
    api_key='your-api-key'
)
```

## Error Handling

```python
from poridhi_cloud import PoridihCloudError

try:
    worker = client.allocate_worker(...)
except PoridihCloudError as e:
    print(f"Cloud Error: {e}")
```



## License

MIT License

## Example Test Script

Here's a complete example script that walks through all the steps:

### Step-1: Get machine id 

```python
from poridih_cloud import PoridihCloud

# Initialize with default settings
client = PoridihCloud(
    base_url='https://api-url',
    api_key='your-api-key-here'
)



 #Get available machines

machines = client.get_machineId()
print(machines)
```
### Step-2: Deploy a model by allocating a worker

**After deployment, please wait a few seconds for your deployment to be ready.**
```python
from poridih_cloud import PoridihCloud

# Initialize with default settings
client = PoridihCloud(
    base_url='https://api-url',
    api_key='your-api-key-here'
)

worker = client.allocate_worker(
    cpu=1,
    memory=3096,
    gpu='nvidia-tesla-t4',
    gpu_count=1,
    image='k33g/ollama-deepseek-coder-runner:0.0.0',
    port=11434,
    machine_id="machine-id-from-step-1"
)
print(worker)
```
### Step-3:Stream text generation using the deployed model
**Note: Make sure you have an endpoint /api/generate for streaming text generation with JSON request/response format**
```python
from poridih_cloud import PoridihCloud

# Initialize with default settings
client = PoridihCloud(
    base_url='https://api-url',
    api_key='your-api-key-here'
)
for token in client.stream_generate(
    worker_id='worker-id-from-step-2', 
    model='deepseek-coder', 
    prompt='Write a Python function to add two numbers',
    temperature=0.7,
    max_tokens=500,
):
    print(token, end='', flush=True)
```

## Support

For issues and support, please open a GitHub issue in the repository.