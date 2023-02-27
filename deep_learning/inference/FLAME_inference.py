import torch
import matplotlib.pyplot as plt

from utils import (
    get_image_file_paths,
    load_img_from_path,
    pad_numpy_img_till_dims_by_32,
    inference_flame_model,
    overlay_mask_on_image,
)

if __name__ == "__main__":
    # Get the file paths to the test images
    file_paths = get_image_file_paths("../datasets/random_test_imgs")
    file_path = file_paths[0]

    # Load the model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_file = "../weights/FLAME-Unet-Mobilenet-AdamW-class2-epoch15-batch3.pt"
    model = torch.load(model_file)
    model.eval()
    model.to(device)

    # Inference and visualize a single image from the above list of file paths
    og_img = load_img_from_path(file_path)
    img = pad_numpy_img_till_dims_by_32(og_img)

    pred_mask = inference_flame_model(model, device, img)
    pred_mask = pred_mask.numpy()

    # crop the mask to the original image size
    pred_mask = pred_mask[0 : og_img.shape[0], 0 : og_img.shape[1]]

    output_visual = overlay_mask_on_image(og_img, pred_mask)

    plt.imshow(output_visual)
    # plt.imshow(og_img)
    # plt.imshow(pred_mask, alpha=0.5, cmap="gray")
    plt.title(file_path.split("/")[-1])
    plt.axis("off")
    plt.show()
