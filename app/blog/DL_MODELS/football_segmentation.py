import numpy as np
import torch
from torchvision import transforms
from torchvision.ops import nms
from PIL import Image, ImageDraw, ImageFont
import io
import os
from matplotlib import pyplot as plt
import random
from torchvision import transforms as tfs
import pickle
import torchvision.transforms.functional as F


script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "saved_DeepV3_model.pkl")


def football_segmentation(image):
    fig, ax = plt.subplots(5, 2, figsize=(10, 30))
    return 0
