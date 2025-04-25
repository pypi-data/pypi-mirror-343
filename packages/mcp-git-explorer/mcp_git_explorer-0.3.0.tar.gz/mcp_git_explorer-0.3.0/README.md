# MCP Git Explorer

Simple MCP (Model Context Protocol) server for fetching the remote git repository content as a structured text file.

## Features

- Clone and analyze Git repositories
- Generate a structured text representation of repository contents
- Quickly estimate codebase size and token count without retrieving all content
- Support for public repositories and private GitLab repositories with token authentication
- Tokenization counting using OpenAI's tiktoken library
- Respect for .gitignore and .repomixignore patterns
- Skip binary files and empty text files
- Integration with Claude's Model Context Protocol

## Installation

### From PyPI

```bash
pip install mcp-git-explorer
```

### Using uv

```bash
uv pip install mcp-git-explorer
```

### Direct execution with uvx (without installation)

```bash
uvx mcp-git-explorer
```

## Usage

### As a command-line tool

```bash
# Basic usage
mcp-git-explorer

# Using SSE transport
mcp-git-explorer --transport sse

# Providing GitLab token
mcp-git-explorer --gitlab-token YOUR_TOKEN
```

### Environment Variables

- `GIT_EXPLORER_GITLAB_TOKEN`: Your GitLab personal access token for accessing private repositories

### In Claude

MCP Git Explorer provides Claude with the ability to:

1. Explore Git repositories without needing to manually download and upload files
2. Access the full contents of repositories, with automatic token counting
3. Navigate through repository structure and file contents
4. Quickly assess repository size before deciding whether to retrieve full content

#### When to use which tool

- Use `estimate_codebase` when you want to quickly check the size and structure of a repository before analyzing its contents. This is especially useful for large repositories where you need to check if retrieving the full content is feasible within token limits.
- Use `get_codebase` when you need to analyze the actual code and content of the files in the repository.

#### Available Tools

- `get_codebase(repo_url: str, use_token: bool = True) -> str`: Clone and analyze a Git repository, returning full file contents
- `estimate_codebase(repo_url: str, use_token: bool = True) -> str`: Quick analysis providing repository statistics including file count, structure, and token estimation
- `check_gitlab_token_status() -> str`: Check if a GitLab token is configured

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/jmiedzinski/mcp-git-explorer.git
cd mcp-git-explorer

# Install development dependencies
uv pip install -e ".[dev]"
```

### Running locally

```bash
# Run directly
python -m mcp_git_explorer.cli

# Run via MCP CLI
mcp dev mcp_git_explorer/cli.py

# Run via uvx
uvx mcp-git-explorer
```

## License

MIT
