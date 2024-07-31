import numpy as np
import torch
from torchvision import transforms
from torchvision.ops import nms
from PIL import Image, ImageDraw, ImageFont
import io
import pickle
import os

device = "cpu"

# Define labels
labels = ["background", "orange", "apple", "banana"]
label2targets = {l: t for t, l in enumerate(labels)}
targets2label = {t: q for q, t in label2targets.items()}
num_classes = len(targets2label)

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "saved_model.pkl")


# Decode model output
def decode_output(output):
    bbs = output["boxes"].cpu().detach().numpy().astype(np.uint16)
    labels = np.array(
        [targets2label[i] for i in output["labels"].cpu().detach().numpy()]
    )
    confs = output["scores"].cpu().detach().numpy()
    idxs = nms(torch.tensor(bbs.astype(np.float32)), torch.tensor(confs), 0.05)
    bbs, confs, labels = [tensor[idxs] for tensor in [bbs, confs, labels]]
    if len(idxs) == 1:
        bbs, confs, labels = [np.array([tensor]) for tensor in [bbs, confs, labels]]
    return bbs.tolist(), confs.tolist(), labels.tolist()


# Preprocess the image
def preprocess_img(img_path):
    image = Image.open(img_path).convert("RGB")
    transform = transforms.Compose([transforms.ToTensor()])
    return transform(image).to(device)


def draw_annotations(draw, bbs, confs, labels):
    for bbox, conf, label in zip(bbs, confs, labels):
        x1, y1, x2, y2 = bbox

        # Draw the rectangle
        draw.rectangle([x1, y1, x2, y2], outline="red", width=3)

        # Draw the text with a green color and a gap from the rectangle
        text = f"{label} {conf:.2f}"
        text_x = x1 + 5  # Adjust horizontal gap from the left of the rectangle
        text_y = y1 - 15  # Adjust vertical gap from the top of the rectangle

        # Optional: Load a font for better text appearance
        try:
            font = ImageFont.truetype("arial.ttf", size=15)  # Use a TrueType font
        except IOError:
            font = ImageFont.load_default()  # Fallback to default font

        draw.text((text_x, text_y), text, fill="green", font=font)


def predict(image, model, device="cpu"):
    transform = transforms.Compose([transforms.ToTensor()])
    image_tensor = transform(image).to(device)
    model.eval()
    with torch.no_grad():
        output = model([image_tensor])[0]
    bbs, confs, labels = decode_output(output)
    draw_image = image.copy()
    draw = ImageDraw.Draw(draw_image)
    draw_annotations(draw, bbs, confs, labels)
    buffer = io.BytesIO()
    draw_image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


async def fruit_detector(image):
    with open(file_path, "rb") as f:
        loaded = pickle.load(f)
    loaded_model = loaded["model"]
    loaded_model.eval()
    loaded_predict = loaded["predict"]

    buffer = loaded_predict(image, loaded_model, device="cpu")

    return buffer
