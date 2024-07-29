import glob, os
from pathlib import Path

import pandas
import tqdm


def create():
    pass

def copy2dino_dataset(image_list, target_dir):
    image_id = 0
    image_ori_path = {
        "image_id": [],
        "image_raw_path": [],
    }

    for i in tqdm.tqdm(image_list):
        save_link = os.path.join(target_dir, f"{image_id}{Path(i).suffix}")
        # os.symlink(i, save_link)
        image_ori_path["image_id"].append(image_id)
        image_ori_path["image_raw_path"].append(i)
        image_id += 1
        
    pandas.DataFrame(image_ori_path).to_csv(os.path.join(target_dir, "raw_meta_data.csv"))
    
    

WSI_DATA01 = "/nasdata2/dataset/cytology_data/华西二院细胞学AI" #81w
WSI_DATA02 = "/nasdata2/dataset/moshi_patch_data" # 1.7w
WSI_DATA03 = "/nasdata2/dataset/wsi_patch_data" # 13.45w

SHISHI_DATA = "/nasdata2/dataset/shishi_data" # 47w

composite_data = "/nasdata2/dataset/composite_goe_data/images" # 50w

QC_DATA01 = "/nasdata2/dataset/qc/bg/mosaic_4_ps_62_10x/" # 0.78w
QC_DATA02 = "/nasdata2/dataset/qc/hkust_online_anno_001/" # 0.41w

PUBLIC_CELL_DATASET01 = "/nasdata2/dataset/sipakmed/images" # 0.1w
PUBLIC_CELL_DATASET02 = "/nasdata2/dataset/ccedd/images" # 0.07w
PUBLIC_CELL_DATASET03 = "/nasdata2/dataset/isbi2014/images" # 0.1w
PUBLIC_CELL_DATASET04 = "/nasdata2/dataset/dino/v2/base_data" # 0.1w
PUBLIC_CELL_DATASET05 = "/nasdata2/dataset/dino/v2/cytology_dataset/cytology_dataset-master/dataset/" # 0.1w
PUBLIC_CELL_DATASET06 = "/nasdata2/dataset/dino/v2/CDetector2021" # 0.76w
PUBLIC_CELL_DATASET07 = "/nasdata2/dataset/dino/v2/CDetector2021" # 0.76w

jpg_image_roots = [
    WSI_DATA01,
    WSI_DATA02,
    WSI_DATA03,
    SHISHI_DATA,
    composite_data,
    QC_DATA01,
    QC_DATA02,
    PUBLIC_CELL_DATASET01,
    PUBLIC_CELL_DATASET02,
    PUBLIC_CELL_DATASET03,
    PUBLIC_CELL_DATASET04,
    PUBLIC_CELL_DATASET05,
    PUBLIC_CELL_DATASET06,
]

meta_info = [
    {"info": "华西医院细胞学WSI裁剪的沉降式疑似阳性数据"},
    {"info": "浙江人民，河南某院细胞学WSI裁剪的膜式数据"},
    {"info": "多中心细胞学WSI裁剪的阳性和阴性难例沉降式数据"},
    {"info": "多中心细胞学实视设备采集的高质量沉降式数据"},
    {"info": "通过多边形合成的细胞重叠的合成数据集"},
    {"info": "包含各种背景（炎性，血性，萎缩）的细胞学阴性沉降式数据"},
    {"info": "包含各种背景（炎性，血性，萎缩）的细胞学阴性沉降式数据以及模糊气泡数据"},
    {"info": "公开数据集sipakmed"},
    {"info": "公开数据集ccedd"},
    {"info": "公开数据集isbi2014"},
    {"info": "公开数据集FNAC2019"},
    {"info": "公开数据集Cervix93"},
    {"info": "公开数据集CDetector2021"},
]

all_image_path = []
datasets = {
    "dataset_path": [],
    "dataset_info": []
}

# for img_root, info in zip(jpg_image_roots, meta_info):
#     if img_root in [PUBLIC_CELL_DATASET05]:
#         images = glob.iglob(str(Path(img_root)/"**"/"*.png"), recursive=True)
#     elif img_root in [PUBLIC_CELL_DATASET06]:
#         images = glob.iglob(str(Path(img_root)/"**"/"*.bmp"), recursive=True)
#     else:
#         images = glob.iglob(str(Path(img_root)/"**"/"*.jp*g"), recursive=True)
#     cnt = 0
#     datasets["dataset_path"].append(img_root)
#     datasets["dataset_info"].append(info["info"])
#     print(info["info"])
#     for i in tqdm.tqdm(images):
#         cnt += 1
#         all_image_path.append(i)
    
# print(len(all_image_path))
# with open("cell_dataset.txt", "w") as f:
#     for i in all_image_path:
#         f.write(i)
#         f.write("\n")

all_image_path = []
with open("cell_dataset.txt", "r") as f:
    for i in f.readlines():
        all_image_path.append(i.strip())
    
    # for i in all_image_path:
    #     f.write(i)
    #     f.write("\n")

copy2dino_dataset(all_image_path, "/nasdata2/dataset/dino/v2/CellDataset/all/images")