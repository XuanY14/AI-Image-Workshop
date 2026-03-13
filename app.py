# import streamlit as st
# import numpy as np
# from PIL import Image
# import os
# import tempfile
# from pathlib import Path
# from io import BytesIO

# # 导入工具函数
# from utils.image_processing import (
#     resize_image, 
#     preprocess_image, 
#     postprocess_image, 
#     add_noise, 
#     create_damage_mask,
#     validate_image
# )

# from config.settings import TEMP_DIR

# # ===== 页面配置与主题管理 =====
# st.set_page_config(
#     page_title="AI图像工坊",
#     page_icon="🎨",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # 主题切换
# if 'theme' not in st.session_state:
#     st.session_state.theme = "light"

# def toggle_theme():
#     st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

# # ===== 修正后的CSS样式（修复所有可见性问题） =====
# def apply_theme():
#     if st.session_state.theme == "dark":
#         bg_color = "#0e141b"
#         card_bg = "#1a2330"
#         text_color = "#e6edf3"
#         accent = "#58a6ff"
#         border_color = "#30363d"
#     else:
#         bg_color = "#f8f9fa"
#         card_bg = "#ffffff"
#         text_color = "#24292f"
#         accent = "#2969ff"
#         border_color = "#d1d8e0"

#     return f"""
#     <style>
#         /* 基础样式 */
#         .stApp {{
#             background: {bg_color};
#             color: {text_color};
#             font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
#         }}
        
#         /* 修复主标题可见性 - 使用纯色文字 */
#         .main-header {{
#             font-size: 3rem;
#             font-weight: 800;
#             color: {accent};
#             text-align: center;
#             margin: 2rem 0 1rem 0;
#             padding: 1rem;
#             position: relative;
#         }}
        
#         /* 添加渐变装饰条 */
#         .main-header::after {{
#             content: '';
#             display: block;
#             width: 120px;
#             height: 4px;
#             background: linear-gradient(90deg, {accent} 0%, #36b9ff 100%);
#             margin: 0.5rem auto 0;
#             border-radius: 2px;
#         }}
        
#         /* 副标题样式 */
#         .subtitle {{
#             text-align: center;
#             color: gray;
#             font-size: 1.2rem;
#             margin-bottom: 2rem;
#             font-weight: 400;
#         }}
        
#         /* 功能容器卡片 */
#         .function-container {{
#             background: {card_bg};
#             border-radius: 1rem;
#             padding: 2rem;
#             margin: 1rem 0;
#             border: 1px solid {border_color};
#             box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
#             color: {text_color};
#         }}
        
#         /* 图片卡片 */
#         .image-card {{
#             background: {card_bg};
#             border-radius: 0.75rem;
#             padding: 1rem;
#             margin: 0.5rem;
#             border: 1px solid {border_color};
#             transition: all 0.3s ease;
#             color: {text_color};
#         }}
        
#         .image-card:hover {{
#             border-color: {accent};
#             box-shadow: 0 4px 12px rgba(41, 105, 255, 0.15);
#         }}
        
#         /* 导航卡片 */
#         .nav-card {{
#             background: {card_bg};
#             border-radius: 1rem;
#             padding: 1.5rem;
#             margin: 0.5rem 0;
#             cursor: pointer;
#             transition: all 0.3s ease;
#             border: 1px solid {border_color};
#             box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
#             color: {text_color};
#         }}
        
#         .nav-card:hover {{
#             transform: translateY(-4px);
#             box-shadow: 0 8px 24px rgba(41, 105, 255, 0.2);
#             border-color: {accent};
#         }}
        
#         /* 按钮样式 */
#         .stButton>button {{
#             background: linear-gradient(90deg, {accent} 0%, #36b9ff 100%);
#             color: white;
#             border: none;
#             border-radius: 0.5rem;
#             padding: 0.75rem 2rem;
#             font-weight: 600;
#             cursor: pointer;
#             transition: all 0.3s ease;
#             box-shadow: 0 4px 12px rgba(41, 105, 255, 0.3);
#         }}
        
#         .stButton>button:hover {{
#             transform: translateY(-2px);
#             box-shadow: 0 6px 20px rgba(41, 105, 255, 0.4);
#         }}
        
#         /* 信息提示框 */
#         .info-box {{
#             padding: 1rem 1.5rem;
#             border-radius: 0.75rem;
#             margin: 1rem 0;
#             border-left: 4px solid;
#             color: {text_color};
#         }}
        
#         .info-box.success {{ 
#             border-color: #2ecc71; 
#             background: rgba(46, 204, 113, 0.1); 
#         }}
#         .info-box.warning {{ 
#             border-color: #f1c40f; 
#             background: rgba(241, 196, 15, 0.1); 
#         }}
#         .info-box.error {{ 
#             border-color: #e74c3c; 
#             background: rgba(231, 76, 60, 0.1); 
#         }}
        
#         /* 侧边栏描述文字 */
#         .sidebar-desc {{
#             font-size: 0.85rem;
#             color: gray;
#             margin: -0.5rem 0 1rem 0;
#             padding: 0 0.5rem;
#         }}
        
#         /* 移除多余间距 */
#         .block-container {{
#             padding-top: 1rem;
#         }}
        
#         /* 确保标题文字可见 */
#         h1, h2, h3, h4, h5, h6 {{
#             color: {text_color} !important;
#         }}
#     </style>
#     """

# st.markdown(apply_theme(), unsafe_allow_html=True)

# # ===== 将主题切换按钮移到侧边栏顶部 =====
# with st.sidebar:
#     st.button(
#         "🌓 切换主题",
#         on_click=toggle_theme,
#         key="theme_toggle",
#         help="切换深色/浅色模式"
#     )
#     st.markdown("---")  # 添加分隔线

# # ===== 主标题和副标题（确保可见） =====
# st.markdown('<h1 class="main-header">🎨 AI图像工坊</h1>', unsafe_allow_html=True)
# st.markdown('<div class="subtitle">智能图像处理工具箱</div>', unsafe_allow_html=True)
# st.markdown("---")

# # ===== 导航栏 =====
# st.sidebar.markdown("## 🔧 功能导航", unsafe_allow_html=True)

# # 功能列表
# FUNCTIONS = {
#     "🏠 首页介绍": "探索AI图像处理的无限可能",
#     "🖼️ 照片风格迁移": "将艺术风格应用到你的照片",
#     "🧹 照片去噪": "智能移除图像噪声",
#     "🔧 图像修复": "修复受损图像区域",
#     "✨ 图像生成": "从文本创造图像",
#     "🖼️ 背景去除": "一键分离主体与背景"
# }

