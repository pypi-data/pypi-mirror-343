# Poridhi Cloud Python SDK

## Overview

The Poridhi Cloud Python SDK provides a comprehensive interface for interacting with the Poridhi Cloud infrastructure. It supports machine provisioning, worker allocation, resource monitoring, and model inference.

## Features

- Machine Provisioning
- Worker Allocation
- Resource Monitoring
- Model Inference (Streaming)
- Easy-to-use Python Interface

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
    base_url='https://gpu-cloud.poridhi.io',
    api_key='your-api-key-here'
)
```

### Launching a Machine

```python
# Launch a machine with 4 CPUs, 16GB RAM, and 1 NVIDIA GPU
machine = client.launch_machine(
    cpu=4,
    memory=8192,  # Memory in MB
    gpu='nvidia-tesla-t4',
    gpu_count=1
)
print(machine)
```

### Allocating a Worker

```python
# Allocate a worker with specific resources
worker = client.allocate_worker(
    cpu=2,
    memory=2096,
    gpu='nvidia-tesla-t4',
    gpu_count=1,
    image='k33g/ollama-deepseek-coder-runner:0.0.0',
    port=11434,
    machine_id="your-machine-id",
    duration=3600  # Optional duration in seconds
)
print(worker)
```




### Streaming Text Generation

```python
# Stream text generation
# Real-time chunk-by-chunk streaming
for token in client.stream_generate(
    worker_id='your-worker-id',
    model='deepseek-coder',
    prompt='Write a Python function to calculate fibonacci numbers',
    temperature=0.7,
    max_tokens=500
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

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

MIT License

## Support

For issues and support, please open a GitHub issue in the repository.