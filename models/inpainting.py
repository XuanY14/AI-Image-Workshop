import torch
from diffusers import StableDiffusionInpaintPipeline
from PIL import Image
import os
from config.settings import DEVICE, MODELS_CONFIG

class InpaintingModel:
    def __init__(self):
        self.model = None
        self.device = DEVICE
        self.loaded_model_path = None
        self.load_model()
    
    def load_model(self):
        """加载图像修复模型"""
        model_path = MODELS_CONFIG["inpainting"]["local_path"]
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"模型路径不存在: {model_path}")
        
        print(f"从本地路径加载模型: {model_path}")
        try:
            self.model = StableDiffusionInpaintPipeline.from_pretrained(
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
        
        print(f"图像修复模型加载完成，使用设备: {self.device}")
        print(f"模型路径: {self.loaded_model_path}")
    
    def _get_optimal_size(self, original_size):
        """获取最优的处理尺寸，确保是64的倍数"""
        w, h = original_size
        max_size = 960  # 降低最大尺寸，更安全
        
        # 如果任一边超过最大尺寸，按比例缩小
        if max(w, h) > max_size:
            if w > h:
                new_w = max_size
                new_h = int(h * max_size / w)
            else:
                new_h = max_size
                new_w = int(w * max_size / h)
            w, h = new_w, new_h
        
        w = max(64, ((w // 64) * 64))
        h = max(64, ((h // 64) * 64))
        
        return (w, h)
    
    @torch.no_grad()
    def inpaint_image(self, image, mask, prompt="", num_inference_steps=30, guidance_scale=7.5):
        """
        执行图像修复
        Args:
            image: 待修复的图片 (PIL Image)
            mask: 掩码图片 (PIL Image) - 白色为修复区域，黑色为保留区域
            prompt: 修复提示词
            num_inference_steps: 推理步数
            guidance_scale: 引导强度
        Returns:
            修复后的图片 (PIL Image)
        """
        # 保存原始尺寸
        original_size = image.size
        
        # 如果没有提供提示词，使用默认提示词
        if not prompt:
            prompt = "seamless repair, natural background continuation, consistent lighting and texture, clean, photorealistic"
        
        # 确保图像是RGB模式，掩码是L模式
        if image.mode != 'RGB':
            image = image.convert('RGB')
        if mask.mode != 'L':
            mask = mask.convert('L')
        
        if image.size != mask.size:
            mask = mask.resize(image.size, Image.Resampling.NEAREST)
        
        target_size = self._get_optimal_size(image.size)
        image = image.resize(target_size, Image.Resampling.LANCZOS)
        mask = mask.resize(target_size, Image.Resampling.NEAREST)
        
        print(f"调整到目标尺寸进行修复: {target_size}")
        
        try:
            result = self.model(
                prompt=prompt,
                image=image,
                mask_image=mask,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                generator=torch.manual_seed(42),
                output_type="pil"
            ).images[0]
            
            if result.size != original_size:
                result = result.resize(original_size, Image.Resampling.LANCZOS)
                
        except RuntimeError as e:
            if "Sizes of tensors must match" in str(e):
                print(f"张量维度错误，使用标准尺寸重试: {e}")
                # 使用标准尺寸重试
                standard_size = (512, 512)
                image_std = image.resize(standard_size, Image.Resampling.LANCZOS)
                mask_std = mask.resize(standard_size, Image.Resampling.NEAREST)
                
                result = self.model(
                    prompt=prompt,
                    image=image_std,
                    mask_image=mask_std,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale,
                    generator=torch.manual_seed(42),
                    output_type="pil"
                ).images[0]
                
                # 恢复到原始尺寸
                if original_size != standard_size:
                    result = result.resize(original_size, Image.Resampling.LANCZOS)
            else:
                raise e
        
        return result
    
    def process(self, image, mask, prompt="", num_inference_steps=30, guidance_scale=7.5):
        """处理接口"""
        if self.model is None:
            raise RuntimeError("模型未正确加载")
        
        return self.inpaint_image(
            image=image,
            mask=mask,
            prompt=prompt,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale
        )
    
    def get_model_info(self):
        """获取模型信息"""
        return {
            "device": self.device,
            "model_path": self.loaded_model_path,
            "model_type": "StableDiffusionInpaintPipeline",
            "is_loaded": self.model is not None
        }

# 测试代码
if __name__ == "__main__":
    print("初始化图像修复模型...")
    try:
        model = InpaintingModel()
        info = model.get_model_info()
        print(f"模型信息: {info}")
        print("图像修复模型初始化完成!")
    except Exception as e:
        print(f"模型初始化失败: {e}")
        import traceback
        traceback.print_exc()