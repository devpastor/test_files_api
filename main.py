import uvicorn as uvicorn
from fastapi import FastAPI
from config import base_settings
from files import router as files_router

app = FastAPI(
    debug=base_settings.debug,
    title="TEST FILE API",
    docs_url='/doc',
    reload=base_settings.debug,
)
app.include_router(files_router)


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)