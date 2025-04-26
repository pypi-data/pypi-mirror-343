import os
import random
import tkinter

from PIL import Image, ImageTk


class EasyPicture:
    def __init__(self, window, img_dir, size=(350, 350), side=tkinter.RIGHT, expand=False, fill=tkinter.NONE,
                 padx=0, pady=0, layout="pack", row=0, column=0, rowspan=1, columnspan=1,
                 img_exts=('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
        self._window = window
        self._img_dir = img_dir
        self._size = size
        self._img_exts = img_exts

        # 获取图片文件
        img_files = [f for f in os.listdir(self._img_dir) if f.lower().endswith(self._img_exts)]
        if not img_files:
            raise FileNotFoundError(f"No image files found in {self._img_dir} with extensions {self._img_exts}")
        img_path = os.path.join(self._img_dir, random.choice(img_files))

        # 加载图片
        img = Image.open(img_path).resize(self._size, Image.LANCZOS)
        self._photo = ImageTk.PhotoImage(img)  # 必须保存为实例属性

        # 创建Label
        self._label = tkinter.Label(self._window, image=self._photo)

        # 布局
        if layout == "grid":
            self._label.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky="nsew",
                             padx=padx, pady=pady)
        else:
            self._label.pack(side=side, expand=expand, fill=fill, padx=padx, pady=pady)

    def get_label(self):
        return self._label
