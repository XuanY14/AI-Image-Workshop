import os
import torch 
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

MODEL_DIR = PROJECT_ROOT / "models_data"
os.makedirs(MODEL_DIR, exist_ok=True)

TEMP_DIR = PROJECT_ROOT / "temp_files"
os.makedirs(TEMP_DIR, exist_ok=True)

MODELS_CONFIG = {
    "style_transfer": {
        "model_id": "stable_diffusion", 
        "local_path": MODEL_DIR / "stable_diffusion"
    },
    "denoising": {
        "model_id": "stable_diffusion", 
        "local_path": MODEL_DIR / "stable_diffusion"
    },
    "inpainting": {
        "model_id": "stable-diffusion-2-inpainting", 
        "local_path": MODEL_DIR / "stable-diffusion-2-inpainting"
    },
    "generation": {
        "model_id": "stable_diffusion", 
        "local_path": MODEL_DIR / "stable_diffusion"
    },
    "background_removal": {
        "model_id": "background_removal", 
        "local_path": MODEL_DIR / "bg_removal_model"
    }
}

# 设备配置
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# 图像处理参数
IMAGE_SIZE_LIMIT = 10 * 1024 * 1024  # 10MB
MAX_IMAGE_DIMENSION = 1024  # 最大边长

print(f"当前设备: {DEVICE}")
print(f"PyTorch版本: {torch.__version__}")
if torch.cuda.is_available():
    print(f"CUDA版本: {torch.version.cuda}")
    print(f"GPU数量: {torch.cuda.device_count()}")
    print(f"当前GPU: {torch.cuda.get_device_name(0) if torch.cuda.device_count() > 0 else 'N/A'}")

# 验证模型路径是否存在
for model_name, config in MODELS_CONFIG.items():
    if model_name != "background_removal":  
        path = config["local_path"]
        exists = os.path.exists(path)
        print(f"模型 {model_name}: {'✓ 存在' if exists else '✗ 不存在'} -> {path}")