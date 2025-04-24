# DevOps MCP Server

A FastMCP-based MCP server providing DevOps tools and integrations.

This a conservative MCP server. It does not add, update or delete anything in your system, does not run any job. Basically, it is read-only. It only retrieves data for analysis, display the information.

So it is safe for DevOps.

## Features

- GitHub repository search and management
- File content retrieval from repositories
- Issue tracking and management
- Code search functionality

## Installation

To install the package, use the following command:

```bash
pip install devops-mcps
```

## Usage

Run the MCP server:
```bash
devops-mcps
```

## Configuration

### Environment Variables

Set the required environment variable for GitHub API access:


```bash
export GITHUB_PERSONAL_ACCESS_TOKEN=your_token_here
```

## UVX Configuration

Install UVX tools:
```bash
uvx install
```

Run with UVX:
```bash
uvx devops-mcps
```

## Transport Configuration

The MCP server supports two transport types:
- `stdio` (default): Standard input/output communication
- `sse`: Server-Sent Events for HTTP-based communication

### Local Usage
```bash
# Default stdio transport
devops-mcps

# SSE transport
devops-mcps --transport sse
```

### UVX Usage
```bash
# Default stdio transport
uvx run devops-mcps

# SSE transport
uvx run devops-mcps-sse
```

## Docker Configuration

Build the Docker image:
```bash
docker build -t devops-mcps .
```

Run the container:
```bash
docker run -p 8000:8000 devops-mcps
```

## GitHub Public and Enterprise Support

This project supports both public GitHub and GitHub Enterprise automatically.

- By default, it connects to public GitHub (`https://api.github.com`).
- To use with GitHub Enterprise, set the `GITHUB_API_URL` environment variable to your enterprise API endpoint (e.g., `https://github.mycompany.com/api/v3`).

**Example:**

```bash
# For public GitHub (default)
export GITHUB_PERSONAL_ACCESS_TOKEN=your_token_here

# For GitHub Enterprise
export GITHUB_PERSONAL_ACCESS_TOKEN=your_token_here
export GITHUB_API_URL=https://github.mycompany.com/api/v3
```

The server will detect the correct API endpoint at runtime.

## VSCode Configuration

To use this MCP server in vs code copilot, there are 2 ways to configure it in VSCode settings.json with different transport types:

### UVX Configuration

#### stdio Transport (default)
```json
"devops-mcps": {
  "type": "stdio",
  "command": "uvx",
  "args": ["devops-mcps"],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxCe",
    "GITHUB_API_URL": "https://github.mycompany.com/api/v3",
    "JENKINS_URL": "jenkins_url_here",
    "JENKINS_USER": "jenkins_username_here",
    "JENKINS_TOKEN": "jenkins_password_here"
  }
}
```

#### SSE Transport
```json
"devops-mcps": {
  "type": "sse",
  "command": "uvx",
  "args": ["devops-mcps-sse"],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxCe",
    "GITHUB_API_URL": "https://github.mycompany.com/api/v3",
    "JENKINS_URL": "jenkins_url_here",
    "JENKINS_USER": "jenkins_username_here",
    "JENKINS_TOKEN": "jenkins_password_here"
  }
}
```

### Docker Configuration

#### stdio Transport (default)
```json
"devops-mcps": {
  "command": "docker",
  "args": [
    "run",
    "-i",
    "huangjien/devops-mcps:latest"
  ],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxxxxxxxxxxxxxxxxxxxxxx2Ce",
    "GITHUB_API_URL": "https://github.mycompany.com/api/v3",
    "JENKINS_URL": "jenkins_url_here",
    "JENKINS_USER": "jenkins_username_here",
    "JENKINS_TOKEN": "jenkins_password_here"
  }
}
```

#### SSE Transport (MCP Server Deployed in Remote Docker Container)
```json
"devops-mcps": {
  "type": "sse",
  "url": "http://[remote ip address]:8000/sse",
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxxxxxxxxxxxxxxxxxxxxxx2Ce",
    "GITHUB_API_URL": "https://github.mycompany.com/api/v3",
    "JENKINS_URL": "jenkins_url_here",
    "JENKINS_USER": "jenkins_username_here",
    "JENKINS_TOKEN": "jenkins_password_here"
  }
}
```

Note: The docker should start like:

```bash
docker run -p 8000:8000 -e TRANSPORT_TYPE=sse -i huangjien/devops-mcps:latest
```

## Development

Install development dependencies:
```bash
uv pip install -e .[dev]
```

or 
```bash
uv sync
```

Recommend to install vs code extension: **ruff**

Or do it in command line:

To lint (check):

```bash
uvx ruff check
```

To format:

```bash
uvx ruff format
```

Run mcp inspector to test or debug:

```bash
npx @modelcontextprotocol/inspector uv run devops-mcps
```

## CI/CD Pipeline

GitHub Actions workflow will automatically:
1. Build and publish Python package to PyPI
2. Build and push Docker image to Docker Hub

### Required Secrets
Set these secrets in your GitHub repository:
- `PYPI_API_TOKEN`: Your PyPI API token
- `DOCKER_HUB_USERNAME`: Your Docker Hub username
- `DOCKER_HUB_TOKEN`: Your Docker Hub access token

Workflow triggers on push to `main` branch.
## Packaging and Publishing

### Install tools

```bash
pip install -U twine build  
```

### Build the package
```bash
python -m build
```

### Upload to PyPI
1. Create a `~/.pypirc` file with your API token:
    ```ini
    [pypi]
    username = __token__
    password = your_pypi_api_token_here
    ```

2. Upload the package:
    ```bash
    twine upload dist/*
    ```

### Important Notes
- Ensure all classifiers in `pyproject.toml` are valid PyPI classifiers
- Remove deprecated license classifiers in favor of SPDX license expressions
- The package will be available at: https://pypi.org/project/devops-mcps/
- Update the version everytime, or when you push, it will show an error: already exists.


## License

MIT