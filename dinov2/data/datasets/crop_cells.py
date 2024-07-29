import glob, os
from pathlib import Path
import shutil

import tqdm

# huaxi_views = glob.iglob("/nasdata2/dataset/cytology_data/华西二院细胞学AI/**/*.jpeg", recursive=True)
huaxi_views = glob.iglob("/nasdata2/dataset/retina-views-v3/**/*.jpg", recursive=True)

# output_dir = "/nasdata2/dataset/dino/v2/huaxi_cell_data"
output_dir = "/nasdata2/dataset/dino/v2/cro_all_cell_data"
# print(len(huaxi_views))
import multiprocessing as mp

import imageio

def crop_and_save(crop_image_path_idx):
    # 960 256
    crop_image_path, idx = crop_image_path_idx
    save_path = os.path.join(output_dir, f"{idx:08}.jpg")
    # if os.path.exists(save_path):
    #     return crop_image_path
    try:
        crop_image = imageio.v3.imread(crop_image_path)
        h, w = crop_image.shape[:2]
        h, w = 1024, 1024
        crop_image = crop_image[h // 2 - 128: h // 2 + 128, w // 2 - 128: w // 2 + 128, :]
        name = Path(crop_image_path).name
        imageio.imwrite(save_path, crop_image)
    except:
        pass
    return crop_image_path

def merge_cells(dirs, relink2="/nasdata2/dataset/dino/v2/CellDatasetCropped"):
    shutil.rmtree(relink2)
    os.makedirs(relink2, exist_ok=True)
    
    index = 0
    for d in dirs:
        print(d)
        image_paths = glob.glob(os.path.join(d, "**/*.jp*g"), recursive=True)
        
        print(d, len(image_paths))
        for i in tqdm.tqdm(image_paths):
            class_name = "UNKNOWN"
            if "shishi_wsi_path_sample_fixed" in i:
                class_name = Path(i).parent.name
            if not os.path.exists(os.path.join(relink2, f"{class_name}_{index:09}.jpg")):
                os.symlink(i, os.path.join(relink2, f"{class_name}_{index:09}.jpg"))

            index += 1


if __name__ == "__main__":
    # pool = mp.Pool(48)

    # res =  pool.imap_unordered(crop_and_save, zip(huaxi_views, range(10000000)))

    # for i in tqdm.tqdm(res):
    #     # print(i)
    #     pass
    
    merge_cells([
        "/nasdata2/dataset/dino/v2/shishi_wsi_path_sample_fixed/images",
        "/nasdata2/dataset/dino/v2/cro_all_cell_data",
        "/nasdata2/dataset/dino/v2/huaxi_cell_data",
    ])