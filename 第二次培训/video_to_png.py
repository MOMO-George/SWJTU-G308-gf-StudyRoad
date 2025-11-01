import cv2
import os

class video_image:
    def __init__(self, video_path,output_folder):
        self.video_path = video_path
        self.output_folder = output_folder

    def video_to_frames(self, prefix='frame'):
        """
        将视频转换为序列图片

        参数:
            video_path (str): 视频文件路径
            output_folder (str): 输出图片的文件夹路径
            prefix (str): 输出图片的前缀名
        """
        # 创建输出文件夹（如果不存在）
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
            print(f"创建文件夹: {self.output_folder}")

        # 读取视频文件
        cap = cv2.VideoCapture(self.video_path)

        # 检查视频是否成功打开
        if not cap.isOpened():
            print(f"错误：无法打开视频文件 {self.video_path}")
            return

        frame_count = 0
        saved_count = 0

        print("开始提取视频帧...")

        while True:
            # 逐帧读取视频
            ret, frame = cap.read()

            # 如果读取失败（可能是视频结束），退出循环
            if not ret:
                print("视频帧读取完毕或读取失败。")
                break

            # 构造输出图片的文件名和路径
            frame_filename = f"{prefix}_{frame_count:06d}.jpg"
            output_path = os.path.join(self.output_folder, frame_filename)

            # 保存帧为图片文件
            success = cv2.imwrite(output_path, frame)

            if success:
                saved_count += 1
                if saved_count % 100 == 0:  # 每保存100帧打印一次进度
                    print(f"已保存 {saved_count} 帧...")
            else:
                print(f"保存失败: {output_path}")

            frame_count += 1

        # 释放视频捕获对象
        cap.release()
        print(f"处理完成！成功保存 {saved_count} 张图片到 {self.output_folder}")


    def extract_frames_by_time(self, interval_seconds=1):
        """
        按时间间隔抽取视频帧

        参数:
            video_path (str): 视频文件路径
            output_folder (str): 输出图片的文件夹路径
            interval_seconds (float): 抽帧时间间隔（秒）
        """
        cap = cv2.VideoCapture(self.video_path)

        if not cap.isOpened():
            print(f"错误：无法打开视频文件 {self.video_path}")
            return

        # 获取视频帧率
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(f"视频帧率: {fps} FPS")

        # 计算要跳过的帧数
        skip_frames = int(fps * interval_seconds)

        frame_count = 0
        saved_count = 0

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            # 按间隔抽帧
            if frame_count % skip_frames == 0:
                frame_filename = f"frame_{saved_count:06d}.jpg"
                output_path = os.path.join(self.output_folder, frame_filename)
                cv2.imwrite(output_path, frame)
                saved_count += 1

            frame_count += 1

        cap.release()
        print(f"按 {interval_seconds} 秒间隔抽帧完成，共保存 {saved_count} 张图片")


    def extract_frames_uniformly(self, num_frames):
        """
        从视频中均匀抽取指定数量的帧

        参数:
            video_path (str): 视频文件路径
            output_folder (str): 输出图片的文件夹路径
            num_frames (int): 要抽取的帧数量
        """
        cap = cv2.VideoCapture(self.video_path)

        if not cap.isOpened():
            print(f"错误：无法打开视频文件 {self.video_path}")
            return

        # 获取视频总帧数
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(f"视频总帧数: {total_frames}")

        # 计算抽帧间隔
        frame_interval = max(1, total_frames // num_frames)

        frame_count = 0
        saved_count = 0

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            # 按间隔抽帧
            if frame_count % frame_interval == 0 and saved_count < num_frames:
                frame_filename = f"frame_{saved_count:06d}.jpg"
                output_path = os.path.join(self.output_folder, frame_filename)
                cv2.imwrite(output_path, frame)
                saved_count += 1

            frame_count += 1

        cap.release()
        print(f"均匀抽帧完成，共保存 {saved_count} 张图片")


    def video_to_frames_with_progress(self):
        """带进度显示的视频转图片函数"""
        cap = cv2.VideoCapture(self.video_path)

        if not cap.isOpened():
            print(f"错误：无法打开视频文件 {self.video_path}")
            return

        # 获取视频总帧数
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(f"视频总帧数: {total_frames}")

        frame_count = 0
        saved_count = 0

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            # 保存帧为图片
            frame_filename = f"frame_{frame_count:06d}.jpg"
            output_path = os.path.join(self.output_folder, frame_filename)
            cv2.imwrite(output_path, frame)
            saved_count += 1

            # 显示进度
            if frame_count % 100 == 0:
                progress = (frame_count / total_frames) * 100
                print(f"处理进度: {progress:.2f}% ({frame_count}/{total_frames})")

            frame_count += 1

        cap.release()
        print(f"处理完成！成功保存 {saved_count} 张图片")


# 使用示例
if __name__ == "__main__":
    video_path = "video/video_20251030_125916.mp4"  # 替换为你的视频路径
    output_folder = "img2"  # 输出文件夹名称

    #video_to_frames(video_path, output_folder)
    #extract_frames_by_time(video_path, output_folder, interval_seconds=0.5)
    img = video_image(video_path, output_folder)
    img.video_to_frames_with_progress()