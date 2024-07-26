from fastapi import Depends, APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse
from .. import database
from sqlalchemy.orm import Session
import io
from PIL import Image
from ..DL_MODELS.fruit_detection_model import fruit_detector

# from blog.Models.fruit_detection_model import fruit_detector

get_db = database.get_db

router = APIRouter(tags=["Detection"], prefix="/detect")


@router.post("/fruit", status_code=200)
async def detect_fruit(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # Read the uploaded image
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    # Process the image with your deep learning model
    buf = await fruit_detector(image)
    return StreamingResponse(buf, media_type="image/png")
