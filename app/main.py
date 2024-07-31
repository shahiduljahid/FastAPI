from fastapi import FastAPI
from blog import models
from blog.database import engine
from blog.routers import blog, user, authentication, detection
from Functions.download_file_if_needed import download_file_if_needed
import os


app = FastAPI()
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir + "/blog/DL_MODELS/saved_model.pkl")
File_URL = "https://drive.google.com/uc?id=1J9LloeGpK2aYYeNnHeleS8BKg4VpjDQq"


@app.on_event("startup")
async def on_startup():
    # Download the file first
    await download_file_if_needed(file_path, File_URL)


models.Base.metadata.create_all(bind=engine)

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(detection.router)
