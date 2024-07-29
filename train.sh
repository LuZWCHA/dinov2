path=$(dirname "$0") 
export PYTHONPATH=$path:$PYTHONPATH
echo $path


# One GPU
# dinov2/configs/train/vitg14_cell.yaml
# dinov2/configs/train/vitl16_short_cell.yaml
# dinov2/configs/train/vitg14_cell.yaml
# python dinov2/train/train.py \
#     --config-file dinov2/configs/train/vitg14_cell.yaml \ 
#     --output-dir checkpoints/vitg14_cell

# Multi-GPUs
export CUDA_VISIBLE_DEVICES=0,1
export LOCAL_RANK=0
export LOCAL_WORLD_SIZE=2

torchrun \
     --nproc_per_node 2 \
     dinov2/train/train.py \
     --config-file dinov2/configs/train/vitb_cell.yaml \
     --output-dir checkpoints/vitb_cell
