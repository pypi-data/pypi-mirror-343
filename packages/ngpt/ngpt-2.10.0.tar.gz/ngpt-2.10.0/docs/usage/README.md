# Usage Guide

This section contains comprehensive documentation on how to use nGPT, both as a command-line interface (CLI) tool and as a Python library.

## Table of Contents

- [CLI Usage](cli_usage.md) - Learn how to use nGPT from the command line
- [Library Usage](library_usage.md) - Learn how to integrate nGPT into your Python projects
- [CLI Framework](cli_framework.md) - Learn how to build your own CLI tools with nGPT components

## Overview

nGPT offers three primary ways to use it:

### 1. Command-Line Interface (CLI)

nGPT provides a powerful and intuitive command-line interface that allows you to:

- Chat with AI models using simple commands
- Conduct interactive chat sessions with conversation memory
- Generate and execute shell commands
- Generate clean code without markdown formatting
- Configure API settings and preferences
- And more...

See the [CLI Usage](cli_usage.md) guide for detailed documentation.

### 2. Python Library

nGPT can be imported as a Python library, allowing you to:

- Integrate AI capabilities into your Python applications
- Chat with AI models programmatically
- Generate code and shell commands
- Stream responses in real-time
- Use multiple configurations for different providers
- And more...

See the [Library Usage](library_usage.md) guide for detailed documentation and examples.

### 3. CLI Framework

nGPT can be used as a framework to build your own command-line tools:

- Leverage pre-built components for terminal UI 
- Create interactive chat applications with conversation history
- Implement beautiful markdown rendering with syntax highlighting
- Use real-time streaming with live updates
- Add persistent configuration management
- And more...

See the [CLI Framework](cli_framework.md) guide for detailed documentation and the [CLI Component Examples](../examples/cli_components.md) for practical examples.

## Quick Reference

### CLI Quick Start

```bash
# Basic chat
ngpt "Tell me about quantum computing"

# Interactive chat session
ngpt -i

# Generate shell command
ngpt --shell "list all PDF files recursively"

# Generate code
ngpt --code "function to calculate prime numbers"
```

### Library Quick Start

```python
from ngpt import NGPTClient, load_config

# Load configuration
config = load_config()

# Initialize client
client = NGPTClient(**config)

# Chat with AI
response = client.chat("Tell me about quantum computing")
print(response)

# Generate code
code = client.generate_code("function to calculate prime numbers")
print(code)

# Generate shell command
command = client.generate_shell_command("list all PDF files recursively")
print(command)
```

### CLI Framework Quick Start

```python
from ngpt import NGPTClient, load_config
from ngpt.cli import interactive_chat_session, ColoredHelpFormatter
import argparse

# Create parser with colorized help
parser = argparse.ArgumentParser(
    description="My custom AI assistant",
    formatter_class=ColoredHelpFormatter
)

# Initialize client
client = NGPTClient(**load_config())

# Use nGPT interactive session with custom prompt
interactive_chat_session(
    client=client,
    preprompt="You are a specialized AI assistant for my custom tool",
    prettify=True
)
```

For more detailed information, see the specific usage guides. 