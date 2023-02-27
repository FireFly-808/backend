import os
import cv2
import torch
import numpy as np
from typing import Tuple
from torchvision import transforms as T


def pad_numpy_img_till_dims_by_32(img):
    """
    > It pads the image with zeros until the height and width are divisible by 32.

    :param img: The image to be padded
    :return: The padded image
    """
    # Get the shape of the image
    w, h = img.shape[:2]
    # Calculate the number of pixels to pad
    pad_h = 32 - h % 32
    pad_w = 32 - w % 32
    # Pad the image
    img = np.pad(img, ((0, pad_w), (0, pad_h), (0, 0)), mode="linear_ramp")
    return img


def get_image_file_paths(base_dir):
    """
    > It takes a base directory and returns a list of all the file paths to images in the base
    directory.

    :param base_dir: The base directory to search for images
    :return: A list of file paths to images
    """
    return [
        os.path.join(base_dir, i)
        for i in os.listdir(base_dir)
        if i.endswith(".png") or i.endswith(".jpg")
    ]


def load_img_from_path(file_path, BGR2RGB=True):
    """
    > It takes a file path to an image and returns the image as a numpy array.

    :param file_path: The file path to the image
    :return: The image as a numpy array
    """
    img = cv2.imread(file_path)
    if BGR2RGB:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


def inference_flame_model(
    model, device, image, mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
):
    """
    It takes an image, transforms it into a tensor, normalizes it, and then passes it through the model

    :param model: the model you want to use
    :param device: the device to run the model on
    :param image: the image you want to predict on
    :param mean: The mean of the image
    :param std: standard deviation of the image
    :return: The model is returning a predicted segmentation mask with the same size as the input image.
    """
    t = T.Compose([T.ToTensor(), T.Normalize(mean, std)])
    image = t(image)
    image = image.to(device)

    with torch.no_grad():
        image = image.unsqueeze(0)
        output = model(image)
        masked = torch.argmax(output, dim=1)
        masked = masked.cpu().squeeze(0)
    return masked


def overlay_mask_on_image(rgb_img, binary_mask):
    # convert the binary mask to an rgb mask
    rgb_mask = np.zeros((binary_mask.shape[0], binary_mask.shape[1], 3))
    rgb_mask[binary_mask == 1] = [255, 0, 0]
    # overlay the rgb mask on the rgb image
    output_visual = cv2.addWeighted(
        rgb_img.astype(np.uint8), 0.7, rgb_mask.astype(np.uint8), 0.3, 0
    )

    return output_visual