# # 渲染导航（按钮+描述）
# for i, (func_name, desc) in enumerate(FUNCTIONS.items()):
#     if st.sidebar.button(
#         func_name,
#         key=f"nav_title_{i}",
#         use_container_width=True
#     ):
#         st.session_state.current_function = func_name
    
#     st.sidebar.markdown(
#         f'<p class="sidebar-desc">{desc}</p>', 
#         unsafe_allow_html=True
#     )

# # 获取当前功能
# current_function = st.session_state.get("current_function", "🏠 首页介绍")

# # ===== 功能页面渲染函数 =====
# def render_home():
#     st.markdown('<div class="function-container">', unsafe_allow_html=True)
#     st.markdown("## 🚀 欢迎来到AI图像工坊")
#     st.markdown(
#         f'<p style="font-size: 1.1rem; line-height: 1.8;">'
#         '这是一个集成了多种前沿AI图像处理技术的工具箱，让您的图像处理工作变得简单而强大。'
#         '</p>',
#         unsafe_allow_html=True
#     )
    
#     # 修复：使用2列布局避免最后一行出现空白卡片
#     features = [
#         ("🎨 风格迁移", "将梵高的星空风格应用到您的照片"),
#         ("✨ 智能去噪", "去除低光照照片的噪点"),
#         ("🛠️ 图像修复", "修复老照片的破损区域"),
#         ("🤖 AI生成", "将文字描述转化为精美图像"),
#         ("🖼️ 背景分离", "自动抠图，精准识别"),
#     ]
    
#     if len(features) % 3 == 0:
#         cols = st.columns(3)
#         items_per_col = len(features) // 3
#     else:
#         # 如果有余数，使用2列避免空白
#         cols = st.columns(2)
#         items_per_col = (len(features) + 1) // 2
    
#     for i, (title, desc) in enumerate(features):
#         col_idx = i % len(cols)
#         with cols[col_idx]:
#             st.markdown(f"""
#             <div class="nav-card" style="text-align: center; padding: 2rem 1rem;">
#                 <h3 style="color: {st.session_state.theme == 'dark' and '#58a6ff' or '#2969ff'}; margin-bottom: 0.5rem;">{title}</h3>
#                 <p style="font-size: 0.9rem; color: gray;">{desc}</p>
#             </div>
#             """, unsafe_allow_html=True)
    
#     st.markdown(
#         f"""
#         <div class="info-box warning">
#             <strong>💡 首次使用提示：</strong>
#             某些功能首次使用需要加载几分钟时间，请耐心等待。
#         </div>
#         """,
#         unsafe_allow_html=True
#     )
    
#     st.markdown('</div>', unsafe_allow_html=True)

# def render_style_transfer():
#     st.markdown('<div class="function-container">', unsafe_allow_html=True)
#     st.markdown("### 🎨 照片风格迁移")
#     st.info("上传内容图片并描述目标风格，AI将智能融合艺术风格")
    
#     col1, col2 = st.columns([1, 1])
    
#     with col1:
#         content_image = st.file_uploader(
#             "上传内容图片", 
#             type=["jpg", "jpeg", "png"], 
#             key="content",
#             help="选择您想要改变风格的照片"
#         )
#         if content_image:
#             content_img = Image.open(content_image)
#             content_img = validate_image(content_img)
#             content_img = preprocess_image(content_img)
#             content_img = resize_image(content_img)
#             st.markdown('<div class="image-card">', unsafe_allow_html=True)
#             st.image(content_img, caption="📸 内容图片", use_column_width=True)
#             st.markdown('</div>', unsafe_allow_html=True)
    
#     with col2:
#         style_prompt = st.text_input(
#             "🎨 风格描述", 
#             "impressionist painting style, colorful brush strokes, artistic",
#             help="例如：油画风格、水彩画、赛博朋克、复古胶片等"
#         )
#         strength = st.slider(
#             "💪 风格强度", 0.1, 1.0, 0.7, step=0.1,
#             help="值越大，风格效果越明显"
#         )
#         steps = st.slider(
#             "⚡ 推理步数", 10, 50, 30, step=5,
#             help="步数越多，质量越高但速度越慢"
#         )
#         guidance = st.slider(
#             "🎯 引导强度", 1.0, 20.0, 7.5, step=0.5,
#             help="控制生成图像与提示词的匹配程度"
#         )
    
#     if st.button("🚀 执行风格迁移", use_container_width=True) and content_image:
#         with st.spinner("🤖 正在加载模型并处理中..."):
#             try:
#                 progress_bar = st.progress(0)
#                 from models.style_transfer import StyleTransferModel
#                 model = StyleTransferModel()
                
#                 result_img = model.process(
#                     content_image=content_img,
#                     style_prompt=style_prompt,
#                     strength=strength,
#                     num_inference_steps=steps,
#                     guidance_scale=guidance
#                 )
#                 result_img = postprocess_image(result_img)
#                 progress_bar.progress(100)
                
#                 st.markdown("---")
#                 cols = st.columns(2)
#                 with cols[0]:
#                     st.markdown('<div class="image-card">', unsafe_allow_html=True)
#                     st.image(content_img, caption="📋 原始图片", use_column_width=True)
#                     st.markdown('</div>', unsafe_allow_html=True)
#                 with cols[1]:
#                     st.markdown('<div class="image-card">', unsafe_allow_html=True)
#                     st.image(result_img, caption="✨ 风格化结果", use_column_width=True)
#                     st.markdown('</div>', unsafe_allow_html=True)
                
#                 buf = BytesIO()
#                 result_img.save(buf, format="PNG")
#                 st.download_button(
#                     label="⬇️ 下载结果图片",
#                     data=buf.getvalue(),
#                     file_name="style_transferred_result.png",
#                     mime="image/png",
#                     use_container_width=True,
#                     key="download_style"
#                 )
                
#                 st.success("✅ 风格迁移完成！")
                
#             except Exception as e:
#                 st.error(f"❌ 处理过程中出现错误: {str(e)}")
    
#     st.markdown('</div>', unsafe_allow_html=True)

# def render_denoising():
#     st.markdown('<div class="function-container">', unsafe_allow_html=True)
#     st.markdown("### 🧹 照片去噪")
#     st.info("智能移除图像噪声，恢复清晰细节")
    
#     uploaded_file = st.file_uploader(
#         "上传图片", 
#         type=["jpg", "jpeg", "png"],
#         help="支持JPG、PNG格式"
#     )
    
#     if uploaded_file is not None:
#         original_img = Image.open(uploaded_file)
#         original_img = validate_image(original_img)
#         original_img = preprocess_image(original_img)
#         original_img = resize_image(original_img)
        
