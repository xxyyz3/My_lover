import os
import sys
from PIL import Image

if len(sys.argv) < 2:
    print("用法: python replace_mai_image.py <图片路径>")
    print("例如: python replace_mai_image.py \"C:\\Users\\33684\\Desktop\\樱岛麻衣.jpg\"")
    sys.exit(1)

source_path = sys.argv[1]

if not os.path.exists(source_path):
    print(f"错误: 文件不存在 - {source_path}")
    sys.exit(1)

try:
    img = Image.open(source_path)
    print(f"原始图片信息:")
    print(f"  格式: {img.format}")
    print(f"  尺寸: {img.size}")
    print(f"  模式: {img.mode}")
    
    save_dir = os.path.join(os.path.dirname(__file__), "avatars")
    save_path = os.path.join(save_dir, "樱岛麻衣_avatar.png")
    
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    
    img.save(save_path, format='PNG')
    print(f"\n图片已保存到: {save_path}")
    
    saved_img = Image.open(save_path)
    print(f"保存后信息:")
    print(f"  格式: {saved_img.format}")
    print(f"  尺寸: {saved_img.size}")
    
    print("\n✓ 替换成功！请重启Streamlit应用查看效果。")
    
except Exception as e:
    print(f"错误: {e}")
    sys.exit(1)