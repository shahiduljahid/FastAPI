import numpy as np
import torch
from torchvision import models, transforms
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.ops import nms
from PIL import Image, ImageDraw, ImageFont
import io
import os

device = "cpu"

# Define labels
labels = ["background", "orange", "apple", "banana"]
label2targets = {l: t for t, l in enumerate(labels)}
targets2label = {t: q for q, t in label2targets.items()}
num_classes = len(targets2label)


# Load checkpoint
def load_checkpoint(checkpoint, model, optimizer):
    print("=> Loading checkpoint")
    model.load_state_dict(checkpoint["state_dict"])
    optimizer.load_state_dict(checkpoint["optimizer"])


# Get model
def get_model():
    model = models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    return model


model = get_model().to(device)
optimizer = torch.optim.SGD(
    model.parameters(), lr=0.005, weight_decay=5e-4, momentum=0.9
)
# Get the current script's directory
script_dir = os.path.dirname(__file__)
checkpoint_path = os.path.join(script_dir + "\\checkpoints\\our_fast_r_cnn_model.pth")
if os.path.exists(checkpoint_path):
    
    load_checkpoint(
        torch.load(checkpoint_path),
        model,
        optimizer,
    )


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


async def fruit_detector(image):
    transform = transforms.Compose([transforms.ToTensor()])
    image_tensor = transform(image).to(device)
    model.eval()
    # Make a prediction
    with torch.no_grad():
        output = model([image_tensor])[0]
    # Decode the output
    bbs, confs, labels = decode_output(output)

    # Convert the PIL image to a format where you can draw on it
    draw_image = image.copy()
    draw = ImageDraw.Draw(draw_image)

    # Draw bounding boxes
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

    draw_annotations(draw, bbs, confs, labels)
    # Save the image to a bytes buffer
    buffer = io.BytesIO()
    draw_image.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer
