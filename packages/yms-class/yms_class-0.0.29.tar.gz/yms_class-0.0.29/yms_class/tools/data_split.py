import os
import shutil

# 配置路径（需根据实际情况修改）
source_folder = r'D:\Code\deep-learning-code\classification\data\VibrationData1'  # 源文件夹
target_base = r"D:\Code\deep-learning-code\classification\dataset\VibrationData1"  # 分类结果保存的根目录（需包含上面创建的4个文件夹）

# 定义分类区间
categories = {
    "1-H1": (0, 249),
    "1-H2": (250, 499),
    "1-H3": (500, 749),
    "1-H4": (750, 999)
}

# 遍历源文件夹中的文件
for filename in os.listdir(source_folder):
    if not filename.endswith("_resized.jpg"):
        continue  # 跳过不符合命名规则的文件

    # 提取第一个数字（假设文件名格式为 "数字_数字_resized.png"）
    first_num = filename.split("_")[0]
    if not first_num.isdigit():
        continue  # 确保第一个部分是数字
    first_num = int(first_num)

    # 判断所属分类
    category = None
    for cat, (start, end) in categories.items():
        if start <= first_num <= end:
            category = cat
            break

    if category:
        target_folder = os.path.join(target_base, category)
        # 创建目标文件夹（如果不存在）
        os.makedirs(target_folder, exist_ok=True)
        # 移动文件
        source_path = os.path.join(source_folder, filename)
        target_path = os.path.join(target_folder, filename)
        shutil.move(source_path, target_path)
        print(f"已移动 {filename} 到 {category}")
    else:
        print(f"跳过不符合区间的文件：{filename}")

print("分类完成！")

# import os
# from pathlib import Path
#
# # 配置参数（需根据实际情况修改）
# source_folder = r"D:\Code\deep-learning-code\output\VibrationData1"  # 例如："D:/images"
# image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')  # 支持的图片扩展名（大小写敏感）
#
#
# def rename_images_in_subfolders():
#     for subfolder in Path(source_folder).glob('**/*'):
#         if not subfolder.is_dir():  # 跳过非文件夹
#             continue
#
#         # 获取子文件夹内的所有图片文件（保留扩展名大小写）
#         image_files = [f for f in subfolder.iterdir()
#                        if f.is_file() and f.suffix.lower() in image_extensions]
#
#         if not image_files:  # 无子图片文件则跳过
#             continue
#
#         # 按文件名排序（可根据需求改为按修改时间排序：key=lambda x: x.stat().st_mtime）
#         image_files.sort(key=lambda x: x.name)
#
#         # 生成新文件名：子文件夹名_序号.扩展名
#         subfolder_name = subfolder.name
#         for idx, file in enumerate(image_files, start=1):
#             new_filename = f"{subfolder_name}_{idx}{file.suffix}"
#             new_filepath = subfolder / new_filename
#
#             # 避免覆盖已有文件（可取消注释以启用）
#             # if new_filepath.exists():
#             #     print(f"警告：文件 {new_filename} 已存在，跳过")
#             #     continue
#
#             # 重命名文件
#             file.rename(new_filepath)
#             print(f"重命名：{file.name} → {new_filename}")
#
#
# rename_images_in_subfolders()
# print("重命名完成！")

