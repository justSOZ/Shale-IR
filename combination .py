from PIL import Image, ImageFile
import os

# 解除PIL的图像大小限制
Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True

# 图片所在的目录
image_directory = r'D:\APP\17'

# 检查目录是否存在
if not os.path.exists(image_directory):
    print(f"Directory {image_directory} does not exist.")
else:
    # 获取所有图片文件名，并按列和行排序
    images_files = []
    for file in os.listdir(image_directory):
        if file.endswith('.jpg'):
            parts = file.split('_')
            if len(parts) == 2 and parts[0].isdigit() and parts[1].endswith('.jpg') and parts[1][:-4].isdigit():
                col = int(parts[0])
                row = int(parts[1][:-4])
                images_files.append((col, row, file))

    # 打印找到的文件数量
    print(f"Number of valid image files found: {len(images_files)}")

    if not images_files:
        print("No valid image files found in the directory.")
    else:
        images_files.sort(key=lambda x: (x[0], x[1]))

        # 假设每个小图的尺寸相同，先打开第一张图获取尺寸
        first_image_path = os.path.join(image_directory, images_files[0][2])
        with Image.open(first_image_path) as img:
            width, height = img.size

        # 创建一个空白的大图来存放所有的图片
        merged_width = 70 * width
        merged_height = 70 * height

        # 打印合并后的大图像的尺寸
        print(f"Merged Image Dimensions: {merged_width}x{merged_height}")

        # 创建一个新的空白图像用于存储合并后的结果
        merged_image = Image.new('RGB', (merged_width, merged_height))

        # 遍历所有小图像并将它们粘贴到大图像上
        for col, row, filename in images_files:
            image_path = os.path.join(image_directory, filename)
            with Image.open(image_path) as img:
                paste_box = (
                    col * width,
                    row * height,
                    (col + 1) * width,
                    (row + 1) * height
                )
                merged_image.paste(img, paste_box)

        # 保存合并后的图像为TIFF格式
        merged_image.save(os.path.join(image_directory, 'merged_image.tiff'), format='TIFF')
        print("Merged image saved as merged_image.tiff")



