from pydantic_settings import BaseSettings, SettingsConfigDict

class GitExplorerSettings(BaseSettings):
    """Settings for the Git Explorer tool."""
    
    model_config = SettingsConfigDict(
        env_prefix="GIT_EXPLORER_",
        env_file=".env",
        extra="ignore"
    )
    
    gitlab_token: str = ""
