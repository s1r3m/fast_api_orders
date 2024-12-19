import uvicorn
from fastapi import FastAPI
from middleware import DelayMiddleware, ValidationErrorMiddleware
from routes import router

app = FastAPI()

# Add custom middleware
app.add_middleware(ValidationErrorMiddleware)  # type: ignore
app.add_middleware(DelayMiddleware)  # type: ignore

# Register the router
app.include_router(router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
