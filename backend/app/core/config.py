"""Application configuration – reads from environment variables."""
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="TRADINGLAB_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Server
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = False

    # Data directory – defaults to ~/.tradinglab/data
    data_dir: Path = Path.home() / ".tradinglab" / "data"

    @property
    def db_path(self) -> Path:
        return self.data_dir / "db" / "tradinglab.db"

    @property
    def db_url(self) -> str:
        return f"sqlite:///{self.db_path}"

    @property
    def market_data_dir(self) -> Path:
        return self.data_dir / "market_data"

    def ensure_dirs(self) -> None:
        """Create all required directories on first start."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.market_data_dir.mkdir(parents=True, exist_ok=True)


settings = Settings()
