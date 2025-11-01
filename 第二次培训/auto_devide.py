# 将图片和标注数据按比例切分为 训练集和测试集
import shutil
import random
import os
import argparse

class auto_devide:
    def __init__(self,image_dir,txt_dir,save_dir):
        self.image_dir = image_dir
        self.txt_dir = txt_dir
        self.save_dir = save_dir


    # 检查文件夹是否存在
    def mkdir(self,path):
        if not os.path.exists(path):
            os.makedirs(path)


    def devide(self):
        # 创建文件夹
        self.mkdir(self.save_dir)
        images_dir = os.path.join(self.save_dir, 'images')
        labels_dir = os.path.join(self.save_dir, 'labels')

        img_train_path = os.path.join(images_dir, 'train')
        img_test_path = os.path.join(images_dir, 'test')
        img_val_path = os.path.join(images_dir, 'val')

        label_train_path = os.path.join(labels_dir, 'train')
        label_test_path = os.path.join(labels_dir, 'test')
        label_val_path = os.path.join(labels_dir, 'val')

        self.mkdir(images_dir)
        self.mkdir(labels_dir)
        self.mkdir(img_train_path)
        self.mkdir(img_test_path)
        self.mkdir(img_val_path)
        self.mkdir(label_train_path)
        self.mkdir(label_test_path)
        self.mkdir(label_val_path)

        # 数据集划分比例，训练集70%，验证集15%，测试集15%，按需修改
        train_percent = 0.80
        val_percent = 0.10
        test_percent = 0.10

        total_txt = os.listdir(self.txt_dir)
        num_txt = len(total_txt)
        list_all_txt = range(num_txt)  # 范围 range(0, num)

        num_train = int(num_txt * train_percent)
        num_val = int(num_txt * val_percent)
        num_test = num_txt - num_train - num_val

        train = random.sample(list_all_txt, num_train)
        # 在全部数据集中取出train
        val_test = [i for i in list_all_txt if not i in train]
        # 再从val_test取出num_val个元素，val_test剩下的元素就是test
        val = random.sample(val_test, num_val)

        print("训练集数目：{}, 验证集数目：{},测试集数目：{}".format(len(train), len(val), len(val_test) - len(val)))
        for i in list_all_txt:
            name = total_txt[i][:-4]

            srcImage = os.path.join(self.image_dir, name + '.png')
            srcLabel = os.path.join(self.txt_dir, name + '.txt')

            if i in train:
                dst_train_Image = os.path.join(img_train_path, name + '.png')
                dst_train_Label = os.path.join(label_train_path, name + '.txt')
                shutil.copyfile(srcImage, dst_train_Image)
                shutil.copyfile(srcLabel, dst_train_Label)
            elif i in val:
                dst_val_Image = os.path.join(img_val_path, name + '.png')
                dst_val_Label = os.path.join(label_val_path, name + '.txt')
                shutil.copyfile(srcImage, dst_val_Image)
                shutil.copyfile(srcLabel, dst_val_Label)
            else:
                dst_test_Image = os.path.join(img_test_path, name + '.png')
                dst_test_Label = os.path.join(label_test_path, name + '.txt')
                shutil.copyfile(srcImage, dst_test_Image)
                shutil.copyfile(srcLabel, dst_test_Label)


if __name__ == '__main__':
    """
    python split_datasets.py --image-dir my_datasets/color_rings/imgs --txt-dir my_datasets/color_rings/txts --save-dir my_datasets/color_rings/train_data
    """
    parser = argparse.ArgumentParser(description='split datasets to train,val,test params')
    parser.add_argument('--image-dir', type=str, default=r'img2',
                        help='image path dir')
    parser.add_argument('--txt-dir', type=str, default=r'txt',
                        help='txt path dir')
    parser.add_argument('--save-dir', default=r'data', type=str,
                        help='save dir')
    args = parser.parse_args()
    image_dir = args.image_dir
    txt_dir = args.txt_dir
    save_dir = args.save_dir

    train = auto_devide(image_dir, txt_dir, save_dir)
    train.devide()
