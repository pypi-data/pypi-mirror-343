# Noir-LLM

> **DISCLAIMER**: This package is for educational purposes only. Use at your own risk. See the [Disclaimer](#disclaimer) section for more details.

A Python package for accessing various LLM models freely and using them in your projects.

## Features

- Access to multiple LLM models through a unified API
- Web search capabilities for supported models
- System prompt customization
- Command-line interface for interactive chat sessions
- Simple Python API for integration into your projects

## Installation

```bash
pip install noir-llm
```

## Quick Start

### Command-Line Interface

List available models:

```bash
noir-llm list
```

Start an interactive chat session:

```bash
noir-llm chat
```

Start a chat session with a specific model:

```bash
noir-llm chat --model glm-4-32b
# or
noir-llm chat --model mistral-31-24b
```

Enable web search for the chat session:

```bash
noir-llm chat --model glm-4-32b --websearch
# or
noir-llm chat --model mistral-31-24b --websearch
```

Send a single message:

```bash
noir-llm send "What is the capital of France?" --model glm-4-32b
# or
noir-llm send "What is the capital of France?" --model llama-3.2-3b
```

### Python API

```python
from noir import NoirClient

# Create a client
client = NoirClient()

# List available models
models = client.get_available_models()
print(f"Available models: {models}")

# Select a model
client.select_model("glm-4-32b")
# or
# client.select_model("mistral-31-24b")

# Set a system prompt
client.set_system_prompt("You are a helpful assistant.")

# Send a message
response = client.send_message("What is the capital of France?")
print(f"Response: {response}")

# Enable web search
response = client.send_message("What are the latest developments in quantum computing?", websearch=True)
print(f"Response with web search: {response}")
```

## Available Models

- GLM-4-32B: A powerful language model with web search capabilities
- Z1-32B: Another powerful language model with web search capabilities
- Z1-Rumination: A model optimized for deep research and analysis
- Mistral-31-24B: A high-quality language model from Venice AI with web search capabilities
- Llama-3.2-3B: A compact but powerful model from Venice AI with web search capabilities

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Publishing to PyPI

This package provides two methods for publishing to PyPI:

### Method 1: Using GitHub Actions (Recommended)

This method uses GitHub Actions for automated publishing. To publish a new version, simply run the publishing script:

```bash
# Bump patch version (0.2.0 -> 0.2.1) and publish
python publish_to_pypi.py

# Bump minor version (0.2.0 -> 0.3.0) and publish
python publish_to_pypi.py --part minor

# Bump major version (0.2.0 -> 1.0.0) and publish
python publish_to_pypi.py --part major
```

The script will:
1. Bump the version number in `noir/__init__.py` and `setup.py`
2. Commit the changes
3. Create a tag
4. Push the changes and tag to GitHub

This will trigger the GitHub Actions workflow, which will build and publish the package to PyPI automatically.

If you want to test the process without pushing to GitHub, you can use:

```bash
python publish_to_pypi.py --no-push
```

### Method 2: Direct Publishing

If you prefer to publish directly to PyPI without using GitHub Actions, you can use the `--direct` option:

```bash
python publish_to_pypi.py --direct
```

This will:
1. Bump the version number in `noir/__init__.py` and `setup.py`
2. Build the package
3. Publish directly to PyPI using the hardcoded credentials

### Setting Up PyPI Credentials

For the GitHub Actions workflow to work, you need to add your PyPI token as a secret:

1. Go to your GitHub repository
2. Click on "Settings" > "Secrets and variables" > "Actions"
3. Click "New repository secret"
4. Add a secret named `PYPI_USERNAME` with value `__token__`
5. Add another secret named `PYPI_PASSWORD` with your PyPI token

## Disclaimer

**IMPORTANT**: This package is provided for educational purposes only. Use at your own risk. The package accesses third-party APIs without official authorization, which may violate terms of service of the respective providers. The authors are not responsible for any consequences resulting from the use of this package, including but not limited to account suspensions, legal actions, or any other damages.

By using this package, you acknowledge that:
- You are using it solely for educational and research purposes
- You understand the potential risks involved
- You take full responsibility for any consequences that may arise from its use

## License

This project is licensed under the MIT License - see the LICENSE file for details.
