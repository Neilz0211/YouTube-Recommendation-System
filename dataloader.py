import pandas as pd
from torch.utils.data import Dataset

class VideoDataset(Dataset):
    def __init__(self, file_path):
        self.data = pd.read_json(file_path)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data.iloc[idx]