#         noise_factor = st.slider(
#             "🔊 噪声强度", 0.05, 0.3, 0.1, step=0.05,
#             help="用于演示的噪声强度"
#         )
#         noisy_img = add_noise(original_img, noise_factor)
        
#         algo_options = {
#             "bilateral": "保边滤波 - 保留边缘细节",
#             "median": "中值滤波 - 适合椒盐噪声",
#             "nlm": "非局部均值 - 高质量去噪",
#             "gaussian": "高斯模糊 - 简单快速"
#         }
        
#         denoise_method = st.selectbox(
#             "🧪 选择去噪算法",
#             options=list(algo_options.keys()),
#             format_func=lambda x: f"{x} - {algo_options[x].split(' - ')[1]}",
#             help="不同算法适用于不同类型的噪声"
#         )
        
#         with st.expander("⚙️ 算法参数设置", expanded=True):
#             if denoise_method == "bilateral":
#                 d = st.slider("滤波距离", 1, 20, 9)
#                 sigma_color = st.slider("颜色相似度", 10, 200, 75)
#                 sigma_space = st.slider("空间相似度", 10, 200, 75)
#                 params = {"d": d, "sigma_color": sigma_color, "sigma_space": sigma_space}
#             elif denoise_method == "median":
#                 kernel_size = st.slider("核大小（奇数）", 1, 11, 3, step=2)
#                 params = {"kernel_size": kernel_size}
#             elif denoise_method == "nlm":
#                 h = st.slider("去噪强度h", 1, 20, 10)
#                 template_ws = st.slider("模板窗口大小", 3, 15, 7)
#                 search_ws = st.slider("搜索窗口大小", 10, 30, 21)
#                 params = {"h": h, "template_window_size": template_ws, "search_window_size": search_ws}
#             else:
#                 kernel_size = st.slider("核大小（奇数）", 1, 15, 5, step=2)
#                 sigma = st.slider("高斯标准差", 0.1, 5.0, 1.0)
#                 params = {"kernel_size": kernel_size, "sigma": sigma}
        
#         if st.button("🚀 执行去噪", use_container_width=True):
#             with st.spinner("🤖 正在去噪处理..."):
#                 try:
#                     progress = st.progress(0)
#                     from models.denoising import DenoisingModel
#                     model = DenoisingModel()
                    
#                     denoised_img = model.process(
#                         noisy_image=noisy_img,
#                         method=denoise_method,
#                         **params
#                     )
#                     progress.progress(100)
                    
#                     st.markdown("---")
#                     cols = st.columns(3)
#                     with cols[0]:
#                         st.markdown('<div class="image-card">', unsafe_allow_html=True)
#                         st.image(original_img, caption="🖼️ 原始图片", use_column_width=True)
#                         st.markdown('</div>', unsafe_allow_html=True)
#                     with cols[1]:
#                         st.markdown('<div class="image-card">', unsafe_allow_html=True)
#                         st.image(noisy_img, caption="📢 含噪声图片", use_column_width=True)
#                         st.markdown('</div>', unsafe_allow_html=True)
#                     with cols[2]:
#                         st.markdown('<div class="image-card">', unsafe_allow_html=True)
#                         st.image(denoised_img, caption="✨ 去噪后", use_column_width=True)
#                         st.markdown('</div>', unsafe_allow_html=True)
                    
#                     buf = BytesIO()
#                     denoised_img.save(buf, format="PNG")
#                     st.download_button(
#                         label="⬇️ 下载去噪结果",
#                         data=buf.getvalue(),
#                         file_name="denoised_result.png",
#                         mime="image/png",
#                         use_container_width=True,
#                         key="download_denoise"
#                     )
                    
#                     st.success("✅ 去噪完成！")
                    
#                 except Exception as e:
#                     st.error(f"❌ 去噪过程中出现错误: {str(e)}")
    
#     st.markdown('</div>', unsafe_allow_html=True)

