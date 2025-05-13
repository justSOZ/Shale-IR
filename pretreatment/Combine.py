import os
from PIL import Image


def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if basename.endswith(pattern):
                yield os.path.join(root, basename)


def main():
    # input_dir = r'D:\APP\3861.9'
    input_dir = r'D:\APP\2049.5'

    output_dir = r'D:\APP\result2049'
    file_pattern = '.jpg'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Find all jpg files and parse their coordinates
    image_paths = list(find_files(input_dir, file_pattern))
    images = {}

    for path in image_paths:
        filename = os.path.basename(path)
        name, _ = os.path.splitext(filename)
        x, y = map(int, name.split('_'))
        images[(x, y)] = path

    min_x = min(images.keys(), key=lambda k: k[0])[0]
    max_x = max(images.keys(), key=lambda k: k[0])[0]
    min_y = min(images.keys(), key=lambda k: k[1])[1]
    max_y = max(images.keys(), key=lambda k: k[1])[1]

    inner_min_x = min_x + 1
    inner_max_x = max_x - 1
    inner_min_y = min_y + 1
    inner_max_y = max_y - 1

    # tile_size = 15
    tile_size = 4

    def process_tile(start_x, start_y):
        tile_images = []
        for dy in range(tile_size):
            row = []
            for dx in range(tile_size):
                x = start_x + dx
                y = start_y + dy
                if (x, y) in images:
                    img = Image.open(images[(x, y)])
                    row.append(img)
                else:
                    row.append(None)
            tile_images.append(row)

        return tile_images

    num_tiles_x = (inner_max_x - inner_min_x + 1) // tile_size
    num_tiles_y = (inner_max_y - inner_min_y + 1) // tile_size


    exit = 0

    for tx in range(num_tiles_x):
        for ty in range(num_tiles_y):
            start_x = inner_min_x + tx * tile_size
            start_y = inner_min_y + ty * tile_size

            tile_images = process_tile(start_x, start_y)

            if any(any(img is None for img in row) for row in tile_images):
                continue

            first_img = tile_images[0][0]
            width, height = first_img.size
            result_image = Image.new('RGB', (width * tile_size, height * tile_size))

            for row_idx, row in enumerate(tile_images):
                for col_idx, img in enumerate(row):
                    position = (col_idx * width, row_idx * height)
                    result_image.paste(img, position)

            output_path = os.path.join(output_dir, f'tile_{start_x}_{start_y}.tiff')
            result_image.save(output_path, format='TIFF')
            print(f'Saved {output_path}')
            exit += 1
            if exit == 9:
                exit(0)

    print("Processing complete.")


if __name__ == "__main__":
    main()



