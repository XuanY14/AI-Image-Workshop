import torch
from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image
import os
from config.settings import DEVICE, MODELS_CONFIG

class StyleTransferModel:
    def __init__(self):
        self.model = None
        self.device = DEVICE
        self.loaded_model_path = None
        self.load_model()
    
    def load_model(self):
        """加载风格迁移模型"""
        model_path = MODELS_CONFIG["style_transfer"]["local_path"]
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"模型路径不存在: {model_path}")
        
        print(f"从本地路径加载模型: {model_path}")
        try:
            self.model = StableDiffusionImg2ImgPipeline.from_pretrained(
                model_path,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                safety_checker=None
            ).to(self.device)
            self.loaded_model_path = str(model_path)
        except Exception as e:
            print(f"加载模型失败: {e}")
            raise
        
        # 启用内存优化
        if self.device == "cuda":
            try:
                self.model.enable_attention_slicing()
                if hasattr(self.model, 'enable_xformers_memory_efficient_attention'):
                    self.model.enable_xformers_memory_efficient_attention()
            except Exception as e:
                print(f"内存优化设置失败: {e}")
        
        print(f"风格迁移模型加载完成，使用设备: {self.device}")
        print(f"模型路径: {self.loaded_model_path}")
    
    @torch.no_grad()
    def transfer_style(self, content_image, style_prompt, strength=0.7, num_inference_steps=30, guidance_scale=7.5):
        """
        执行风格迁移
        Args:
            content_image: 内容图片 (PIL Image)
            style_prompt: 风格描述文本
            strength: 风格强度 (0-1)
            num_inference_steps: 推理步数
            guidance_scale: 引导强度
        Returns:
            风格迁移后的图片 (PIL Image)
        """
        # 准备提示词
        full_prompt = f"{style_prompt}, high quality, detailed, masterpiece, best quality"
        
        # 生成图像
        result = self.model(
            prompt=full_prompt,
            image=content_image,
            strength=strength,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            generator=torch.manual_seed(42)  
        ).images[0]
        
        return result
    
    def process(self, content_image, style_prompt, strength=0.7, num_inference_steps=30, guidance_scale=7.5):
        """处理接口"""
        if self.model is None:
            raise RuntimeError("模型未正确加载")
        
        return self.transfer_style(
            content_image=content_image,
            style_prompt=style_prompt,
            strength=strength,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale
        )
    
    def get_model_info(self):
        """获取模型信息"""
        return {
            "device": self.device,
            "model_path": self.loaded_model_path,
            "model_type": "StableDiffusionImg2ImgPipeline",
            "is_loaded": self.model is not None
        }

# 测试代码
if __name__ == "__main__":
    print("初始化风格迁移模型...")
    try:
        model = StyleTransferModel()
        info = model.get_model_info()
        print(f"模型信息: {info}")
        print("风格迁移模型初始化完成!")
    except Exception as e:
        print(f"模型初始化失败: {e}")