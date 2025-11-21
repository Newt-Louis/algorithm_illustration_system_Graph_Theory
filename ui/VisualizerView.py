import tkinter as tk
from core.Graph import Graph
from algorithms.IBaseAlgorithmStrategy import IBaseAlgorithmStrategy


class VisualizerView(tk.Frame):
    def __init__(self, parent, controller, strategy: IBaseAlgorithmStrategy):
        super().__init__(parent)
        self.controller = controller
        self.strategy = strategy  # Đối tượng chiến lược

        # --- Dữ liệu Logic ---
        self.graph = Graph()  # Tải đồ thị mẫu
        self.all_steps = self.strategy.run(self.graph, 'A')  # Chạy logic 1 lần

        self.current_step_index = 0
        self.is_auto_running = False
        self.auto_run_delay_ms = 500

        self.setup_ui()

        # --- Vẽ trạng thái ban đầu (bước 0) ---
        self.render_current_step()

    def setup_ui(self):
        top_frame = tk.Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        back_button = tk.Button(top_frame, text="< Quay lại Menu",
                                command=self.on_back)
        back_button.pack(side=tk.LEFT)

        self.step_label = tk.Label(top_frame, text="Bước: 0 / 0", font=("Arial", 12))
        self.step_label.pack(side=tk.LEFT, padx=20)

        self.canvas = tk.Canvas(self, bg="white", highlightthickness=1,
                                highlightbackground="black")
        self.canvas.pack(fill="both", expand=True, padx=10, pady=5)

        bottom_frame = tk.Frame(self)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        button_container = tk.Frame(bottom_frame)
        button_container.pack()

        self.prev_button = tk.Button(button_container, text="<< Prev",
                                     command=self.on_prev)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.play_pause_button = tk.Button(button_container, text="▶ Play",
                                           command=self.on_play_pause, width=8)
        self.play_pause_button.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(button_container, text="Next >>",
                                     command=self.on_next)
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(button_container, text="⏹ Stop (Reset)",
                                     command=self.on_stop)
        self.stop_button.pack(side=tk.LEFT, padx=5)

    def render_current_step(self):
        if not self.all_steps:
            return

        # Yêu cầu strategy class vẽ
        self.strategy.render_step(
            self.canvas,
            self.graph,
            self.all_steps,
            self.current_step_index
        )

        # Cập nhật trạng thái nút (Prev/Next) và nhãn đếm
        self.update_button_states()

    def on_back(self):
        self.is_auto_running = False
        self.controller.show_main_menu()

    def on_next(self):
        if self.current_step_index < len(self.all_steps) - 1:
            self.current_step_index += 1
            self.render_current_step()

    def on_prev(self):
        if self.current_step_index > 0:
            self.current_step_index -= 1
            self.render_current_step()

    def on_play_pause(self):
        self.is_auto_running = not self.is_auto_running
        if self.is_auto_running:
            self.play_pause_button.config(text="⏸ Pause")
            if self.current_step_index == len(self.all_steps) - 1:
                self.current_step_index = 0
                self.render_current_step()
            self.auto_run_loop()
        else:
            self.play_pause_button.config(text="▶ Play")

    def on_stop(self):
        self.is_auto_running = False
        self.play_pause_button.config(text="▶ Play")
        self.current_step_index = 0
        self.render_current_step()

    def auto_run_loop(self):
        if not self.is_auto_running:
            return

        if self.current_step_index >= len(self.all_steps) - 1:
            self.is_auto_running = False
            self.play_pause_button.config(text="▶ Play")
            self.update_button_states()
            return

        self.on_next()

        if self.is_auto_running:
            self.after(self.auto_run_delay_ms, self.auto_run_loop)

    def update_button_states(self):
        if not self.all_steps:
            total_steps = 0
        else:
            total_steps = len(self.all_steps) - 1

        # Vô hiệu hóa Prev ở bước 0
        self.prev_button.config(
            state=tk.DISABLED if self.current_step_index == 0 else tk.NORMAL)

        # Vô hiệu hóa Next ở bước cuối
        self.next_button.config(
            state=tk.DISABLED if self.current_step_index >= total_steps else tk.NORMAL)

        self.step_label.config(
            text=f"Bước: {self.current_step_index} / {total_steps}")

        if self.is_auto_running:
            self.prev_button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)
        else:
            self.stop_button.config(state=tk.NORMAL)