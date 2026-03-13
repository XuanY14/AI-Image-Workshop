# AI图像工坊

AI图像工坊是一个基于深度学习的多功能图像处理工具箱，集成了风格迁移、去噪、修复、生成和背景去除等多种AI图像趣味玩法和实用功能，并具有一个可视化界面。

![image]([图片路径](https://github.com/XuanY14/AI-Image-Workshop/blob/master/image.png))

## 🚀 快速开始

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd ai_image_workshop
```

2. **创建虚拟环境** 
```bash
conda create -n ai_image python=3.9
conda activate ai_image
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **准备模型** (如果已有预训练模型)
将您的模型文件放置在 `models_data/` 目录下：
- `models_data/stable_diffusion/` - SD基础模型
- `models_data/stable-diffusion-2-inpainting/` - SD修复模型

5. **启动应用**
```bash
streamlit run app.py
```
