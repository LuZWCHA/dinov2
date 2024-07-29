# from fastai.vision.all import Path, get_image_files, verify_images

import glob
import os
from typing import Any, Optional, Callable, Tuple
from pathlib import Path
from PIL import Image
import tqdm

from dinov2.data.datasets.extended import ExtendedVisionDataset
from torchvision import transforms


def check_image(im_path):
    try:
        im = Image.open(im_path)
        del im
    except:
        return im_path
    return None

def verify_images(images):
    import multiprocessing as mp
    pool = mp.Pool(max(os.cpu_count() - 1, 1))
    res = pool.imap_unordered(check_image, images)
    failed_imgs = []
    for im_path in tqdm.tqdm(res, total=len(images)):
        if im_path:
            failed_imgs.append(im_path)
    return failed_imgs

class RecursiveImageDataset(ExtendedVisionDataset):
    def __init__(self,
                root: str,
                transforms: Optional[Callable] = None,
                transform: Optional[Callable] = None,
                target_transform: Optional[Callable] = None) -> None:

        super().__init__(root, transforms, transform, target_transform)

        self.root = Path(root)
        image_paths = glob.glob(str(self.root/"**"/"*.jp*g"), recursive=True)
        invalid_images = set()
        # if verify_images:
        print("Verifying images. This ran at ~100 images/sec/cpu for me. Probably depends heavily on disk perf.")
        invalid_images = set(verify_images(image_paths))
        print("Skipping invalid images:", invalid_images)
        self.image_paths = [p for p in image_paths if p not in invalid_images]


    def get_image_data(self, index: int) -> bytes:  # should return an image as an array

        image_path = self.image_paths[index]
        img = Image.open(image_path).convert(mode="RGB").resize((256, 256))

        return img

    def get_target(self, index: int) -> Any:
        image_path = self.image_paths[index]
        class_names = [
            "NILM",
            "ASCUS",
            "LSIL",
            "ASCH",
            "HSIL",
            "TRI",
            "AGC",
            "ACTINO",
            "FUNGI",
            "EC",
            "CC",
            "HSV",
        ]
        class_name = Path(image_path).stem.split("_")
        
        if class_name[0] == "UNKNOWN" or class_name[0] not in class_names:
            return 0
        return class_names.index(class_name[0]) + 1

    def __getitem__(self, index: int) -> Tuple[Any, Any]:
        try:
            image = self.get_image_data(index)
        except Exception as e:
            raise RuntimeError(f"can not read image for sample {index}") from e
        target = self.get_target(index)

        if self.transforms is not None:
            image, target = self.transforms(image, target)

        return image, target

    def __len__(self):
        """Returns the total number of samples."""
        return len(self.image_paths)