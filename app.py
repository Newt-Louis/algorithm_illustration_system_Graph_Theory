import tkinter as tk
from ui.MainMenuView import MainMenuView
from ui.VisualizerView import VisualizerView
from algorithms.BFSStrategy import BFSStrategy


# from algorithms.dfs_strategy import DFSStrategy # (Khi bạn thêm sau)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Minh họa Thuật toán Đồ thị")
        self.geometry("800x600")

        # Lưu trữ frame đang hiển thị
        self._current_view = None

        # Đăng ký tất cả các chiến lược thuật toán của bạn
        # Key: tên hiển thị, Value: LỚP chiến lược
        self.strategies = {
            "BFS": BFSStrategy,
            # "DFS": DFSStrategy, # (Khi bạn thêm sau)
            # "Dijkstra": DijkstraStrategy,
        }

        # Bắt đầu bằng cách hiển thị menu chính
        self.show_main_menu()

    def show_main_menu(self):
        """Dọn dẹp view cũ và hiển thị menu chính."""
        if self._current_view:
            self._current_view.destroy()  # Hủy frame cũ

        # 'self' (App) chính là 'parent' và cũng là 'controller'
        self._current_view = MainMenuView(self, self)
        self._current_view.pack(fill="both", expand=True)

    def show_visualizer(self, strategy_name):
        """Dọn dẹp menu và hiển thị trang minh họa."""
        if self._current_view:
            self._current_view.destroy()

        # Lấy LỚP chiến lược từ tên
        StrategyClass = self.strategies.get(strategy_name)

        if StrategyClass:
            # Khởi tạo một đối tượng chiến lược mới
            strategy_instance = StrategyClass()

            self._current_view = VisualizerView(self, self, strategy_instance)
            self._current_view.pack(fill="both", expand=True)
        else:
            print(f"Lỗi: Không tìm thấy chiến lược '{strategy_name}'")
            self.show_main_menu()  # Quay lại menu nếu có lỗi