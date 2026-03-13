import numpy as np
from PIL import Image
from typing import Literal
import cv2  # OpenCV 提供高效图像处理

class ClassicDenoising:
    """
    基于经典图像处理算法的去噪器（无需深度学习模型）
    支持多种噪声类型和去噪方法
    """
    
    def __init__(self):
        pass

    def _pil_to_cv2(self, pil_image: Image.Image) -> np.ndarray:
        """将 PIL Image 转为 OpenCV BGR numpy array"""
        img = np.array(pil_image)
        if img.ndim == 2:
            return img  # 灰度图
        elif img.shape[2] == 3:
            return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        elif img.shape[2] == 4:
            return cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        else:
            raise ValueError("不支持的图像通道数")

    def _cv2_to_pil(self, cv2_img: np.ndarray) -> Image.Image:
        """将 OpenCV BGR numpy array 转为 PIL Image (RGB)"""
        if cv2_img.ndim == 2:
            return Image.fromarray(cv2_img)
        else:
            rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
            return Image.fromarray(rgb)

    def denoise_image(
        self,
        noisy_image: Image.Image,
        method: Literal["bilateral", "nlm", "median", "gaussian", "fastnlm"] = "bilateral",
        **kwargs
    ) -> Image.Image:
        """
        使用经典算法对图像去噪
        
        Args:
            noisy_image (PIL.Image): 输入含噪图像
            method (str): 去噪方法
                - "median": 中值滤波（适合椒盐噪声）
                - "gaussian": 高斯模糊（简单但会模糊边缘）
                - "bilateral": 双边滤波（保边去噪，适合高斯噪声）
                - "nlm": 非局部均值（Non-Local Means，高质量去噪）
                - "fastnlm": 快速非局部均值（OpenCV 的 fastNlMeansDenoising）
            **kwargs: 方法特定参数
        
        Returns:
            PIL.Image: 去噪后的图像
        """
        img_cv = self._pil_to_cv2(noisy_image)
        is_color = img_cv.ndim == 3

        if method == "median":
            # 适合椒盐噪声
            kernel_size = kwargs.get("kernel_size", 3)
            if kernel_size % 2 == 0:
                kernel_size += 1
            if is_color:
                denoised = cv2.medianBlur(img_cv, kernel_size)
            else:
                denoised = cv2.medianBlur(img_cv, kernel_size)

        elif method == "gaussian":
            kernel_size = kwargs.get("kernel_size", 5)
            sigma = kwargs.get("sigma", 1.0)
            if kernel_size % 2 == 0:
                kernel_size += 1
            denoised = cv2.GaussianBlur(img_cv, (kernel_size, kernel_size), sigma)

        elif method == "bilateral":
            # 保边去噪，适合轻微高斯噪声
            d = kwargs.get("d", 9)
            sigma_color = kwargs.get("sigma_color", 75)
            sigma_space = kwargs.get("sigma_space", 75)
            denoised = cv2.bilateralFilter(img_cv, d, sigma_color, sigma_space)

        elif method == "nlm":
            # 非局部均值，高质量但较慢
            h = kwargs.get("h", 10)  # 滤波强度
            h_color = kwargs.get("h_color", 10) if is_color else h
            template_window_size = kwargs.get("template_window_size", 7)
            search_window_size = kwargs.get("search_window_size", 21)
            if is_color:
                denoised = cv2.fastNlMeansDenoisingColored(
                    img_cv, None, h, h_color, template_window_size, search_window_size
                )
            else:
                denoised = cv2.fastNlMeansDenoising(
                    img_cv, None, h, template_window_size, search_window_size
                )
        elif method == "fastnlm":
            # OpenCV 的快速 NLM，其实是 fastNlMeansDenoising
            return self.denoise_image(noisy_image, method="nlm", **kwargs)
        else:
            raise ValueError(f"不支持的去噪方法: {method}")

        return self._cv2_to_pil(denoised)

    def process(self, noisy_image: Image.Image, method="bilateral", **kwargs):
        return self.denoise_image(noisy_image, method=method, **kwargs)

    def get_model_info(self):
        return {
            "device": "CPU (纯算法)",
            "model_type": "Classic Image Processing",
            "methods_available": ["median", "gaussian", "bilateral", "nlm"],
            "is_loaded": True
        }

# 创建一个别名
DenoisingModel = ClassicDenoising