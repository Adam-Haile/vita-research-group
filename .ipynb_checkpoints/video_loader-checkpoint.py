import os
import cv2
import torch
from torch.utils.data import Dataset
from torchvision.transforms.functional import to_pil_image

class VideoDataset(Dataset):
    def __init__(self, video_dir, transform=None):
        self.video_dir = video_dir
        self.video_files = [os.path.join(video_dir, f) for f in os.listdir(video_dir) if f.endswith(('.mp4', '.avi'))]
        self.transform = transform

    def __len__(self):
        return len(self.video_files)

    def __getitem__(self, idx, n_fr=300):
        video_path = self.video_files[idx]
        # Load video
        cap = cv2.VideoCapture(video_path)
        frames = []
        i = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            # Convert BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert RGB to Grayscale
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            # Convert numpy array to PIL Image
            frame = to_pil_image(frame)
            if self.transform:
                frame = self.transform(frame)
            # Ensure the frame is a 2D tensor after transformation
            # Note: Adjust this part according to your transform's output
            frame = torch.squeeze(frame)  # This ensures the frame is 2D if your transform outputs a 3D tensor with 1 channel
            frames.append(frame)
            i += 1
            if i == n_fr:
                break

        # Stack frames to create a 'depth' dimension
        frames = torch.stack(frames)  # Now should be [300, H, W]

        # Add a batch dimension
        frames = frames.unsqueeze(0)  # Now should be [1, 300, H, W]

        return frames

