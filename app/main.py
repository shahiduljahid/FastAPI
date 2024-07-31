from fastapi import FastAPI
from blog import models
from blog.database import engine
from blog.routers import blog, user, authentication, detection
from Functions.download_file_if_needed import download_file_if_needed
import os
import pickle
import global_parameters

app = FastAPI()
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir + "/blog/DL_MODELS/saved_model.pkl")
File_URL = "https://drive.google.com/uc?id=1J9LloeGpK2aYYeNnHeleS8BKg4VpjDQq"


@app.on_event("startup")
async def on_startup():
    # Download the file first
    await download_file_if_needed(file_path, File_URL)

    # Now, load the model
    with open(file_path, "rb") as f:
        loaded = pickle.load(f)
    global_parameters.loaded_model = loaded["model"]
    global_parameters.loaded_predict = loaded["predict"]
    global_parameters.loaded_model.eval()


models.Base.metadata.create_all(bind=engine)

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(detection.router)
