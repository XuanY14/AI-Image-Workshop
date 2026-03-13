import torch
from diffusers import StableDiffusionPipeline
from PIL import Image
import os
from config.settings import DEVICE, MODELS_CONFIG

class GenerationModel:
    def __init__(self):
        self.model = None
        self.device = DEVICE
        self.loaded_model_path = None
        self.load_model()
    
    def load_model(self):
        """加载图像生成模型"""
        model_path = MODELS_CONFIG["generation"]["local_path"]
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"模型路径不存在: {model_path}")
        
        print(f"从本地路径加载模型: {model_path}")
        try:
            self.model = StableDiffusionPipeline.from_pretrained(
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
        
        print(f"图像生成模型加载完成，使用设备: {self.device}")
        print(f"模型路径: {self.loaded_model_path}")
    
    @torch.no_grad()
    def generate_image(self, prompt, negative_prompt="", num_images=1, 
                      num_inference_steps=50, guidance_scale=7.5):
        """
        生成图像
        Args:
            prompt: 正面提示词
            negative_prompt: 负面提示词
            num_images: 生成图片数量
            num_inference_steps: 推理步数
            guidance_scale: 引导强度
        Returns:
            生成的图片列表
        """
        results = self.model(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_images_per_prompt=num_images,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            generator=torch.manual_seed(42)  
        ).images
        
        return results
    
    def process(self, prompt, negative_prompt="", num_images=1, 
               num_inference_steps=50, guidance_scale=7.5):
        """处理接口"""
        if self.model is None:
            raise RuntimeError("模型未正确加载")
        
        return self.generate_image(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_images=num_images,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale
        )
    
    def get_model_info(self):
        """获取模型信息"""
        return {
            "device": self.device,
            "model_path": self.loaded_model_path,
            "model_type": "StableDiffusionPipeline",
            "is_loaded": self.model is not None
        }

# 测试代码
if __name__ == "__main__":
    print("初始化图像生成模型...")
    try:
        model = GenerationModel()
        info = model.get_model_info()
        print(f"模型信息: {info}")
        print("图像生成模型初始化完成!")
    except Exception as e:
        print(f"模型初始化失败: {e}")