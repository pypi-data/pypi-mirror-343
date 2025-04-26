# Marqus Manner Module

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-green)
[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)

A comprehensive security analysis tool for Model Context Protocol (MCP) servers that performs vulnerability scanning and AI Bill of Materials (AIBOM) analysis.

## Overview

Marqus Manner Module is a security tool designed to scan Model Context Protocol (MCP) servers for vulnerabilities and potential attack vectors. It performs detailed analysis of MCP tools, prompts, and resources, providing trust scoring and security recommendations.

### Key Features

- **Comprehensive MCP Server Scanning**: Automatically discovers and analyzes MCP servers from standard configuration locations
- **AI Bill of Materials (AIBOM) Analysis**: Evaluates security profiles of AI components
- **Active & Passive Scanning Modes**: Choose between deep, API-based scanning or fast, local analysis
- **Whitelisting Mechanism**: Maintain trusted components to reduce noise in scanning results
- **Cross-Reference Security Checks**: Detect potential cross-origin vulnerabilities between servers
- **Detailed Reporting**: Rich console output with comprehensive security findings

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Install via pip

```bash
pip install marqus-manner
```

### Install from source

```bash
git clone https://github.com/marqus-ai/marqus-manner.git
cd marqus-manner
pip install -e .
```

## Quick Start

### 1. Installation

```bash
pip install marqus-manner
```

### 2. Basic Usage

Scan all detected Model Context Protocol servers:

```bash
marqus scan
```

Perform AIBOM security analysis:

```bash
marqus aibom
```

Show installed MCP tools without security checks:

```bash
marqus inspect
```

### 3. Advanced Usage

Add trusted tools to whitelist:

```bash
# View current whitelist
marqus whitelist

# Add a trusted tool
marqus whitelist tool "ToolName" "tool-hash-value"
```

Enable active scanning with API integration:

```bash
marqus scan --active-scan --api-key YOUR_API_KEY
```

Configure custom storage location:

```bash
marqus scan --storage-file ~/custom/marqus/data
```

## Usage

### Command Line Interface

The module provides a comprehensive CLI with several commands:

```
marqus [--debug] [--log-to-console] COMMAND [OPTIONS]
```

Global options:
- `--debug`: Enable debug logging
- `--log-to-console`: Send logs to console in addition to log file

Commands:
- `scan`: Scan MCP servers for security vulnerabilities
- `aibom`: Perform AIBOM security analysis on MCP servers
- `inspect`: Show details of MCP entities without security checks
- `whitelist`: Manage trusted tools and components
- `help`: Display help information

### Scan Command

The default command for scanning MCP servers:

```bash
marqus scan [OPTIONS] [FILES...]
```

Options:
- `--storage-file PATH`: Path to storage directory (default: ~/.marqus-manner)
- `--base-url URL`: Base URL for the AIBOM scanning API
- `--verify-url URL`: Base URL for the verification API
- `--checks-per-server N`: Number of checks to perform on each server
- `--server-timeout SECONDS`: Number of seconds to wait while trying an MCP server
- `--suppress-mcpserver-io`: Suppress the output of the MCP server (default: True)
- `--aibom`: Enable AIBOM security analysis
- `--active-scan`: Enable active scanning (more thorough but potentially slower)
- `--api-key KEY`: API key for scanning services

### AIBOM Command

Dedicated command for AIBOM security analysis:

```bash
marqus aibom [OPTIONS] [FILES...]
```

Options are similar to the scan command.

### Whitelist Command

Manage the whitelist of trusted MCP entities:

```bash
marqus whitelist [OPTIONS] [TYPE] [NAME] [HASH]
```

Options:
- `--storage-file PATH`: Path to storage directory (default: ~/.marqus-manner)
- `--reset`: Reset the whitelist
- `--local-only`: Do not contribute to the global whitelist

Arguments:
- `TYPE`: Entity type (tool, prompt, resource)
- `NAME`: Entity name
- `HASH`: Entity hash

