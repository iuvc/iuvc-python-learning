import os
from PIL import Image

def merge_images_with_spacing(images, direction='horizontal', background_color=(255, 255, 255), spacing=10):
    if not images:
        raise ValueError("图片列表为空。")

    direction = direction.lower()
    if direction not in ('horizontal', 'vertical'):
        raise ValueError("无效的拼接方向。")

    # 获取所有图片的宽高信息
    image_sizes = [Image.open(image_path).size for image_path in images]

    # 计算带间隔的图片大小
    if direction == 'horizontal':
        total_width = sum(image_size[0] for image_size in image_sizes) + spacing * (len(images) - 1)
        max_height = max(image_sizes, key=lambda x: x[1])[1]
        total_height = max_height
    else:
        total_height = sum(image_size[1] for image_size in image_sizes) + spacing * (len(images) - 1)
        max_width = max(image_sizes, key=lambda x: x[0])[0]
        total_width = max_width

    # 计算缩放比例并更新大小
    scaled_sizes = []
    for width, height in image_sizes:
        if direction == 'horizontal':
            scale_factor = max_height / height
            scaled_sizes.append((int(width * scale_factor), max_height))
        else:
            scale_factor = max_width / width
            scaled_sizes.append((max_width, int(height * scale_factor)))

    # 创建带间隔的最终拼接图像对象
    merged_image = Image.new('RGB', (total_width, total_height), background_color)

    # 将图片按顺序拼接到最终图像上
    x_offset, y_offset = 0, 0
    for index, image_path in enumerate(images):
        image = Image.open(image_path)
        scaled_width, scaled_height = scaled_sizes[index]

        if direction == 'horizontal':
            scaled_image = image.resize((scaled_width, max_height))
            merged_image.paste(scaled_image, (x_offset, y_offset))
            x_offset += scaled_width + spacing
        else:
            scaled_image = image.resize((max_width, scaled_height))
            merged_image.paste(scaled_image, (x_offset, y_offset))
            y_offset += scaled_height + spacing

    # 重新计算拼接后的图像的总宽度和总高度
    if direction == 'horizontal':
        total_width = x_offset - spacing
    else:
        total_height = y_offset - spacing

    # 重新创建最终拼接图像，确保不会裁剪最后一张图
    merged_image = Image.new('RGB', (total_width, total_height), background_color)

    # 将图片按顺序拼接到最终图像上
    x_offset, y_offset = 0, 0
    for index, image_path in enumerate(images):
        image = Image.open(image_path)
        scaled_width, scaled_height = scaled_sizes[index]

        if direction == 'horizontal':
            scaled_image = image.resize((scaled_width, max_height))
            merged_image.paste(scaled_image, (x_offset, y_offset))
            x_offset += scaled_width + spacing
        else:
            scaled_image = image.resize((max_width, scaled_height))
            merged_image.paste(scaled_image, (x_offset, y_offset))
            y_offset += scaled_height + spacing

    return merged_image

  
def get_image_list(folder_path, allowed_formats=['jpg', 'png']):
    """
    获取指定文件夹中的图片列表

    参数：
    folder_path: 字符串，目标文件夹路径
    allowed_formats: 可选，一个包含允许的图片格式的列表，默认为['jpg', 'png']

    返回：
    返回包含图片文件路径的列表
    """
    image_list = []

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)

        # 确保文件是一个文件而不是目录，并且是允许的图片格式
        if os.path.isfile(file_path) and file.lower().endswith(tuple(allowed_formats)):
            image_list.append(file_path)

    return image_list


def create_image(file_path, export_name, direction='horizontal', background_color=(255, 255, 255), spacing=10):
    folder_path = file_path  # 替换为你的目标文件夹路径
    allowed_formats = ['jpg', 'png']
    image_paths = get_image_list(folder_path, allowed_formats)
    result_image = merge_images_with_spacing(image_paths, direction, background_color, spacing)
    result_image.save(export_name+'.png')

### 参数1，文件夹路径
### 参数2，导出文件名
### 参数3，拼接方向：'horizontal'横向, 'vertical'竖向
create_image('./img', 'result_v', 'vertical')
