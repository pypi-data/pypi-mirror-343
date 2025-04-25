# Promptlyzer Client

Python client library for the Promptlyzer API.

## Version

0.2.1

## Installation

```bash
pip install promptlyzer
```

## Features

- Prompt management and versioning
- Automatic fetching of the latest prompt versions
- Caching and automatic updates
- Connection pooling and async support

## Basic Usage

```python
from promptlyzer import PromptlyzerClient

# Create a client
client = PromptlyzerClient(
    api_url="https://api.promptlyzer.com",
    email="your-email@example.com",
    password="your-password",
    environment="dev"  # or "staging", "prod"
)

# Get a specific prompt (always returns the latest version)
prompt = client.get_prompt("project-id", "prompt-name")
print(prompt)

# List all prompts in a project
prompts = client.list_prompts("project-id")
print(prompts)
```

## Using PromptManager

PromptManager automatically keeps prompts up-to-date in the background:

```python
from promptlyzer import PromptlyzerClient, PromptManager

# Create a client
client = PromptlyzerClient(
    api_url="https://api.promptlyzer.com",
    email="your-email@example.com",
    password="your-password"
)

# Callback function when a prompt is updated
def on_prompt_updated(prompt_name, prompt_data):
    print(f"Prompt updated: {prompt_name}")
    print(f"New version: {prompt_data.get('current_version')}")

# Create a PromptManager
manager = PromptManager(
    client=client,
    project_id="your-project-id",
    update_interval=180,  # Check for updates every 3 minutes
    on_update_callback=on_prompt_updated
)

# Start the manager
manager.start()

# Get a prompt (from cache)
prompt = manager.get_prompt("prompt-name")

# Stop the manager when done
manager.stop()
```

## Command Line Interface

Promptlyzer provides a command line interface:

```bash
# Get a specific prompt
promptlyzer get your-project-id prompt-name

# List all prompts in a project
promptlyzer list your-project-id

# Monitor prompts for updates
promptlyzer monitor your-project-id
```

## Environment Variables

Promptlyzer supports the following environment variables:

- `PROMPTLYZER_API_URL`: API URL
- `PROMPTLYZER_EMAIL`: User email
- `PROMPTLYZER_PASSWORD`: User password
- `PROMPTLYZER_TOKEN`: API token (if available)

## Using with Docker

### Docker Compose Example

```yaml
version: '3'

services:
  app:
    image: your-app-image
    environment:
      - PROMPTLYZER_API_URL=https://api.promptlyzer.com
      - PROMPTLYZER_EMAIL=your-email@example.com
      - PROMPTLYZER_PASSWORD=your-password
    volumes:
      - ./app:/app
    command: python /app/main.py
```

### Dockerfile Example

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install promptlyzer
RUN pip install promptlyzer

COPY . .

# Set environment variables
ENV PROMPTLYZER_API_URL=https://api.promptlyzer.com
# Credentials should be passed at runtime or via Docker secrets

CMD ["python", "main.py"]
```

### Running the Container

```bash
docker run -e PROMPTLYZER_EMAIL=your-email@example.com \
           -e PROMPTLYZER_PASSWORD=your-password \
           your-app-image
```

## Changes in 0.2.1

- Fixed API endpoint URL structure
- Removed "version" parameter to always fetch the latest prompt
- Improved thread management in PromptManager

## License

MIT