## Advanced Usage

### Active vs. Passive Scanning

The module supports two scanning modes:

- **Passive Scanning (Default)**: Faster local analysis without API calls
- **Active Scanning**: More thorough analysis using the AIBOM scanning API

To enable active scanning:

```bash
marqus scan --active-scan --api-key YOUR_API_KEY
```

### Custom Configuration Paths

By default, Marqus Manner scans well-known MCP configuration locations. You can specify custom paths:

```bash
marqus scan /path/to/custom/mcp_config.json
```

### API Integration

For enterprise users, the module supports integration with the AIBOM scanning API:

```bash
marqus scan --aibom --active-scan --api-key YOUR_API_KEY
```

## Configuration

The module creates a storage directory at `~/.marqus-manner` which contains:

- Scan history
- Whitelist database
- Log files

You can specify a custom storage location with the `--storage-file` option.

## Testing

The Marqus Manner Module includes a comprehensive test suite to ensure functionality and reliability. Tests are organized into unit tests and end-to-end (e2e) tests.

### Running Tests

To run the complete test suite:

```bash
pytest
```

To run unit tests only:

```bash
pytest tests/unit/
```

To run e2e tests only:

```bash
pytest tests/e2e/
```

To run tests with coverage reporting:

```bash
pytest --cov=marqus_manner tests/
```

### Test Structure

- **Unit Tests**: Validate individual components in isolation
  - `test_marqus_scanner.py`: Tests the core scanning functionality
  - `test_mcp_client.py`: Tests the Model Context Protocol client
  - `test_storage_file.py`: Tests the persistent storage mechanism
  - `test_utils.py`: Tests utility functions

- **End-to-End Tests**: Test complete workflows
  - `test_full_scan_flow.py`: Tests the entire scanning process

### Mock Infrastructure

The test suite uses pytest fixtures and mocks to simulate:
- Model Context Protocol (MCP) servers
- Tool responses
- API calls
- File system operations

This allows testing without requiring actual MCP server connections.

### Test Status

All core functionality is covered by the test suite and working properly:
- Scanner initialization and scanning logic
- Storage file persistence and whitelist management
- MCP client configuration file parsing
- Utility functions for command argument processing
- End-to-end testing for the complete scan workflow

Note: For running async tests, you'll need to install pytest-asyncio with:
```bash
pip install pytest-asyncio
```

## Troubleshooting

### Common Issues

1. **Server Timeout**: Increase the timeout value with `--server-timeout`
2. **API Connection Failures**: Check your API key and network connectivity
3. **False Positives**: Use the whitelist command to suppress trusted components

### Debug Mode

Enable debug mode for verbose logging:

```bash
marqus --debug --log-to-console scan
```

Logs are stored in `~/.marqus-manner/logs/marqus.log`

## Security Recommendations

- Regularly update the Marqus Manner Module to get the latest security checks
- Use the whitelist feature for trusted components rather than disabling checks
- For production environments, perform active scans with API integration
- Audit custom prompts and tools for potential security vulnerabilities

## Contributing

We welcome contributions to the Marqus Manner Module! Here's how to get started:

### Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/marqus-manner.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate the environment: `source venv/bin/activate` (Unix) or `venv\Scripts\activate` (Windows)
5. Install development dependencies: `pip install -e ".[dev]"`

### Development Workflow

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Run tests: `pytest`
4. Format code: `black . && isort .`
5. Verify type checking: `mypy .`
6. Commit your changes: `git commit -m "Add your meaningful commit message"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a pull request

### Code Style

This project follows:
- [PEP 8](https://www.python.org/dev/peps/pep-0008/) for code style
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) for docstrings

We use the following tools to enforce style:
- Black for code formatting
- isort for import sorting
- mypy for type checking

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For bug reports and feature requests, please open an issue on our [GitHub repository](https://github.com/marqus-ai/marqus-manner).

For commercial support, contact dev-support@marqus.ai