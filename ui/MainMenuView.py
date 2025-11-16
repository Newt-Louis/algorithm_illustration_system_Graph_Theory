import tkinter as tk
from tkinter import font as tkFont

class MainMenuView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller # 'controller' là App (root)

        # Tiêu đề
        title_font = tkFont.Font(family='Helvetica', size=24, weight='bold')
        label = tk.Label(self, text="Chọn Thuật Toán", font=title_font)
        label.pack(pady=40, padx=20)

        # Khung chứa các nút
        button_frame = tk.Frame(self)
        button_frame.pack()

        # Lấy danh sách tên thuật toán từ controller
        button_font = tkFont.Font(family='Helvetica', size=14)
        for strategy_name in self.controller.strategies.keys():
            # Tạo nút cho mỗi thuật toán
            button = tk.Button(
                button_frame,
                text=strategy_name,
                font=button_font,
                width=20,
                height=2,
                # 'lambda' rất quan trọng để truyền đúng tên
                command=lambda name=strategy_name:
                    self.controller.show_visualizer(name)
            )
            button.pack(pady=10)