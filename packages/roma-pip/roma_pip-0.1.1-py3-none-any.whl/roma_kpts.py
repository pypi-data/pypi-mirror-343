from PIL import Image
import torch
import cv2
from romatch import roma_outdoor

class ROMAMatcher:
    def __init__(self, device, roma_path, dinov2_path):
        self.device = device
        weights = torch.load(roma_path, map_location=device, weights_only=True)
        dinov2_weights = torch.load(dinov2_path, map_location=device, weights_only=True)
        self.roma_model = roma_outdoor(device=device, weights=weights, dinov2_weights=dinov2_weights)
    
    def roma_match(self, im1_path, im2_path):
        if type(im1_path) == str:
            W_A, H_A = Image.open(im1_path).size
            W_B, H_B = Image.open(im2_path).size
        else:
            W_A, H_A = cv2.imread(im1_path).shape[1], cv2.imread(im1_path).shape[0]
            W_B, H_B = cv2.imread(im2_path).shape[1], cv2.imread(im2_path).shape[0]
        warp, certainty = self.roma_model.match(im1_path, im2_path, device=device)
        matches, certainty = self.roma_model.sample(warp, certainty)
        kpts1, kpts2 = self.roma_model.to_pixel_coordinates(matches, H_A, W_A, H_B, W_B)
        return kpts1, kpts2


# def roma_match(im1_path, im2_path):
#     device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#     if torch.backends.mps.is_available():
#         device = torch.device('mps')
#     roma_model = roma_outdoor(device=device)
#     W_A, H_A = Image.open(im1_path).size
#     W_B, H_B = Image.open(im2_path).size
#     warp, certainty = roma_model.match(im1_path, im2_path, device=device)
#     matches, certainty = roma_model.sample(warp, certainty)
#     kpts1, kpts2 = roma_model.to_pixel_coordinates(matches, H_A, W_A, H_B, W_B)
#     return kpts1, kpts2



if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--im_A_path", default="../Roma/assets/360_2D_模板.jpg", type=str)
    parser.add_argument("--im_B_path", default="../Roma/assets/360_2D_待检.jpg", type=str)

    args, _ = parser.parse_known_args()
    im1_path = args.im_A_path
    im2_path = args.im_B_path

    # Create model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    if torch.backends.mps.is_available():
        device = torch.device('mps')
    roma_model = ROMAMatcher(device=device, roma_path="../Roma/weights/roma_outdoor.pth", dinov2_path="../Roma/weights/dinov2_vitl14_pretrain.pth")
    kpts1, kpts2 = roma_model.roma_match(im1_path, im2_path)
    pass


    # warp, certainty = roma_model.match(im1_path, im2_path, device=)
    # # Sample matches for estimation
    # matches, certainty = roma_model.sample(warp, certainty)
    # kpts1, kpts2 = roma_model.to_pixel_coordinates(matches, H_A, W_A, H_B, W_B)

    # F, mask = cv2.findFundamentalMat(
    #     kpts1.cpu().numpy(), kpts2.cpu().numpy(), ransacReprojThreshold=0.2, method=cv2.USAC_MAGSAC, confidence=0.999999, maxIters=10000
    # )