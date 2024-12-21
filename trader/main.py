import uvicorn
from fastapi import FastAPI

from middleware import DelayMiddleware
from routes import router
from web_socket import ws_router

app = FastAPI()

app.add_middleware(DelayMiddleware)

app.include_router(router)
app.include_router(ws_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
