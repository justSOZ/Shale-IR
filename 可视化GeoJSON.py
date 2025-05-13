import geopandas as gpd
import matplotlib.pyplot as plt

# 读取GeoJSON文件
file_path = r'D:\APP\2049labeled\test.geojson'
gdf = gpd.read_file(file_path)

# 绘制GeoDataFrame
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, color='blue', edgecolor='black')

# 添加标题
ax.set_title('Visualization of GeoJSON Data')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# 显示图形
plt.show()



