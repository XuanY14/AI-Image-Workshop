import os
from pathlib import Path
from modelscope.hub.snapshot_download import snapshot_download
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_style_transfer_model():
    """下载风格迁移模型"""
    try:
        from modelscope.pipelines import pipeline
        from modelscope.utils.constant import Tasks
        
        # 尝试创建管道来下载模型
        pipeline = pipeline(
            Tasks.image_style_transfer,
            model='damo/cv_unet_image-style-transfer',
            model_revision='v1.0.1'
        )
        logger.info("风格迁移模型下载完成")
        return True
    except Exception as e:
        logger.error(f"风格迁移模型下载失败: {e}")
        return False

def download_denoising_model():
    """下载去噪模型"""
    try:
        from modelscope.pipelines import pipeline
        from modelscope.utils.constant import Tasks
        
        pipeline = pipeline(
            Tasks.image_denoising,
            model='damo/cv_gan_image-denoising',
            model_revision='v1.0.1'
        )
        logger.info("去噪模型下载完成")
        return True
    except Exception as e:
        logger.error(f"去噪模型下载失败: {e}")
        return False

def download_inpainting_model():
    """下载图像修复模型"""
    try:
        from modelscope.pipelines import pipeline
        from modelscope.utils.constant import Tasks
        
        pipeline = pipeline(
            Tasks.image_inpainting,
            model='damo/cv_fcn_image-inpainting',
            model_revision='v1.0.1'
        )
        logger.info("图像修复模型下载完成")
        return True
    except Exception as e:
        logger.error(f"图像修复模型下载失败: {e}")
        return False

def download_generation_model():
    """下载图像生成模型"""
    try:
        from modelscope.pipelines import pipeline
        from modelscope.utils.constant import Tasks
        
        pipeline = pipeline(
            Tasks.text_to_image_synthesis,
            model='damo/text-to-image-synthesis',
            model_revision='v1.0.1'
        )
        logger.info("图像生成模型下载完成")
        return True
    except Exception as e:
        logger.error(f"图像生成模型下载失败: {e}")
        return False

def download_background_removal_model():
    """下载背景移除模型"""
    try:
        from modelscope.pipelines import pipeline
        from modelscope.utils.constant import Tasks
        
        pipeline = pipeline(
            Tasks.semantic_segmentation,
            model='damo/cv_san_background-removal',
            model_revision='v1.0.1'
        )
        logger.info("背景移除模型下载完成")
        return True
    except Exception as e:
        logger.error(f"背景移除模型下载失败: {e}")
        return False

def check_and_download_all_models():
    """检查并下载所有模型"""
    print("开始下载魔搭模型...")
    
    downloads = [
        ("风格迁移模型", download_style_transfer_model),
        ("去噪模型", download_denoising_model),
        ("图像修复模型", download_inpainting_model),
        ("图像生成模型", download_generation_model),
        ("背景移除模型", download_background_removal_model)
    ]
    
    for name, download_func in downloads:
        print(f"正在下载 {name}...")
        success = download_func()
        if success:
            print(f"✓ {name} 下载成功")
        else:
            print(f"✗ {name} 下载失败，将使用备用方法")
    
    print("模型下载检查完成!")

if __name__ == "__main__":
    check_and_download_all_models()


# https://www.modelscope.cn/models/AI-ModelScope/stable-diffusion-v1-5/
# https://www.modelscope.cn/models/stabilityai/stable-diffusion-2-inpainting/summary