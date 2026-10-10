from fastapi import FastAPI

from app.routers.convert import router as convert_router

app = FastAPI(title="Currency converter")
app.include_router(convert_router)
