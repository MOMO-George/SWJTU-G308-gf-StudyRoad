import cv2
import numpy as np
import os


def rotate_image(image, angle):
    """旋转图像并返回无黑边偏移的结果"""
    h, w = image.shape[:2]
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))
    M[0, 2] += (new_w / 2) - center[0]
    M[1, 2] += (new_h / 2) - center[1]
    rotated = cv2.warpAffine(image, M, (new_w, new_h))
    return rotated


def colorize_image(image, color='red'):
    """将图像非白/黑区域涂红或涂蓝"""
    # 提取白/黑区域（允许±20的阈值偏差）
    white_low, white_high = 235, 255
    white_mask = (image[:, :, 0] >= white_low) & (image[:, :, 0] <= white_high) \
                 & (image[:, :, 1] >= white_low) & (image[:, :, 1] <= white_high) \
                 & (image[:, :, 2] >= white_low) & (image[:, :, 2] <= white_high)
    black_low, black_high = 0, 20
    black_mask = (image[:, :, 0] >= black_low) & (image[:, :, 0] <= black_high) \
                 & (image[:, :, 1] >= black_low) & (image[:, :, 1] <= black_high) \
                 & (image[:, :, 2] >= black_low) & (image[:, :, 2] <= black_high)
    combined_mask = np.logical_or(white_mask, black_mask).astype(np.uint8) * 255

    # 创建颜色背景
    if color == 'red':
        color_bg = np.zeros_like(image)
        color_bg[:, :, 2] = 255  # 红色通道设为255
    elif color == 'blue':
        color_bg = np.zeros_like(image)
        color_bg[:, :, 0] = 255  # 蓝色通道设为255
    else:
        return image  # 颜色无效时返回原图

    # 合并：白/黑区域保留原图，其余区域显示指定颜色
    result = np.where(combined_mask[:, :, np.newaxis] == 255, image, color_bg)
    return result


def process_rotations_and_colorize(source_dir, target_dir, rotations=4, color='red'):
    """处理图像：旋转+涂红/涂蓝"""
    os.makedirs(target_dir, exist_ok=True)
    for root, _, files in os.walk(source_dir):
        for file in files:
            if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
            img_path = os.path.join(root, file)
            img = cv2.imread(img_path)
            if img is None:
                print(f"无法读取: {img_path}")
                continue
            name, ext = os.path.splitext(file)
            current_img = img.copy()
            for i in range(rotations):
                angle = -90 * (i + 1)
                rotated_img = rotate_image(current_img, angle)
                # 执行涂红/涂蓝
                colorized_img = colorize_image(rotated_img, color=color)
                # 保存结果
                save_name = f"{name}_{i + 1}_{color}{ext}"
                save_path = os.path.join(target_dir, save_name)
                cv2.imwrite(save_path, colorized_img)
                current_img = rotated_img
            print(f"处理完成: {file}")


if __name__ == '__main__':
    # 示例：先涂红再涂蓝（可分别调用）
    process_rotations_and_colorize(
        source_dir='img',
        target_dir='img2',
        rotations=1,
        color='red'
    )
    process_rotations_and_colorize(
        source_dir='img',
        target_dir='img2',
        rotations=1,
        color='blue'
    )