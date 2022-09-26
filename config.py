import os
from pathlib import Path

from aiocache import Cache
from aiocache.serializers import PickleSerializer
from pydantic import BaseSettings, Field


def get_project_root() -> Path:
    return Path(__file__).parent


class Settings(BaseSettings):
    class Config:
        env_file = '.env'

    root_path: Path = Field(default_factory=get_project_root, env='ROOT_DIR')
    file_dir: str = Field(..., env="TEST_FILE_DIR")
    debug: bool = Field(..., env="DEBUG")

    def make_file_dir(self):
        if not self.root_path.joinpath(self.file_dir).exists():
            self.root_path.joinpath(self.file_dir).mkdir(parents=True)


base_settings = Settings()
base_settings.make_file_dir()
cache = Cache(Cache.MEMORY, serializer=PickleSerializer())
