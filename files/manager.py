import os
from pathlib import Path
from typing import List

from aiocache import cached, Cache
from aiocache.serializers import PickleSerializer
from aiofiles import open

from config import base_settings, cache
from files.models import FileContent, FileInfo, FileIndex


class FileManager:

    async def get_index_by_id(self, file_id: str) -> FileIndex:
        file_index = None
        async with open(Path(base_settings.root_path, 'file_index.txt'), 'r') as f:
            async for line in f:
                if line.startswith(file_id):
                    file_index = FileIndex.from_string(line)
            if not file_index:
                raise FileNotFoundError(f"File with id {file_id} not found")
        return file_index

    async def create_file(self, file: FileContent) -> FileInfo:
        if not file.get_path.exists():
            async with open(file.get_path, 'w') as f:
                await f.write(file.content)
                await cache.delete('file_list')

            async with open(Path(base_settings.root_path, 'file_index.txt'), 'a') as f:
                await f.write(FileIndex(
                    id=file.id,
                    file_name=file.file_name,
                    file_path=file.get_path,
                ).to_string())

        else:
            raise FileExistsError(f"File with name {file.file_name} already exists")
        return await file.get_info()

    @cached(ttl=10, cache=Cache.MEMORY, key="file_list", serializer=PickleSerializer())
    async def get_file_list(self) -> List[FileInfo]:
        result = []
        async with open(Path(base_settings.root_path, 'file_index.txt'), 'r') as f:
            async for line in f:
                file_index = FileIndex.from_string(line)
                f_info = FileInfo.from_path(file_index.file_path, file_index.file_name)
                f_info.id = file_index.id
                result.append(f_info)
        return result

    async def get_file(self, file_id: str) -> FileContent:
        file_index = await self.get_index_by_id(file_id)
        async with open(file_index.file_path, 'r') as f:
            return FileContent(
                id=file_index.id,
                file_name=file_index.file_name,
                content=await f.read(),
            )

    async def get_file_info(self, file_id: str) -> FileInfo:
        file_index: FileIndex = await self.get_index_by_id(file_id)
        return FileInfo.from_path(file_index.file_path, file_index.file_name)

