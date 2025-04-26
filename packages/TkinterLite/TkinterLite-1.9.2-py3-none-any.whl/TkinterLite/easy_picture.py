import os
import tkinter

from PIL import Image, ImageTk


class EasyPicture:
    def __init__(self, window, img_path, size=(350, 350), side=tkinter.RIGHT, expand=False, fill=tkinter.NONE,
                 padx=0, pady=0, layout="pack", row=0, column=0, rowspan=1, columnspan=1):
        self._window = window
        self._img_path = img_path
        self._size = size

        if not os.path.isfile(self._img_path):
            raise FileNotFoundError(f"Image file not found: {self._img_path}")

        # 加载图片
        img = Image.open(self._img_path).resize(self._size, Image.LANCZOS)
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
