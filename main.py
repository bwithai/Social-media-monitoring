from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers.User import user_router
from routers.X import x_router
from routers.FB import fb_router

# api
app = FastAPI(
    title='Social Media Monitoring Service',
    version='1'
)

# cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/')
def wellcome():
    return {
        "message": "Wellcome to Social Media Monitoring Service"
    }


# X (Twitter)
app.include_router(x_router)
app.include_router(fb_router)
app.include_router(user_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",  # Assuming your FastAPI app instance is named `app` in main.py
        host="192.168.1.114",
        port=8000,
        ssl_keyfile='./server.key',
        ssl_certfile='./server.crt',
        log_level="info",
        reload=True  # Add this line to enable auto-reloading
    )