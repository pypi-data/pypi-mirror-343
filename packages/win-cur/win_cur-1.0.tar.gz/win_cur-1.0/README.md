# win-cur
支持.cur文件读写, 系统光标设置 (.cur 或 .ani)\
Support .cur file read/write, system cursor settings(.cur or .ani).

不支持压缩模式图标\
Not support compressed icon.

例子:\
Samples:

```python
from PIL import Image  # 不是依赖库 Not a dependent library

from win_cur.cursor import Cursor

cur = Cursor()
# 必须为RGBA模式 Must be RGBA mode
image = Image.open("sample.png").convert("RGBA")
# 添加热点(鼠标指针中心)为2, 2的光标进入文件
# Add a cursor enter the file, hotspot=(2, 2)
cur.add_cursor(image.width, image.height, 2, 2, image.tobytes())
cur.save_file("sample.cur")
```