# def render_inpainting():
#     st.markdown('<div class="function-container">', unsafe_allow_html=True)
#     st.markdown("### 🔧 图像修复")
#     st.info("智能修复受损或缺失的图像区域")
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         image_file = st.file_uploader(
#             "上传待修复图片", 
#             type=["jpg", "jpeg", "png"], 
#             key="repair_image",
#             help="选择需要修复的图像"
#         )
#         if image_file:
#             original_img = Image.open(image_file)
#             original_img = validate_image(original_img)
#             original_img = preprocess_image(original_img)
#             original_img = resize_image(original_img)
#             st.markdown('<div class="image-card">', unsafe_allow_html=True)
#             st.image(original_img, caption="🖼️ 待修复图片", use_column_width=True)
#             st.markdown('</div>', unsafe_allow_html=True)
    
#     with col2:
#         mask_file = st.file_uploader(
#             "上传掩码图片（白色为修复区域）", 
#             type=["jpg", "jpeg", "png"], 
#             key="mask",
#             help="白色区域表示需要修复的部分"
#         )
        
#         auto_generate = st.checkbox(
#             "🤖 自动生成损坏区域掩码", 
#             value=True,
#             help="自动生成矩形损坏区域用于演示"
#         )
        
#         if auto_generate and image_file:
#             damage_ratio = st.slider(
#                 "损坏程度", 
#                 0.1, 0.5, 0.2, step=0.05,
#                 help="控制自动生成损坏区域的大小"
#             )
#             mask_img = create_damage_mask(original_img, damage_ratio)
#             st.markdown('<div class="image-card">', unsafe_allow_html=True)
#             st.image(mask_img, caption="🎯 自动生成的掩码", use_column_width=True)
#             st.markdown('</div>', unsafe_allow_html=True)
#         elif mask_file:
#             mask_img = Image.open(mask_file).convert('L')
#             st.markdown('<div class="image-card">', unsafe_allow_html=True)
#             st.image(mask_img, caption="🎯 上传的掩码", use_column_width=True)
#             st.markdown('</div>', unsafe_allow_html=True)
    
#     prompt = st.text_input(
#         "📝 修复提示词",
#         "seamless repair, natural texture, consistent lighting, high quality",
#         help="描述希望修复后的效果"
#     )
    
#     col1, col2 = st.columns(2)
#     with col1:
#         steps = st.slider("推理步数", 20, 60, 30, step=10)
#     with col2:
#         guidance = st.slider("引导强度", 1.0, 15.0, 7.5, step=0.5)
    
#     if st.button("🚀 执行修复", use_container_width=True) and image_file:
#         with st.spinner("🤖 正在修复图像..."):
#             try:
#                 progress = st.progress(0)
#                 from models.inpainting import InpaintingModel
#                 model = InpaintingModel()
                
#                 if not mask_file and auto_generate:
#                     mask_img = create_damage_mask(original_img, damage_ratio)
                
#                 result_img = model.process(
#                     image=original_img,
#                     mask=mask_img,
#                     prompt=prompt,
#                     num_inference_steps=steps,
#                     guidance_scale=guidance
#                 )
#                 result_img = postprocess_image(result_img)
#                 progress.progress(100)
                
#                 st.markdown("---")
#                 cols = st.columns(3)
#                 with cols[0]:
#                     st.markdown('<div class="image-card">', unsafe_allow_html=True)
#                     st.image(original_img, caption="🖼️ 原始图片", use_column_width=True)
#                     st.markdown('</div>', unsafe_allow_html=True)
#                 with cols[1]:
#                     st.markdown('<div class="image-card">', unsafe_allow_html=True)
#                     st.image(mask_img, caption="🎯 修复掩码", use_column_width=True)
#                     st.markdown('</div>', unsafe_allow_html=True)
#                 with cols[2]:
#                     st.markdown('<div class="image-card">', unsafe_allow_html=True)
#                     st.image(result_img, caption="✨ 修复后图片", use_column_width=True)
#                     st.markdown('</div>', unsafe_allow_html=True)
                
#                 buf = BytesIO()
#                 result_img.save(buf, format="PNG")
#                 st.download_button(
#                     label="⬇️ 下载修复结果",
#                     data=buf.getvalue(),
#                     file_name="inpainting_result.png",
#                     mime="image/png",
#                     use_container_width=True,
#                     key="download_inpaint"
#                 )
                
#                 st.success("✅ 修复完成！")
                
#             except Exception as e:
#                 st.error(f"❌ 修复过程中出现错误: {str(e)}")
    
#     st.markdown('</div>', unsafe_allow_html=True)

# def render_generation():
#     st.markdown('<div class="function-container">', unsafe_allow_html=True)
#     st.markdown("### ✨ 图像生成")
#     st.info("根据文本描述生成高质量图像")
    
#     prompt = st.text_area(
#         "📝 图像描述",
#         "A beautiful landscape with mountains and lake at sunset, high quality, detailed",
#         height=120,
#         help="详细描述您想要生成的图像内容"
#     )
    
#     negative_prompt = st.text_input(
#         "🚫 排除内容（可选）",
#         "blurry, low quality, bad anatomy, deformed, ugly",
#         help="指定不希望出现的元素"
#     )
    
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         num_images = st.slider("生成数量", 1, 4, 1)
#         guidance_scale = st.slider("引导强度", 1.0, 20.0, 7.5, step=0.5)
#     with col2:
#         steps = st.slider("推理步数", 20, 80, 50, step=5)
#     with col3:
#         width = st.slider("宽度", 256, 1024, 512, step=64)
#         height = st.slider("高度", 256, 1024, 512, step=64)
    
#     if st.button("🚀 生成图像", use_container_width=True):
#         if prompt:
#             with st.spinner("🤖 正在生成图像..."):
#                 try:
#                     progress = st.progress(0)
#                     from models.generation import GenerationModel
#                     model = GenerationModel()
#                     progress.progress(20)
                    
#                     generated_images = model.process(
#                         prompt=prompt,
#                         negative_prompt=negative_prompt,
#                         num_images=num_images,
#                         num_inference_steps=steps,
#                         guidance_scale=guidance_scale
#                     )
#                     progress.progress(100)
                    
#                     st.markdown("---")
#                     if num_images == 1:
#                         st.markdown('<div class="image-card">', unsafe_allow_html=True)
#                         st.image(generated_images[0], caption="🎨 生成的图像", use_column_width=True)
#                         st.markdown('</div>', unsafe_allow_html=True)
#                     else:
#                         cols = st.columns(num_images)
#                         for i, img in enumerate(generated_images):
#                             with cols[i]:
#                                 st.markdown('<div class="image-card">', unsafe_allow_html=True)
#                                 st.image(img, caption=f"🎨 生成图像 {i+1}", use_column_width=True)
#                                 st.markdown('</div>', unsafe_allow_html=True)
#                                 buf = BytesIO()
#                                 img.save(buf, format="PNG")
#                                 st.download_button(
#                                     label=f"⬇️ 下载图像{i+1}",
#                                     data=buf.getvalue(),
#                                     file_name=f"generated_image_{i+1}.png",
#                                     mime="image/png",
#                                     use_container_width=True,
#                                     key=f"download_gen_{i}"
#                                 )
                    
#                     st.success(f"✅ 成功生成 {num_images} 张图像！")
                    
#                 except Exception as e:
#                     st.error(f"❌ 生成过程中出现错误: {str(e)}")
#         else:
#             st.warning("⚠️ 请输入图像描述！")
    
#     st.markdown('</div>', unsafe_allow_html=True)

# def render_background_removal():
#     st.markdown('<div class="function-container">', unsafe_allow_html=True)
#     st.markdown("### 🖼️ 背景去除")
#     st.info("自动识别主体并移除背景，支持多种算法")
    
#     uploaded_file = st.file_uploader(
#         "上传图片", 
#         type=["jpg", "jpeg", "png"],
#         help="选择需要去除背景的图像"
#     )
    
#     if uploaded_file is not None:
#         original_img = Image.open(uploaded_file).convert("RGB")
#         original_img = validate_image(original_img)
#         original_img = resize_image(original_img)
        
#         method_options = {
#             "grabcut": "GrabCut算法 - 精确分割",
#             "simple": "简单阈值 - 快速处理",
#             "edge": "边缘检测 - 轮廓识别"
#         }
        
#         method_display = st.radio(
#             "🔍 选择处理方法",
#             options=list(method_options.keys()),
#             format_func=lambda x: method_options[x],
#             help="不同算法适用于不同类型的图像"
#         )
        
#         if st.button("🚀 去除背景", use_container_width=True):
#             with st.spinner("🤖 正在处理..."):
#                 try:
#                     progress = st.progress(0)
#                     from models.background_removal import BackgroundRemovalModel
#                     model = BackgroundRemovalModel()
#                     progress.progress(50)
                    
#                     result_img = model.process(original_img, method=method_display)
#                     progress.progress(100)
                    
#                     st.markdown("---")
#                     cols = st.columns(2)
#                     with cols[0]:
#                         st.markdown('<div class="image-card">', unsafe_allow_html=True)
#                         st.image(original_img, caption="🖼️ 原始图片", use_column_width=True)
#                         st.markdown('</div>', unsafe_allow_html=True)
#                     with cols[1]:
#                         st.markdown('<div class="image-card">', unsafe_allow_html=True)
#                         st.image(result_img, caption="✨ 去除背景后", use_column_width=True)
#                         st.markdown('</div>', unsafe_allow_html=True)
                    
#                     buf = BytesIO()
#                     result_img.save(buf, format="PNG")
#                     st.download_button(
#                         label="⬇️ 下载背景移除结果",
#                         data=buf.getvalue(),
#                         file_name="background_removed.png",
#                         mime="image/png",
#                         use_container_width=True,
#                         key="download_bg"
#                     )
                    
#                     st.success("✅ 背景去除完成！")
                    
#                 except Exception as e:
#                     st.error(f"❌ 背景移除过程中出现错误: {str(e)}")
    
#     st.markdown('</div>', unsafe_allow_html=True)

# # ===== 路由渲染 =====
# functions_map = {
#     "🏠 首页介绍": render_home,
#     "🖼️ 照片风格迁移": render_style_transfer,
#     "🧹 照片去噪": render_denoising,
#     "🔧 图像修复": render_inpainting,
#     "✨ 图像生成": render_generation,
#     "🖼️ 背景去除": render_background_removal,
# }

# # 渲染当前选中功能
# functions_map[current_function]()

# # ===== 页脚 =====
# st.markdown("---")
# st.markdown(
#     """
#     <div style="text-align: center; color: gray; padding: 2rem;">
#         <p>🛠️ AI图像工坊 v1.0 | 基于Streamlit构建 | 由AI驱动</p>
#         <p style="font-size: 0.85rem; margin-top: 0.5rem;">
#             所有处理均在本地完成，保障您的隐私安全
#         </p>
#     </div>
#     """,
#     unsafe_allow_html=True
# )


import streamlit as st
import numpy as np
from PIL import Image
import os
import tempfile
from pathlib import Path
from io import BytesIO

# 导入工具函数
from utils.image_processing import (
    resize_image, 
    preprocess_image, 
    postprocess_image, 
    add_noise, 
    create_damage_mask,
    validate_image
)

from config.settings import TEMP_DIR

# ===== 页面配置与主题管理 =====
st.set_page_config(
    page_title="AI图像工坊",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 主题切换
if 'theme' not in st.session_state:
    st.session_state.theme = "light"

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

# ===== 修正后的CSS样式（修复所有可见性问题） =====
def apply_theme():
    if st.session_state.theme == "dark":
        bg_color = "#0e141b"
        card_bg = "#1a2330"
        text_color = "#e6edf3"
        accent = "#58a6ff"
        border_color = "#30363d"
    else:
        bg_color = "#f8f9fa"
        card_bg = "#ffffff"
        text_color = "#24292f"
        accent = "#2969ff"
        border_color = "#d1d8e0"

    return f"""
    <style>
        /* 基础样式 */
        .stApp {{
            background: {bg_color};
            color: {text_color};
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}
        
        /* 修复主标题可见性 - 使用纯色文字 */
        .main-header {{
            font-size: 3rem;
            font-weight: 800;
            color: {accent};
            text-align: center;
            margin: 2rem 0 1rem 0;
            padding: 1rem;
            position: relative;
        }}
        
        /* 添加渐变装饰条 */
        .main-header::after {{
            content: '';
            display: block;
            width: 120px;
            height: 4px;
            background: linear-gradient(90deg, {accent} 0%, #36b9ff 100%);
            margin: 0.5rem auto 0;
            border-radius: 2px;
        }}
        
        /* 副标题样式 */
        .subtitle {{
            text-align: center;
            color: gray;
            font-size: 1.2rem;
            margin-bottom: 2rem;
            font-weight: 400;
        }}
        
        /* 图片卡片 */
        .image-card {{
            background: {card_bg};
            border-radius: 0.75rem;
            padding: 1rem;
            margin: 0.5rem;
            border: 1px solid {border_color};
            transition: all 0.3s ease;
            color: {text_color};
        }}
        
        .image-card:hover {{
            border-color: {accent};
            box-shadow: 0 4px 12px rgba(41, 105, 255, 0.15);
        }}
        
        /* 导航卡片 */
        .nav-card {{
            background: {card_bg};
            border-radius: 1rem;
            padding: 1.5rem;
            margin: 0.5rem 0;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 1px solid {border_color};
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            color: {text_color};
        }}
        
        .nav-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(41, 105, 255, 0.2);
            border-color: {accent};
        }}
        
        /* 按钮样式 */
        .stButton>button {{
            background: linear-gradient(90deg, {accent} 0%, #36b9ff 100%);
            color: white;
            border: none;
            border-radius: 0.5rem;
            padding: 0.75rem 2rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(41, 105, 255, 0.3);
        }}
        
        .stButton>button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(41, 105, 255, 0.4);
        }}
        
        /* 信息提示框 */
        .info-box {{
            padding: 1rem 1.5rem;
            border-radius: 0.75rem;
            margin: 1rem 0;
            border-left: 4px solid;
            color: {text_color};
        }}
        
        .info-box.success {{ 
            border-color: #2ecc71; 
            background: rgba(46, 204, 113, 0.1); 
        }}
        .info-box.warning {{ 
            border-color: #f1c40f; 
            background: rgba(241, 196, 15, 0.1); 
        }}
        .info-box.error {{ 
            border-color: #e74c3c; 
            background: rgba(231, 76, 60, 0.1); 
        }}
        
        /* 侧边栏描述文字 */
        .sidebar-desc {{
            font-size: 0.85rem;
            color: gray;
            margin: -0.5rem 0 1rem 0;
            padding: 0 0.5rem;
        }}
        
        /* 移除多余间距 */
        .block-container {{
            padding-top: 1rem;
        }}
        
        /* 确保标题文字可见 */
        h1, h2, h3, h4, h5, h6 {{
            color: {text_color} !important;
        }}
    </style>
    """

st.markdown(apply_theme(), unsafe_allow_html=True)

# ===== 将主题切换按钮移到侧边栏顶部 =====
with st.sidebar:
    st.button(
        "🌓 切换主题",
        on_click=toggle_theme,
        key="theme_toggle",
        help="切换深色/浅色模式"
    )
    st.markdown("---")  # 添加分隔线

# ===== 主标题和副标题（确保可见） =====
st.markdown('<h1 class="main-header">🎨 AI图像工坊</h1>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">智能图像处理工具箱</div>', unsafe_allow_html=True)
st.markdown("---")

# ===== 导航栏 =====
st.sidebar.markdown("## 🔧 功能导航", unsafe_allow_html=True)

# 功能列表
FUNCTIONS = {
    "🏠 首页介绍": "探索AI图像处理的无限可能",
    "🖼️ 照片风格迁移": "将艺术风格应用到你的照片",
    "🧹 照片去噪": "智能移除图像噪声",
    "🔧 图像修复": "修复受损图像区域",
    "✨ 图像生成": "从文本创造图像",
    "🖼️ 背景去除": "一键分离主体与背景"
}

# 渲染导航（按钮+描述）
for i, (func_name, desc) in enumerate(FUNCTIONS.items()):
    if st.sidebar.button(
        func_name,
        key=f"nav_title_{i}",
        use_container_width=True
    ):
        st.session_state.current_function = func_name
    
    st.sidebar.markdown(
        f'<p class="sidebar-desc">{desc}</p>', 
        unsafe_allow_html=True
    )

# 获取当前功能
current_function = st.session_state.get("current_function", "🏠 首页介绍")

# ===== 功能页面渲染函数 =====
def render_home():
    st.markdown("## 🚀 欢迎来到AI图像工坊")
    st.markdown(
        f'<p style="font-size: 1.1rem; line-height: 1.8;">'
        '这是一个集成了多种前沿AI图像处理技术的工具箱，让您的图像处理工作变得简单而强大。'
        '</p>',
        unsafe_allow_html=True
    )
    
    # 使用2列布局展示功能特性
    features = [
        ("🎨 风格迁移", "将梵高的星空风格应用到您的照片"),
        ("✨ 智能去噪", "去除低光照照片的噪点"),
        ("🛠️ 图像修复", "修复老照片的破损区域"),
        ("🤖 AI生成", "将文字描述转化为精美图像"),
        ("🖼️ 背景分离", "自动抠图，精准识别"),
    ]
    
    cols = st.columns(2)
    
    for i, (title, desc) in enumerate(features):
        col_idx = i % 2  # 交替放在两列中
        with cols[col_idx]:
            # 获取当前主题的颜色
            accent_color = "#58a6ff" if st.session_state.theme == "dark" else "#2969ff"
            st.markdown(f"""
            <div class="nav-card" style="text-align: center; padding: 2rem 1rem;">
                <h3 style="color: {accent_color}; margin-bottom: 0.5rem;">{title}</h3>
                <p style="font-size: 0.9rem; color: gray;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown(
        f"""
        <div class="info-box warning">
            <strong>💡 首次使用提示：</strong>
            某些功能首次使用需要加载几分钟时间，请耐心等待。
        </div>
        """,
        unsafe_allow_html=True
    )

def render_style_transfer():
    st.markdown("### 🎨 照片风格迁移")
    st.info("上传内容图片并描述目标风格，AI将智能融合艺术风格")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        content_image = st.file_uploader(
            "上传内容图片", 
            type=["jpg", "jpeg", "png"], 
            key="content",
            help="选择您想要改变风格的照片"
        )
        if content_image:
            content_img = Image.open(content_image)
            content_img = validate_image(content_img)
            content_img = preprocess_image(content_img)
            content_img = resize_image(content_img)
            st.markdown('<div class="image-card">', unsafe_allow_html=True)
            st.image(content_img, caption="📸 内容图片", use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        style_prompt = st.text_input(
            "🎨 风格描述", 
            "impressionist painting style, colorful brush strokes, artistic",
            help="例如：油画风格、水彩画、赛博朋克、复古胶片等"
        )
        strength = st.slider(
            "💪 风格强度", 0.1, 1.0, 0.7, step=0.1,
            help="值越大，风格效果越明显"
        )
        steps = st.slider(
            "⚡ 推理步数", 10, 50, 30, step=5,
            help="步数越多，质量越高但速度越慢"
        )
        guidance = st.slider(
            "🎯 引导强度", 1.0, 20.0, 7.5, step=0.5,
            help="控制生成图像与提示词的匹配程度"
        )
    
    if st.button("🚀 执行风格迁移", use_container_width=True) and content_image:
        with st.spinner("🤖 正在加载模型并处理中..."):
            try:
                progress_bar = st.progress(0)
                from models.style_transfer import StyleTransferModel
                model = StyleTransferModel()
                
                result_img = model.process(
                    content_image=content_img,
                    style_prompt=style_prompt,
                    strength=strength,
                    num_inference_steps=steps,
                    guidance_scale=guidance
                )
                result_img = postprocess_image(result_img)
                progress_bar.progress(100)
                
                st.markdown("---")
                cols = st.columns(2)
                with cols[0]:
                    st.markdown('<div class="image-card">', unsafe_allow_html=True)
                    st.image(content_img, caption="📋 原始图片", use_column_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                with cols[1]:
                    st.markdown('<div class="image-card">', unsafe_allow_html=True)
                    st.image(result_img, caption="✨ 风格化结果", use_column_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                buf = BytesIO()
                result_img.save(buf, format="PNG")
                st.download_button(
                    label="⬇️ 下载结果图片",
                    data=buf.getvalue(),
                    file_name="style_transferred_result.png",
                    mime="image/png",
                    use_container_width=True,
                    key="download_style"
                )
                
                st.success("✅ 风格迁移完成！")
                
            except Exception as e:
                st.error(f"❌ 处理过程中出现错误: {str(e)}")

def render_denoising():
    st.markdown("### 🧹 照片去噪")
    st.info("智能移除图像噪声，恢复清晰细节")
    
    uploaded_file = st.file_uploader(
        "上传图片", 
        type=["jpg", "jpeg", "png"],
        help="支持JPG、PNG格式"
    )
    
    if uploaded_file is not None:
        original_img = Image.open(uploaded_file)
        original_img = validate_image(original_img)
        original_img = preprocess_image(original_img)
        original_img = resize_image(original_img)
        
        noise_factor = st.slider(
            "🔊 噪声强度", 0.05, 0.3, 0.1, step=0.05,
            help="用于演示的噪声强度"
        )
        noisy_img = add_noise(original_img, noise_factor)
        
        algo_options = {
            "bilateral": "保边滤波 - 保留边缘细节",
            "median": "中值滤波 - 适合椒盐噪声",
            "nlm": "非局部均值 - 高质量去噪",
            "gaussian": "高斯模糊 - 简单快速"
        }
        
        denoise_method = st.selectbox(
            "🧪 选择去噪算法",
            options=list(algo_options.keys()),
            format_func=lambda x: f"{x} - {algo_options[x].split(' - ')[1]}",
            help="不同算法适用于不同类型的噪声"
        )
        
        with st.expander("⚙️ 算法参数设置", expanded=True):
            if denoise_method == "bilateral":
                d = st.slider("滤波距离", 1, 20, 9)
                sigma_color = st.slider("颜色相似度", 10, 200, 75)
                sigma_space = st.slider("空间相似度", 10, 200, 75)
                params = {"d": d, "sigma_color": sigma_color, "sigma_space": sigma_space}
            elif denoise_method == "median":
                kernel_size = st.slider("核大小（奇数）", 1, 11, 3, step=2)
                params = {"kernel_size": kernel_size}
            elif denoise_method == "nlm":
                h = st.slider("去噪强度h", 1, 20, 10)
                template_ws = st.slider("模板窗口大小", 3, 15, 7)
                search_ws = st.slider("搜索窗口大小", 10, 30, 21)
                params = {"h": h, "template_window_size": template_ws, "search_window_size": search_ws}
            else:
                kernel_size = st.slider("核大小（奇数）", 1, 15, 5, step=2)
                sigma = st.slider("高斯标准差", 0.1, 5.0, 1.0)
                params = {"kernel_size": kernel_size, "sigma": sigma}
        
        if st.button("🚀 执行去噪", use_container_width=True):
            with st.spinner("🤖 正在去噪处理..."):
                try:
                    progress = st.progress(0)
                    from models.denoising import DenoisingModel
                    model = DenoisingModel()
                    
                    denoised_img = model.process(
                        noisy_image=noisy_img,
                        method=denoise_method,
                        **params
                    )
                    progress.progress(100)
                    
                    st.markdown("---")
                    cols = st.columns(3)
                    with cols[0]:
                        st.markdown('<div class="image-card">', unsafe_allow_html=True)
                        st.image(original_img, caption="🖼️ 原始图片", use_column_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    with cols[1]:
                        st.markdown('<div class="image-card">', unsafe_allow_html=True)
                        st.image(noisy_img, caption="📢 含噪声图片", use_column_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    with cols[2]:
                        st.markdown('<div class="image-card">', unsafe_allow_html=True)
                        st.image(denoised_img, caption="✨ 去噪后", use_column_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    buf = BytesIO()
                    denoised_img.save(buf, format="PNG")
                    st.download_button(
                        label="⬇️ 下载去噪结果",
                        data=buf.getvalue(),
                        file_name="denoised_result.png",
                        mime="image/png",
                        use_container_width=True,
                        key="download_denoise"
                    )
                    
                    st.success("✅ 去噪完成！")
                    
                except Exception as e:
                    st.error(f"❌ 去噪过程中出现错误: {str(e)}")

def render_inpainting():
    st.markdown("### 🔧 图像修复")
    st.info("智能修复图像中的选定区域")
    
    # 上传原图
    image_file = st.file_uploader(
        "上传待修复图片", 
        type=["jpg", "jpeg", "png"], 
        key="repair_image",
        help="选择需要修复的图像"
    )
    
    if image_file:
        original_img = Image.open(image_file)
        original_img = validate_image(original_img)
        
        # 记录原始尺寸
        original_size = original_img.size
        st.info(f"原始图片尺寸: {original_size[0]} × {original_size[1]}")
        
        # 显示原图
        st.markdown('<div class="image-card">', unsafe_allow_html=True)
        st.image(original_img, caption="🖼️ 待修复图片", use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 提供两种掩码方式
        mask_option = st.radio(
            "选择掩码创建方式",
            ["手动绘制掩码", "上传掩码文件"],
            help="选择如何指定修复区域"
        )
        
        if mask_option == "手动绘制掩码":
            try:
                from streamlit_drawable_canvas import st_canvas
                
                # 创建画布用于绘制掩码
                canvas_result = st_canvas(
                    fill_color="rgba(0, 0, 0, 0)",  # 完全透明
                    stroke_width=30,               # 笔刷宽度
                    stroke_color="white",          # 笔刷颜色（白色表示修复区域）
                    background_image=original_img,
                    update_streamlit=True,
                    height=original_img.height,
                    width=original_img.width,
                    drawing_mode="freedraw",
                    key="canvas",
                )
                
                if canvas_result.image_data is not None:
                    import cv2
                    # 将画布数据转换为灰度掩码
                    mask_array = canvas_result.image_data[:, :, 3]  # 获取alpha通道
                    mask_img = Image.fromarray((mask_array > 0).astype(np.uint8) * 255, mode='L')
                    
                    # 确保掩码尺寸与原图一致
                    if mask_img.size != original_size:
                        mask_img = mask_img.resize(original_size, Image.Resampling.NEAREST)
                    
                    # 显示生成的掩码
                    st.markdown('<div class="image-card">', unsafe_allow_html=True)
                    st.image(mask_img, caption="🎯 绘制的修复掩码", use_column_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                else:
                    st.warning("请在画布上绘制需要修复的区域")
                    return
                    
            except ImportError:
                st.error("⚠️ 需要安装 streamlit-drawable-canvas 来支持交互式掩码绘制")
                st.code("pip install streamlit-drawable-canvas", language="bash")
                return
        
        else:  # 上传掩码文件
            mask_file = st.file_uploader(
                "上传掩码图片（白色为修复区域）", 
                type=["jpg", "jpeg", "png"], 
                key="mask_upload",
                help="白色区域表示需要修复的部分"
            )
            
            if not mask_file:
                st.warning("请上传掩码图片")
                return
            
            mask_img = Image.open(mask_file).convert('L')  # 转为灰度
            
            # 验证掩码尺寸并调整
            if mask_img.size != original_size:
                st.warning(f"掩码尺寸 ({mask_img.size}) 与原图尺寸 ({original_size}) 不匹配，已自动调整")
                mask_img = mask_img.resize(original_size, Image.Resampling.NEAREST)
            
            st.markdown('<div class="image-card">', unsafe_allow_html=True)
            st.image(mask_img, caption="🎯 上传的掩码", use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 修复参数
        prompt = st.text_input(
            "📝 修复提示词",
            "seamless repair, natural texture, consistent lighting, high quality",
            help="描述希望修复后的效果"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            steps = st.slider("推理步数", 20, 60, 30, step=10)
        with col2:
            guidance = st.slider("引导强度", 1.0, 15.0, 7.5, step=0.5)
        
        if st.button("🚀 执行修复", use_container_width=True):
            with st.spinner("🤖 正在修复图像..."):
                try:
                    progress = st.progress(0)
                    from models.inpainting import InpaintingModel
                    model = InpaintingModel()
                    
                    # 在这里不需要额外的尺寸调整，因为模型内部会处理
                    result_img = model.process(
                        image=original_img,
                        mask=mask_img,
                        prompt=prompt,
                        num_inference_steps=steps,
                        guidance_scale=guidance
                    )
                    progress.progress(100)
                    
                    # 验证结果尺寸
                    if result_img.size != original_size:
                        st.warning(f"结果尺寸 {result_img.size} 与原始尺寸 {original_size} 不同")
                    
                    st.markdown("---")
                    cols = st.columns(3)
                    with cols[0]:
                        st.markdown('<div class="image-card">', unsafe_allow_html=True)
                        st.image(original_img, caption="🖼️ 原始图片", use_column_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    with cols[1]:
                        st.markdown('<div class="image-card">', unsafe_allow_html=True)
                        st.image(mask_img, caption="🎯 修复掩码", use_column_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    with cols[2]:
                        st.markdown('<div class="image-card">', unsafe_allow_html=True)
                        st.image(result_img, caption="✨ 修复后图片", use_column_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    buf = BytesIO()
                    result_img.save(buf, format="PNG")
                    st.download_button(
                        label="⬇️ 下载修复结果",
                        data=buf.getvalue(),
                        file_name="inpainting_result.png",
                        mime="image/png",
                        use_container_width=True,
                        key="download_inpaint"
                    )
                    
                    st.success("✅ 修复完成！")
                    
                except Exception as e:
                    st.error(f"❌ 修复过程中出现错误: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())

def render_generation():
    st.markdown("### ✨ 图像生成")
    st.info("根据文本描述生成高质量图像")
    
    prompt = st.text_area(
        "📝 图像描述",
        "A beautiful landscape with mountains and lake at sunset, high quality, detailed",
        height=120,
        help="详细描述您想要生成的图像内容"
    )
    
    negative_prompt = st.text_input(
        "🚫 排除内容（可选）",
        "blurry, low quality, bad anatomy, deformed, ugly",
        help="指定不希望出现的元素"
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        num_images = st.slider("生成数量", 1, 4, 1)
        guidance_scale = st.slider("引导强度", 1.0, 20.0, 7.5, step=0.5)
    with col2:
        steps = st.slider("推理步数", 20, 80, 50, step=5)
    with col3:
        width = st.slider("宽度", 256, 1024, 512, step=64)
        height = st.slider("高度", 256, 1024, 512, step=64)
    
    if st.button("🚀 生成图像", use_container_width=True):
        if prompt:
            with st.spinner("🤖 正在生成图像..."):
                try:
                    progress = st.progress(0)
                    from models.generation import GenerationModel
                    model = GenerationModel()
                    progress.progress(20)
                    
                    generated_images = model.process(
                        prompt=prompt,
                        negative_prompt=negative_prompt,
                        num_images=num_images,
                        num_inference_steps=steps,
                        guidance_scale=guidance_scale
                    )
                    progress.progress(100)
                    
                    st.markdown("---")
                    if num_images == 1:
                        st.markdown('<div class="image-card">', unsafe_allow_html=True)
                        st.image(generated_images[0], caption="🎨 生成的图像", use_column_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        cols = st.columns(num_images)
                        for i, img in enumerate(generated_images):
                            with cols[i]:
                                st.markdown('<div class="image-card">', unsafe_allow_html=True)
                                st.image(img, caption=f"🎨 生成图像 {i+1}", use_column_width=True)
                                st.markdown('</div>', unsafe_allow_html=True)
                                buf = BytesIO()
                                img.save(buf, format="PNG")
                                st.download_button(
                                    label=f"⬇️ 下载图像{i+1}",
                                    data=buf.getvalue(),
                                    file_name=f"generated_image_{i+1}.png",
                                    mime="image/png",
                                    use_container_width=True,
                                    key=f"download_gen_{i}"
                                )
                    
                    st.success(f"✅ 成功生成 {num_images} 张图像！")
                    
                except Exception as e:
                    st.error(f"❌ 生成过程中出现错误: {str(e)}")
        else:
            st.warning("⚠️ 请输入图像描述！")

def render_background_removal():
    st.markdown("### 🖼️ 背景去除")
    st.info("自动识别主体并移除背景，支持多种算法")
    
    uploaded_file = st.file_uploader(
        "上传图片", 
        type=["jpg", "jpeg", "png"],
        help="选择需要去除背景的图像"
    )
    
    if uploaded_file is not None:
        original_img = Image.open(uploaded_file).convert("RGB")
        original_img = validate_image(original_img)
        original_img = resize_image(original_img)
        
        method_options = {
            "grabcut": "GrabCut算法 - 精确分割",
            "simple": "简单阈值 - 快速处理",
            "edge": "边缘检测 - 轮廓识别"
        }
        
        method_display = st.radio(
            "🔍 选择处理方法",
            options=list(method_options.keys()),
            format_func=lambda x: method_options[x],
            help="不同算法适用于不同类型的图像"
        )
        
        if st.button("🚀 去除背景", use_container_width=True):
            with st.spinner("🤖 正在处理..."):
                try:
                    progress = st.progress(0)
                    from models.background_removal import BackgroundRemovalModel
                    model = BackgroundRemovalModel()
                    progress.progress(50)
                    
                    result_img = model.process(original_img, method=method_display)
                    progress.progress(100)
                    
                    st.markdown("---")
                    cols = st.columns(2)
                    with cols[0]:
                        st.markdown('<div class="image-card">', unsafe_allow_html=True)
                        st.image(original_img, caption="🖼️ 原始图片", use_column_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    with cols[1]:
                        st.markdown('<div class="image-card">', unsafe_allow_html=True)
                        st.image(result_img, caption="✨ 去除背景后", use_column_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    buf = BytesIO()
                    result_img.save(buf, format="PNG")
                    st.download_button(
                        label="⬇️ 下载背景移除结果",
                        data=buf.getvalue(),
                        file_name="background_removed.png",
                        mime="image/png",
                        use_container_width=True,
                        key="download_bg"
                    )
                    
                    st.success("✅ 背景去除完成！")
                    
                except Exception as e:
                    st.error(f"❌ 背景移除过程中出现错误: {str(e)}")

# ===== 路由渲染 =====
functions_map = {
    "🏠 首页介绍": render_home,
    "🖼️ 照片风格迁移": render_style_transfer,
    "🧹 照片去噪": render_denoising,
    "🔧 图像修复": render_inpainting,
    "✨ 图像生成": render_generation,
    "🖼️ 背景去除": render_background_removal,
}

# 渲染当前选中功能
functions_map[current_function]()

# ===== 页脚 =====
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: gray; padding: 2rem;">
        <p>🛠️ AI图像工坊 v1.0 | 基于Streamlit构建 | 由AI驱动</p>
        <p style="font-size: 0.85rem; margin-top: 0.5rem;">
            所有处理均在本地完成，保障您的隐私安全
        </p>
    </div>
    """,
    unsafe_allow_html=True
)