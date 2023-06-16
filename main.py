from fastapi import FastAPI
from api import router
from database import Base, engine, database

app = FastAPI()

app.include_router(router)


@app.on_event("startup")
async def startup():
    import models
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
