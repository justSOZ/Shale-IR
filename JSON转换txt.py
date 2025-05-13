import geojson
from shapely.geometry import shape, Polygon
import os


def polygon_to_yolo_boxes(polygon, img_w, img_h, tolerance=4):
    """将单个多边形转换为多个YOLO格式标注框"""
    bounds = polygon.bounds  # (minx, miny, maxx, maxy)
    boxes = []

    # 创建网格并筛选有效区域
    for x in range(int(bounds[0]), int(bounds[2]), tolerance):
        for y in range(int(bounds[1]), int(bounds[3]), tolerance):
            rect = Polygon([(x, y), (x + tolerance, y),
                            (x + tolerance, y + tolerance), (x, y + tolerance)])

            if polygon.contains(rect):
                # 计算归一化坐标（保留6位小数）
                xc = round((x + tolerance / 2) / img_w, 6)
                yc = round((y + tolerance / 2) / img_h, 6)
                w = round(tolerance / img_w, 6)
                h = round(tolerance / img_h, 6)

                # 确保坐标在有效范围
                if all(0 <= coord <= 1 for coord in [xc, yc, w, h]):
                    boxes.append([0, xc, yc, w, h])  # 类别ID=0（pore）

    return boxes


def convert_geojson_to_yolo(geojson_path, output_dir, img_size=(4096, 4096)):
    """主转换函数"""
    with open(geojson_path, 'r', encoding='utf-8') as f:
        gj = geojson.load(f)

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 按图像ID聚合标注
    annotations = {}
    for feature in gj['features']:
        geom = shape(feature['geometry'])
        if isinstance(geom, Polygon):
            # 从属性中提取图像ID（需根据实际数据结构调整）
            image_id = feature['properties'].get('image_id', 'default')

            # 转换当前多边形
            boxes = polygon_to_yolo_boxes(geom, img_size[0], img_size[1])

            # 聚合标注
            if image_id in annotations:
                annotations[image_id].extend(boxes)
            else:
                annotations[image_id] = boxes

    # 写入文件（每个图像一个txt文件）
    for image_id, boxes in annotations.items():
        txt_path = os.path.join(output_dir, f"{image_id}.txt")
        with open(txt_path, 'w', encoding='utf-8') as f:
            for box in boxes:
                f.write(' '.join(map(str, box)) + '\n')  # 每行一个标注


# 执行转换
convert_geojson_to_yolo(
    geojson_path=r'D:\APP\2049labeled\test.geojson',
    output_dir=r'D:\APP\2049labeled\labels'
)