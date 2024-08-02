from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers import User, X, FB, Analysis

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


app.include_router(User.router)
app.include_router(X.router)
app.include_router(FB.router)
app.include_router(Analysis.router)

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
# https://x.com/elonmusk/status/1818083969721659861