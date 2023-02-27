import pyrovision.models as models
from torchvision import transforms
import torch
from PIL import Image
import os


def test_images(model, file_paths, tf):
    """
    > It takes a model, a list of image file paths, and a transform function, and returns a list of
    tuples containing the image file path, the predicted label, and the confidence of the prediction.

    :param model: The model to use for prediction
    :param file_paths: a list of file paths to images
    :param tf: The transform function to apply to the image
    :return: A list of tuples. Each tuple contains the image file name, the predicted label, and the
    confidence.
    """
    print(f"model: {model.__class__.__name__}")
    results = []
    for img_file in file_paths:
        img = Image.open(img_file).convert("RGB")
        # Transform
        tf_img = tf(img)
        # Predict
        with torch.no_grad():
            pred = model(tf_img.unsqueeze(0))
            is_wildfire = torch.sigmoid(pred).item() >= 0.5
        # Append results as tuple to list
        results.append((img_file, is_wildfire, torch.sigmoid(pred).item()))
        print(f"Image: {img_file}")
        print(f"Wildfire: {is_wildfire}")
        print(f"Confidence: {torch.sigmoid(pred).item()}\n")
    return results


if __name__ == "__main__":
    # Init
    normalize = transforms.Normalize(
        mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
    )

    tf = transforms.Compose(
        [
            transforms.Resize(size=(448)),
            transforms.CenterCrop(size=448),
            transforms.ToTensor(),
            normalize,
        ]
    )

    # List test image file paths
    base_dir = "test_imgs/"
    file_paths = [
        os.path.join(base_dir, i) for i in os.listdir(base_dir) if i.endswith(".png")
    ]
    # Load models to test
    model = models.resnet34(pretrained=True).eval()

    results = test_images(model, file_paths, tf)

    # print(results)
