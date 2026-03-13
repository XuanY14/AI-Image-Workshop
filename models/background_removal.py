import torch
import numpy as np
from PIL import Image, ImageChops
import cv2
import os
from config.settings import DEVICE, MODELS_CONFIG
from typing import Tuple, Optional

class BackgroundRemovalModel:
    def __init__(self):
        self.device = DEVICE
        # 预计算GrabCut的模型缓存
        self._bgd_model = np.zeros((1, 65), np.float64)
        self._fgd_model = np.zeros((1, 65), np.float64)
        # 边缘检测的预定义核
        self._edge_kernel = np.ones((5, 5), np.uint8)
        self._morph_kernel = np.ones((10, 10), np.uint8)
        print(f"背景移除模型初始化完成，使用设备: {self.device}")

    def _create_rgba(self, rgb: np.ndarray, alpha: np.ndarray) -> Image.Image:
        """统一创建RGBA图像，避免重复代码"""
        # 优化：直接使用PIL操作避免不必要的数组拷贝
        rgb_img = Image.fromarray(rgb)
        alpha_img = Image.fromarray(alpha).convert('L')
        return Image.merge('RGBA', (*rgb_img.split(), alpha_img))

    def _auto_rect(self, h: int, w: int) -> Tuple[int, int, int, int]:
        """智能计算GrabCut矩形区域，避免硬编码"""
        # 基于图像尺寸动态计算安全边界
        margin_h = max(10, int(0.1 * h))
        margin_w = max(10, int(0.1 * w))
        
        # 确保矩形在图像内部
        x1 = margin_w
        y1 = margin_h
        x2 = w - margin_w
        y2 = h - margin_h
        
        # 防止无效矩形
        if x2 <= x1 or y2 <= y1:
            x1, y1 = max(0, w//4), max(0, h//4)
            x2, y2 = min(w, 3*w//4), min(h, 3*h//4)
        
        return (x1, y1, x2 - x1, y2 - y1)

    def remove_background_grabcut(self, image: Image.Image) -> Image.Image:
        """优化版GrabCut算法，增加鲁棒性和性能"""
        img_array = np.array(image)
        h, w = img_array.shape[:2]
        
        # 异常处理：过小图像
        if min(h, w) < 50:
            return self.remove_background_simple_threshold(image)
        
        # 智能矩形区域
        rect = self._auto_rect(h, w)
        
        try:
            # 重用预分配模型
            bgd_model = self._bgd_model.copy()
            fgd_model = self._fgd_model.copy()
            
            mask = np.zeros((h, w), np.uint8)
            cv2.grabCut(
                img_array, 
                mask, 
                rect, 
                bgd_model, 
                fgd_model, 
                3, 
                cv2.GC_INIT_WITH_RECT
            )
            
            # 优化掩码生成
            mask_fg = np.where((mask == 1) | (mask == 3), 255, 0).astype('uint8')
            
            # 后处理：去除噪点
            mask_fg = cv2.morphologyEx(mask_fg, cv2.MORPH_CLOSE, self._morph_kernel)
            mask_fg = cv2.GaussianBlur(mask_fg, (5, 5), 0)
            
            # 保留原始色彩，仅应用透明度
            return self._create_rgba(img_array, mask_fg)
            
        except cv2.error as e:
            print(f"GrabCut处理失败: {str(e)}，回退到简单阈值方法")
            return self.remove_background_simple_threshold(image)

    def remove_background_simple_threshold(self, image: Image.Image) -> Image.Image:
        """优化版阈值方法，增加自适应能力"""
        img_array = np.array(image)
        
        # 转换为灰度并增强对比度
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        gray = cv2.equalizeHist(gray)
        
        # 自适应阈值
        thresh = cv2.adaptiveThreshold(
            gray, 255, 
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 
            11, 2
        )
        
        # 智能判断是否需要反转
        fg_ratio = np.sum(thresh) / (thresh.size * 255)
        if fg_ratio > 0.7:  # 前景占比过大时反转
            thresh = 255 - thresh
        
        # 优化边缘
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, self._morph_kernel)
        thresh = cv2.GaussianBlur(thresh, (5, 5), 0)
        _, thresh = cv2.threshold(thresh, 127, 255, cv2.THRESH_BINARY)
        
        return self._create_rgba(img_array, thresh)

    def remove_background_edge_detection(self, image: Image.Image) -> Image.Image:
        """优化版边缘检测，增加主体识别能力"""
        img_array = np.array(image)
        h, w = img_array.shape[:2]
        
        # 多尺度边缘融合
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        edges1 = cv2.Canny(gray, 30, 90)
        edges2 = cv2.Canny(gray, 50, 150)
        edges = cv2.bitwise_or(edges1, edges2)
        
        # 智能轮廓选择
        contours, _ = cv2.findContours(
            edges, 
            cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        # 选择最大轮廓（假设主体是最大物体）
        if contours:
            main_contour = max(contours, key=cv2.contourArea)
            mask = np.zeros((h, w), dtype=np.uint8)
            cv2.drawContours(mask, [main_contour], -1, 255, thickness=cv2.FILLED)
            
            # 优化边缘
            mask = cv2.dilate(mask, self._edge_kernel, iterations=2)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self._morph_kernel)
            mask = cv2.GaussianBlur(mask, (7, 7), 0)
            _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
        else:
            # 无轮廓时回退
            return self.remove_background_simple_threshold(image)
        
        return self._create_rgba(img_array, mask)

    def process(self, image: Image.Image, method: str = "auto") -> Image.Image:
        """
        智能处理接口
        Args:
            image: 输入图像 (PIL Image)
            method: 处理方法 ("grabcut", "simple", "edge", "auto")
        """
        # 智能方法选择
        if method == "auto":
            w, h = image.size
            # 小图像用简单方法，大图像用GrabCut
            method = "simple" if min(w, h) < 300 else "grabcut"
        
        try:
            if method == "simple":
                return self.remove_background_simple_threshold(image)
            elif method == "edge":
                return self.remove_background_edge_detection(image)
            else:  # 包括"grabcut"和"auto"的回退
                return self.remove_background_grabcut(image)
        except Exception as e:
            print(f"背景移除失败: {str(e)}，使用安全回退方法")
            return self.remove_background_simple_threshold(image)

    def get_model_info(self) -> dict:
        """获取优化后的模型信息"""
        return {
            "device": self.device,
            "model_type": "Hybrid Background Removal",
            "methods": ["grabcut", "simple", "edge", "auto"],
            "is_loaded": True,
            "optimizations": [
                "Intelligent region selection",
                "Adaptive thresholding",
                "Robust fallback mechanisms",
                "Memory reuse for OpenCV models",
                "Edge-preserving smoothing"
            ]
        }

# 测试代码
if __name__ == "__main__":
    print("初始化背景移除模型...")
    model = BackgroundRemovalModel()
    info = model.get_model_info()
    print(f"模型信息: {info}")
    
    # 添加实际测试
    try:
        test_img = Image.open("test.jpg").convert("RGB")
        print("测试GrabCut方法...")
        result = model.process(test_img, method="grabcut")
        result.save("output_grabcut.png")
        
        print("测试自动方法选择...")
        result_auto = model.process(test_img, method="auto")
        result_auto.save("output_auto.png")
        print("处理完成！结果已保存")
    except Exception as e:
        print(f"测试失败: {str(e)}")
    
    print("背景移除模型初始化完成!")