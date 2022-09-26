from typing import List

import ujson
from fastapi import APIRouter, Body, HTTPException

from fastapi_restful.cbv import cbv
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse

from files.manager import FileManager
from files.models import FileInfo, FileContent

router = APIRouter(prefix='/files', tags=['Files'])


@cbv(router)
class FileRouter:
    _manager = FileManager()

    @router.head('/files/{file_id}')
    async def get_file_info(self, file_id):
        data = await self._manager.get_file_info(file_id)
        data = {k: str(v) for k, v in data.dict().items()}
        return HTMLResponse(headers=data, media_type='application/json')

    @router.get('/files/{file_id}')
    async def get_file(self, file_id: str) -> FileResponse:
        _index = await self._manager.get_index_by_id(file_id)
        return FileResponse(
            path=_index.file_path,
            filename=_index.file_name,
            media_type="application/octet-stream",

        )


    @router.get('/files', response_model=List[FileInfo])
    async def get_file_list(self) -> List[FileInfo]:
        return await self._manager.get_file_list()

    @router.post('/files')
    async def create_file(self, file: FileContent = Body(
        example={
            "file_name": "test.txt",
            "content": "test"
        }
    )):
        try:
            return await self._manager.create_file(file)
        except FileExistsError as e:
            raise HTTPException(status_code=400, detail=str(e))
