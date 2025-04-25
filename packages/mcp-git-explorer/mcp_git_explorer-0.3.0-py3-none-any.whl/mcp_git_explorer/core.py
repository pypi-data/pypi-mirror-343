import os
import tempfile
import shutil
from pathlib import Path
import textwrap
from urllib.parse import urlparse
import fnmatch
from mcp.server.fastmcp import FastMCP
from .settings import GitExplorerSettings

class GitExplorer:
    """Git Explorer tool for accessing and processing Git repositories."""
    def __init__(self, name="Git Codebase Explorer", settings=None):
        """Initialize the Git Explorer with optional custom name and settings."""
        self.mcp = FastMCP(
            name,
            dependencies=["gitpython", "tiktoken"],
        )
        self.settings = settings or GitExplorerSettings()
        # Register tools
        self.mcp.tool()(self.get_codebase)
        self.mcp.tool()(self.estimate_codebase)
        self.mcp.tool()(self.check_gitlab_token_status)
        self.mcp.tool()(self.get_file)

    def _clone_repository(self, repo_url: str, use_token: bool = True) -> str:
        """Clone a Git repository into a temporary directory and return the path."""
        import git
        from urllib.parse import urlparse
        import shutil
        import tempfile

        authenticated_url = repo_url
        if use_token and self.settings.gitlab_token:
            parsed_url = urlparse(repo_url)
            netloc = f"oauth2:{self.settings.gitlab_token}@{parsed_url.netloc}"
            authenticated_url = parsed_url._replace(netloc=netloc).geturl()

        temp_dir = tempfile.mkdtemp()
        try:
            git.Repo.clone_from(authenticated_url, temp_dir, depth=1)
            # Remove .git directory to save space and simplify processing
            git_dir = os.path.join(temp_dir, ".git")
            if os.path.exists(git_dir):
                shutil.rmtree(git_dir)
            return temp_dir
        except Exception as e:
            shutil.rmtree(temp_dir, ignore_errors=True)
            raise

    def _process_repository(self, repo_url: str, use_token: bool = True):
        """
        Clone and process a Git repository, returning repository information.

        Args:
            repo_url (str): The URL of the Git repository to clone
            use_token (bool): Whether to use GitLab token for authentication

        Returns:
            dict: Repository information including:
                - temp_dir: Path to cloned repository
                - repo_structure: Text representation of repo structure
                - file_count: Number of files in repository
                - files_content: Concatenated file contents (if requested)
                - token_count: Estimated token count
                - error: Error message (if any)
        """
        import git
        import tiktoken

        result = {
            "temp_dir": None,
            "repo_structure": "",
            "file_count": 0,
            "files_content": "",
            "token_count": 0,
            "error": None
        }

        try:
            # Clone the repository
            temp_dir = self._clone_repository(repo_url, use_token)
            result["temp_dir"] = temp_dir

            # Get ignore patterns
            ignore_patterns = []
            gitignore_path = os.path.join(temp_dir, ".gitignore")
            if os.path.exists(gitignore_path):
                with open(gitignore_path, 'r', errors='replace') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            ignore_patterns.append(line)

            repomixignore_path = os.path.join(temp_dir, ".repomixignore")
            if os.path.exists(repomixignore_path):
                with open(repomixignore_path, 'r', errors='replace') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            ignore_patterns.append(line)

            # Generate repository structure
            repo_structure = self._generate_repo_structure(temp_dir)
            result["repo_structure"] = repo_structure

            # Count files and generate content
            files = []
            root_path = Path(temp_dir)
            for path in sorted(root_path.glob("**/*")):
                if path.is_file() and not self._should_ignore_file(path, root_path, ignore_patterns) and not self._is_binary_file(path):
                    try:
                        content = path.read_text(errors='replace')
                        if content and content.strip():
                            files.append(path)
                    except Exception:
                        pass

            result["file_count"] = len(files)

            # Generate files content if needed
            files_content = self._concatenate_files_from_list(root_path, files)
            result["files_content"] = files_content

            # Count tokens
            enc = tiktoken.get_encoding("o200k_base")

            # Create content for token estimation
            sample_content = f"{repo_structure}\n\n{files_content}"
            tokens = enc.encode(sample_content)
            result["token_count"] = len(tokens)

            return result

        except git.GitCommandError as e:
            if "Authentication failed" in str(e):
                result["error"] = (
                    f"Authentication error while accessing repository {repo_url}.\n"
                    "Make sure the repository is public or a valid access token "
                    "has been set in the GIT_EXPLORER_GITLAB_TOKEN environment variable."
                )
            else:
                result["error"] = f"Git error: {str(e)}"
            return result
        except Exception as e:
            result["error"] = f"An error occurred: {str(e)}"
            return result

    def _get_single_file(self, repo_url: str, file_path: str, use_token: bool = True) -> str:
        """Clone a repository and return the content of a single specified file."""
        temp_dir = None
        try:
            temp_dir = self._clone_repository(repo_url, use_token)
            full_path = os.path.join(temp_dir, file_path)
            if not os.path.exists(full_path):
                raise FileNotFoundError(f"The file {file_path} does not exist in the repository.")
            if not os.path.isfile(full_path):
                raise IsADirectoryError(f"The path {file_path} is not a file.")
            with open(full_path, 'r', errors='replace') as f:
                content = f.read()
            return content
        finally:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)

    async def get_file(self, repo_url: str, file_path: str, use_token: bool = True) -> str:
        """
        Fetch the content of a single specified file from a Git repository.

        This tool clones a Git repository from the provided URL, reads the content
        of the specified file, and returns it as a string. The repository is cloned
        with depth=1 for efficiency. If the file does not exist or an error occurs,
        an appropriate error message is returned.

        Args:
            repo_url (str): The URL of the Git repository to clone.
            file_path (str): The relative path to the file within the repository.
            use_token (bool, optional): Whether to use the GitLab token for authentication.
                                       Defaults to True.

        Returns:
            str: The content of the specified file, or an error message if retrieval fails.
        """
        try:
            content = self._get_single_file(repo_url, file_path, use_token)
            return content
        except FileNotFoundError as e:
            return str(e)
        except IsADirectoryError as e:
            return str(e)
        except git.GitCommandError as e:
            if "Authentication failed" in str(e):
                return (
                    f"Authentication error while accessing repository {repo_url}.\n"
                    "Make sure the repository is public or a valid access token "
                    "has been set in the GIT_EXPLORER_GITLAB_TOKEN environment variable."
                )
            else:
                return f"Git error: {str(e)}"
        except Exception as e:
            return f"An error occurred: {str(e)}"

    async def estimate_codebase(self, repo_url: str, use_token: bool = True) -> str:
        """
        Get statistics about a Git repository without downloading all content.

        This tool clones a git repository from the provided URL, analyzes its structure,
        and returns statistical information useful for LLM processing, including:
        - Estimated token count
        - Total file count
        - Repository structure

        Args:
            repo_url (str): The URL of the Git repository to clone
            use_token (bool, optional): Whether to use the GitLab token for authentication.
                                       Defaults to True.

        Returns:
            str: A formatted text representation of the repository statistics

        Raises:
            GitCommandError: If there is an error during the git clone operation
            Exception: For any other errors that occur during processing
        """
        result = None
        temp_dir = None

        try:
            # Process the repository
            result = self._process_repository(repo_url, use_token)
            temp_dir = result["temp_dir"]

            if result["error"]:
                return result["error"]

            # Format the output
            output = textwrap.dedent(f"""
            # Git Repository Statistics: {repo_url}

            ## Summary:
            - Estimated token count (o200k_base encoding): {result["token_count"]:,}
            - Total files: {result["file_count"]:,}

            ## Repository Structure:
            {result["repo_structure"]}
            """).strip()

            return output

        finally:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

    async def get_codebase(self, repo_url: str, use_token: bool = True) -> str:
        """
        Clone a Git repository and generate a structured text file containing its contents.

        This tool clones a git repository from the provided URL, processes its contents,
        and returns a single text file containing the repository structure and the content
        of all files. Binary files and empty text files are excluded. The tool respects
        .gitignore and .repomixignore patterns. The output includes an estimated token count
        using the o200k_base encoding.

        Args:
            repo_url (str): The URL of the Git repository to clone
            use_token (bool, optional): Whether to use the GitLab token for authentication.
                                       Defaults to True.

        Returns:
            str: A formatted text representation of the repository contents, including
                 file structure, estimated token count, and the content of all text files.

        Raises:
            GitCommandError: If there is an error during the git clone operation
            Exception: For any other errors that occur during processing
        """
        result = None
        temp_dir = None

        try:
            # Process the repository
            result = self._process_repository(repo_url, use_token)
            temp_dir = result["temp_dir"]

            if result["error"]:
                return result["error"]

            # Create preamble with token information
            preamble = textwrap.dedent(f"""
            # Git Repository: {repo_url}
            This file contains the complete content of the git repository cloned from:
            {repo_url}
            Estimated token count (o200k_base encoding): {result["token_count"]:,}
            Total files: {result["file_count"]:,}
            Below you'll find the repository structure and the full content of all files.
            Each file is preceded by a separator indicating the beginning of the file and
            followed by a separator indicating the end of the file, along with the full path to the file.

            ## Repository Structure:
            {result["repo_structure"]}

            ## File Contents:
            """).strip()

            # Create final content
            output = f"{preamble}\n\n{result['files_content']}"
            return output

        finally:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

    def check_gitlab_token_status(self) -> str:
        """Check if the GitLab token is configured in the environment.
        Returns:
            A message indicating whether the GitLab token is configured
        """
        if self.settings.gitlab_token:
            return "GitLab token is configured."
        else:
            return (
                "GitLab token is not configured. "
                "Set the GIT_EXPLORER_GITLAB_TOKEN environment variable "
                "to access private GitLab repositories."
            )

    def run(self, transport: str = "stdio") -> None:
        """Run the Git Explorer with the specified transport."""
        self.mcp.run(transport=transport)

    def _should_ignore_file(self, file_path: Path, root_path: Path, ignore_patterns: list[str]) -> bool:
        # Convert to a path relative to the root directory
        rel_path = file_path.relative_to(root_path)
        rel_path_str = str(rel_path).replace(os.sep, '/')
        # Check each pattern
        for pattern in ignore_patterns:
            # Handle pattern formats
            if pattern.startswith('/'):
                # Pattern starts with / - only match from root
                pattern = pattern[1:]
                if fnmatch.fnmatch(rel_path_str, pattern):
                    return True
            elif pattern.endswith('/'):
                # Pattern ends with / - match directories
                if file_path.is_dir() and fnmatch.fnmatch(rel_path_str, pattern[:-1]):
                    return True
            else:
                # Standard pattern - match anywhere in path
                if fnmatch.fnmatch(rel_path_str, pattern):
                    return True
                # Also check if any parent directory matches the pattern
                parts = rel_path_str.split('/')
                for i in range(len(parts)):
                    partial_path = '/'.join(parts[:i+1])
                    if fnmatch.fnmatch(partial_path, pattern):
                        return True
        return False

    def _generate_repo_structure(self, repo_path: str) -> str:
        result = []
        def _add_directory(directory: Path, prefix: str = ""):
            paths = sorted(directory.iterdir(), key=lambda p: (p.is_file(), p.name))
            for i, path in enumerate(paths):
                is_last = i == len(paths) - 1
                result.append(f"{prefix}{'└── ' if is_last else '├── '}{path.name}")
                if path.is_dir():
                    _add_directory(
                        path,
                        prefix + ('151    ' if is_last else '│   ')
                    )
        _add_directory(Path(repo_path))
        return "\n".join(result)

    def _is_binary_file(self, file_path: Path) -> bool:
        """Check if a file is binary by reading its first few thousand bytes."""
        try:
            chunk_size = 8000  # Read first 8K bytes
            with open(file_path, 'rb') as f:
                chunk = f.read(chunk_size)
            # Check for null bytes which usually indicate binary content
            if b'\x00' in chunk:
                return True
            # Check if the file is mostly text by looking at the ratio of printable to non-printable characters
            text_characters = bytes(range(32, 127)) + b'\n\r\t\b'
            # If more than 30% non-printable characters, it's likely binary
            return sum(byte not in text_characters for byte in chunk) / len(chunk) > 0.3
        except Exception:
            # If we can't read it, assume it's binary to be safe
            return True

    def _concatenate_files_from_list(self, root_path: Path, files: list[Path]) -> str:
        """Concatenate the contents of the given files into a single string."""
        result = []
        for path in files:
            rel_path = path.relative_to(root_path)
            try:
                # Read file content
                content = path.read_text(errors='replace')
                # Skip empty files or files with only empty lines
                if not content or not content.strip():
                    continue
                # Add non-empty text file to result
                result.append(f"=====< BEGIN filename: {rel_path} >=====\n")
                result.append(content)
                result.append(f"===== <END filename: {rel_path} >=====\n\n")
            except Exception as e:
                result.append(f"=====< BEGIN filename: {rel_path} >=====\n")
                result.append(f"[Error reading file: {str(e)}]")
                result.append(f"===== <END filename: {rel_path} >=====\n\n")
        return "\n".join(result)

    def _concatenate_files(self, repo_path: str, ignore_patterns: list[str]) -> str:
        """Legacy method - uses _concatenate_files_from_list internally."""
        result = []
        root_path = Path(repo_path)
        # Build a list of all files first, so we can sort them
        all_files = []
        for path in sorted(root_path.glob("**/*")):
            if path.is_file():
                if not self._should_ignore_file(path, root_path, ignore_patterns) and not self._is_binary_file(path):
                    all_files.append(path)

        return self._concatenate_files_from_list(root_path, all_files)