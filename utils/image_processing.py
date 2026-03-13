import cv2
import numpy as np
from PIL import Image
import io

def resize_image(image, max_size=1024):
    """调整图像大小以适应处理限制"""
    width, height = image.size
    
    # 首先按比例调整到最大尺寸限制
    if max(width, height) > max_size:
        if width > height:
            new_width = max_size
            new_height = int(height * max_size / width)
        else:
            new_height = max_size
            new_width = int(width * max_size / height)
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        width, height = new_width, new_height
    
    # 【修改】不再强制8的倍数，由模型自行处理
    return image

def preprocess_image(image):
    """预处理图像"""
    if image.mode != 'RGB':
        image = image.convert('RGB')
    return image

def postprocess_image(image):
    """后处理图像"""
    if image.mode != 'RGB':
        image = image.convert('RGB')
    return image

def add_noise(image, noise_factor=0.1):
    """给图像添加噪声（用于测试去噪功能）"""
    image_array = np.array(image)
    noise = np.random.normal(0, noise_factor * 255, image_array.shape)
    noisy_image = np.clip(image_array + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_image)

def create_damage_mask(image, damage_ratio=0.2):
    """创建损坏区域掩码（用于测试修复功能）"""
    width, height = image.size
    mask = np.ones((height, width), dtype=np.uint8) * 255
    
    num_rectangles = np.random.randint(2, 5)
    for _ in range(num_rectangles):
        rect_width = int(width * damage_ratio)
        rect_height = int(height * damage_ratio)
        x = np.random.randint(0, width - rect_width)
        y = np.random.randint(0, height - rect_height)
        mask[y:y+rect_height, x:x+rect_width] = 0
    
    return Image.fromarray(mask, mode='L')

def remove_background_simple(image):
    """简单的背景移除方法（基于颜色差异）"""
    img_array = np.array(image)
    
    mask = np.zeros(img_array.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    
    h, w = img_array.shape[:2]
    rect = (int(0.1*w), int(0.1*h), int(0.8*w), int(0.8*h))
    
    cv2.grabCut(img_array, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    result = img_array * mask2[:, :, np.newaxis]
    alpha = mask2 * 255
    result_with_alpha = np.dstack([result, alpha])
    
    return Image.fromarray(result_with_alpha, mode='RGBA')

def validate_image(image):
    """验证图像格式和大小"""
    if image is None:
        raise ValueError("图像不能为空")
    
    if image.mode not in ['RGB', 'RGBA', 'L']:
        image = image.convert('RGB')
    
    # 【修改】降低尺寸限制，更安全
    width, height = image.size
    if width > 1536 or height > 1536:  # 从2048降到1536
        raise ValueError(f"图像尺寸过大: {width}x{height}，最大支持1536x1536")
    
    return image

def convert_to_rgba(image):
    """将图像转换为RGBA格式"""
    if image.mode == 'RGBA':
        return image
    elif image.mode == 'P':
        image = image.convert('RGBA')
    elif image.mode == 'L':
        image = image.convert('RGBA')
    else:
        image = image.convert('RGBA')
    return image

def blend_images(base_image, overlay_image, alpha=0.5):
    """混合两张图像"""
    base_array = np.array(base_image)
    overlay_array = np.array(overlay_image)
    
    if base_array.shape != overlay_array.shape:
        overlay_image = overlay_image.resize(base_image.size)
        overlay_array = np.array(overlay_image)
    
    blended = (alpha * base_array + (1 - alpha) * overlay_array).astype(np.uint8)
    return Image.fromarray(blended)

def resize_for_inpainting(image, max_size=1024):  # 【关键修改】提高限制
    """调整图像大小以适应修复模型，保持原始比例"""
    original_size = image.size
    width, height = image.size
    
    # 首先按比例调整到最大尺寸限制
    if max(width, height) > max_size:
        if width > height:
            new_width = max_size
            new_height = int(height * max_size / width)
        else:
            new_height = max_size
            new_width = int(width * max_size / height)
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        width, height = new_width, new_height
    
    # 【重要】不再强制8的倍数，保持原始宽高比
    size_info = {
        'original_size': original_size,
        'was_resized': (original_size != (width, height)),
        'target_size': (width, height)
    }
    return image, size_info

def restore_original_size(image, original_info):
    """根据原始信息恢复图像到原始尺寸"""
    if original_info and 'original_size' in original_info:
        original_size = original_info['original_size']
        if image.size != original_size:
            image = image.resize(original_size, Image.Resampling.LANCZOS)
    return image