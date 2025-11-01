import cv2
import numpy as np
import os

def rotate_image(image, angle):
    """旋转图像并返回无黑边偏移的结果"""
    # 获取图像尺寸
    h, w = image.shape[:2]
    # 计算旋转中心
    center = (w / 2, h / 2)
    # 获取旋转矩阵
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    # 计算旋转后图像的新边界
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))
    # 调整旋转矩阵以防止偏移
    M[0, 2] += (new_w / 2) - center[0]
    M[1, 2] += (new_h / 2) - center[1]
    # 执行旋转
    rotated = cv2.warpAffine(image, M, (new_w, new_h))
    return rotated

def process_rotations(source_dir, target_dir, rotations=4):
    """处理所有图像，每次旋转90度，共旋转指定次数"""
    os.makedirs(target_dir, exist_ok=True)
    for root, _, files in os.walk(source_dir):
        for file in files:
            if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
            # 读取原图
            img_path = os.path.join(root, file)
            img = cv2.imread(img_path)
            if img is None:
                print(f"无法读取: {img_path}")
                continue
            # 分离文件名和后缀
            name, ext = os.path.splitext(file)
            current_img = img.copy()
            # 执行多次旋转
            for i in range(rotations):
                angle = -90 * (i + 1)  # 每次顺时针旋转90度
                rotated_img = rotate_image(current_img, angle)
                # 保存结果
                save_name = f"{name}_{i+1}{ext}"
                save_path = os.path.join(target_dir, save_name)
                cv2.imwrite(save_path, rotated_img)
                # 更新当前图像为旋转后的结果
                current_img = rotated_img
            print(f"处理完成: {file}")

if __name__ == '__main__':
    process_rotations(
        source_dir='img',   # 源图像文件夹
        target_dir='img2',  # 保存结果的文件夹
        rotations=3         # 旋转4次
    )