import pytest
from unittest.mock import Mock, patch
from pathlib import Path
import os
import tempfile
import shutil
from mcp_git_explorer import GitExplorer
class TestGitExplorer:

    @pytest.fixture
    def git_explorer(self):
        """Fixture providing GitExplorer instance with mocked settings"""
        with patch('mcp_git_explorer.core.GitExplorerSettings') as mock_settings:
            mock_settings.return_value.gitlab_token = "test_token"
            explorer = GitExplorer()
            return explorer

    # Testy dla get_codebase
    @pytest.mark.asyncio
    async def test_get_codebase_public_repo(self, git_explorer):
        """Test pobierania publicznego repozytorium"""
        repo_url = "https://github.com/test/public-repo.git"
        
        with patch('git.Repo.clone_from') as mock_clone:
            # Przygotowanie mocków i tymczasowego katalogu
            temp_dir = tempfile.mkdtemp()
            test_file = Path(temp_dir) / "test.py"
            test_file.write_text("def test(): pass")
            
            mock_clone.return_value = None
            
            result = await git_explorer.get_codebase(repo_url)
            
            assert "test.py" in result
            assert "def test(): pass" in result
            assert "Estimated token count" in result
            
            shutil.rmtree(temp_dir)

    @pytest.mark.asyncio
    async def test_get_codebase_authentication_error(self, git_explorer):
        """Test obsługi błędu autentykacji"""
        repo_url = "https://gitlab.com/private/repo.git"
        
        with patch('git.Repo.clone_from') as mock_clone:
            mock_clone.side_effect = git.GitCommandError(
                'git clone', 'Authentication failed'
            )
            
            result = await git_explorer.get_codebase(repo_url)
            assert "Authentication error" in result

    # Testy dla estimate_codebase
    @pytest.mark.asyncio
    async def test_estimate_codebase_empty_repo(self, git_explorer):
        """Test estymacji pustego repozytorium"""
        repo_url = "https://github.com/test/empty-repo.git"
        
        with patch('git.Repo.clone_from') as mock_clone:
            temp_dir = tempfile.mkdtemp()
            mock_clone.return_value = None
            
            result = await git_explorer.estimate_codebase(repo_url)
            
            assert "Total files: 0" in result
            assert "Estimated token count" in result
            
            shutil.rmtree(temp_dir)

    @pytest.mark.asyncio
    async def test_estimate_codebase_with_files(self, git_explorer):
        """Test estymacji repozytorium z plikami"""
        repo_url = "https://github.com/test/repo-with-files.git"
        
        with patch('git.Repo.clone_from') as mock_clone:
            # Przygotowanie mocków i struktury plików
            temp_dir = tempfile.mkdtemp()
            (Path(temp_dir) / "src").mkdir()
            (Path(temp_dir) / "src" / "main.py").write_text("print('hello')")
            (Path(temp_dir) / "README.md").write_text("# Test Repo")
            
            mock_clone.return_value = None
            
            result = await git_explorer.estimate_codebase(repo_url)
            
            assert "Total files: 2" in result
            assert "src" in result
            assert "main.py" in result
            assert "README.md" in result
            
            shutil.rmtree(temp_dir)

    # Testy dla check_gitlab_token_status
    def test_check_gitlab_token_status_with_token(self, git_explorer):
        """Test sprawdzania statusu tokena gdy jest skonfigurowany"""
        result = git_explorer.check_gitlab_token_status()
        assert "GitLab token is configured" in result

    def test_check_gitlab_token_status_without_token(self, git_explorer):
        """Test sprawdzania statusu tokena gdy nie jest skonfigurowany"""
        with patch('mcp_git_explorer.core.GitExplorerSettings') as mock_settings:
            mock_settings.return_value.gitlab_token = ""
            explorer = GitExplorer()
            result = explorer.check_gitlab_token_status()
            assert "GitLab token is not configured" in result

    # Testy pomocnicze dla metod prywatnych
    def test_should_ignore_file(self, git_explorer):
        """Test sprawdzania czy plik powinien być ignorowany"""
        root_path = Path("/test/repo")
        test_file = root_path / "node_modules" / "test.js"
        ignore_patterns = ["node_modules/"]
        
        assert git_explorer._should_ignore_file(test_file, root_path, ignore_patterns)

    def test_is_binary_file(self, git_explorer):
        """Test wykrywania plików binarnych"""
        temp_dir = tempfile.mkdtemp()
        
        # Utworzenie pliku tekstowego
        text_file = Path(temp_dir) / "test.txt"
        text_file.write_text("Hello World")
        assert not git_explorer._is_binary_file(text_file)
        
        # Utworzenie pliku binarnego
        binary_file = Path(temp_dir) / "test.bin"
        binary_file.write_bytes(bytes([0, 1, 2, 3]))
        assert git_explorer._is_binary_file(binary_file)
        
        shutil.rmtree(temp_dir)