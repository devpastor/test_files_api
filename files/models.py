import os
from pathlib import Path
from typing import Optional, List
from config import base_settings

from pydantic import BaseModel, Field


class FileIndex(BaseModel):
    id: str = Field(...)
    file_name: str = Field(..., alias="file_name")
    file_path: Path = Field(..., alias="file_path")

    def to_string(self):
        return f"{self.id} {self.file_name} {self.file_path}\n"

    @staticmethod
    def from_string(string: str) -> "FileIndex":
        _id, file_name, file_path = string.split(" ")
        return FileIndex(id=_id, file_name=file_name, file_path=file_path[:-1])


class BaseFile(BaseModel):
    id: str = Field(default_factory=lambda: str(os.urandom(16).hex()))
    file_name: str = Field(..., example="Звіт.txt")

    @property
    def get_path(self):
        path = Path(f"{base_settings.root_path}/{base_settings.file_dir}", self.file_name)
        return path


class FileInfo(BaseFile):
    st_mode: int = Field(..., description="The file type and permissions")
    st_ino: int = Field(..., description="The inode number")
    st_dev: int = Field(..., description="The device id")
    st_uid: int = Field(..., description="The user id of the file owner")
    st_gid: int = Field(..., description="The group id of the file owner")
    st_size: int = Field(..., description="The size of the file, in bytes")
    st_nlink: Optional[int] = Field(..., description="The number of hard links")

    @staticmethod
    def from_path(path: Path, file_name: str) -> "FileInfo":
        stat = os.stat(path)
        print(stat)
        return FileInfo(
            file_id=id(path),
            file_name=file_name,
            st_mode=stat.st_mode,
            st_ino=stat.st_ino,
            st_dev=stat.st_dev,
            st_uid=stat.st_uid,
            st_gid=stat.st_gid,
            st_size=stat.st_size,
            st_nlink=stat.st_nlink,
        )


class FileContent(BaseFile):
    content: str = Field(..., example="test content")

    async def get_info(self) -> FileInfo:
        stat = os.stat(self.get_path)
        return FileInfo(
            id=self.id,
            file_name=self.file_name,
            st_mode=stat.st_mode,
            st_ino=stat.st_ino,
            st_dev=stat.st_dev,
            st_uid=stat.st_uid,
            st_gid=stat.st_gid,
            st_size=stat.st_size,
            st_nlink=stat.st_nlink,
        )


class FileList(BaseModel):
    files: List[FileInfo] = Field(..., description="List of files")
