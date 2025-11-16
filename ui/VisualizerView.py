# ui/VisualizerView.py
import tkinter as tk
from core.Graph import Graph


class VisualizerView(tk.Frame):
    def __init__(self, parent, controller, strategy):
        super().__init__(parent)
        self.controller = controller
        self.strategy = strategy  # Đối tượng chiến lược (vd: BFSStrategy)

        # --- Dữ liệu Logic ---
        self.graph = Graph()  # Tải đồ thị mẫu

        # *** CHẠY THUẬT TOÁN NGAY LẬP TỨC ***
        # Lấy TẤT CẢ các bước 1 lần
        self.all_steps = self.strategy.run(self.graph, 'A')  # Chạy từ nút 'A'

        self.current_step_index = 0
        self.is_auto_running = False
        self.auto_run_delay_ms = 500  # 0.5 giây/bước

        # --- Biến UI (để lưu các đối tượng canvas) ---
        self.node_ui = {}  # Map 'A' -> ID hình tròn
        self.edge_ui = {}  # Map ('A', 'B') -> ID đường thẳng
        self.text_ui = {}  # Map 'A' -> ID text

        # --- Bố cục Giao diện ---
        self.setup_ui()

        # --- Vẽ trạng thái ban đầu ---
        self.render_step_at(self.current_step_index)

    def setup_ui(self):
        """Hàm này tạo các khung và nút bấm."""

        # 1. Khung trên cùng (Quay lại, Tiêu đề)
        top_frame = tk.Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        back_button = tk.Button(top_frame, text="< Quay lại Menu",
                                command=self.on_back)
        back_button.pack(side=tk.LEFT)

        self.step_label = tk.Label(top_frame, text="Bước: 0 / 0", font=("Arial", 12))
        self.step_label.pack(side=tk.LEFT, padx=20)

        # 2. Canvas (ở giữa)
        self.canvas = tk.Canvas(self, bg="white", highlightthickness=1,
                                highlightbackground="black")
        self.canvas.pack(fill="both", expand=True, padx=10, pady=5)

        # 3. Khung điều khiển dưới cùng
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        # Căn giữa các nút
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

    def on_back(self):
        """Quay lại menu chính."""
        self.is_auto_running = False  # Dừng mọi vòng lặp
        self.controller.show_main_menu()

    def on_next(self):
        """Đi tới 1 bước."""
        if self.current_step_index < len(self.all_steps) - 1:
            self.current_step_index += 1
            self.render_step_at(self.current_step_index)

    def on_prev(self):
        """Lùi lại 1 bước."""
        if self.current_step_index > 0:
            self.current_step_index -= 1
            self.render_step_at(self.current_step_index)

    def on_play_pause(self):
        """Bắt đầu hoặc tạm dừng chạy tự động."""
        self.is_auto_running = not self.is_auto_running
        if self.is_auto_running:
            self.play_pause_button.config(text="⏸ Pause")
            # Nếu đang ở cuối, reset lại từ đầu
            if self.current_step_index == len(self.all_steps) - 1:
                self.current_step_index = 0
            self.auto_run_loop()
        else:
            self.play_pause_button.config(text="▶ Play")

    def on_stop(self):
        """Dừng và reset về bước 0."""
        self.is_auto_running = False
        self.play_pause_button.config(text="▶ Play")
        self.current_step_index = 0
        self.render_step_at(self.current_step_index)

    def auto_run_loop(self):
        """Vòng lặp tự động chạy."""
        if not self.is_auto_running:
            return  # Dừng lại nếu nhấn Pause

        self.on_next()

        # Tự dừng khi đến bước cuối
        if self.current_step_index == len(self.all_steps) - 1:
            self.is_auto_running = False
            self.play_pause_button.config(text="▶ Play")
            self.update_button_states()
            return

        # Lên lịch để chạy bước tiếp theo
        self.after(self.auto_run_delay_ms, self.auto_run_loop)

    def render_step_at(self, step_index):
        """
        Hàm quan trọng: Vẽ lại TOÀN BỘ trạng thái của đồ thị
        tại một bước (step_index) cụ thể.
        """

        # 1. Vẽ lại đồ thị cơ bản (màu xám)
        self.draw_base_graph()

        # 2. Tạo một dictionary 'trạng thái'
        #    để lưu màu cuối cùng của từng nút/cạnh
        node_colors = {}
        edge_colors = {}

        # 3. Lặp qua TẤT CẢ các bước từ 0 đến bước hiện tại
        #    để tính toán trạng thái cuối cùng
        for i in range(step_index + 1):
            step = self.all_steps[i]
            action = step[0]

            if action == 'visit' or action == 'process':
                # ('visit', node_name, color)
                node_colors[step[1]] = step[2]
            elif action == 'explore':
                # ('explore', from_node, to_node, color)
                # Xử lý key (A,B) hay (B,A) đều được
                edge_key = tuple(sorted((step[1], step[2])))
                edge_colors[edge_key] = step[2]

        # 4. Áp dụng các màu đã tính toán vào canvas
        for node, color in node_colors.items():
            if node in self.node_ui:
                self.canvas.itemconfig(self.node_ui[node], fill=color)

        for edge_key, color in edge_colors.items():
            if edge_key in self.edge_ui:
                self.canvas.itemconfig(self.edge_ui[edge_key], fill=color, width=3)

        # 5. Cập nhật giao diện
        self.update_button_states()

    def draw_base_graph(self):
        """Vẽ đồ thị ở trạng thái mặc định (màu xám)."""
        self.canvas.delete("all")  # Xóa mọi thứ
        self.node_ui = {}
        self.edge_ui = {}
        self.text_ui = {}

        node_radius = 20
        default_color = 'lightgray'

        # Vẽ các cạnh (Edges) trước
        for node, neighbors in self.graph.edges.items():
            x1, y1 = self.graph.nodes[node]
            for neighbor in neighbors:
                key = tuple(sorted((node, neighbor)))  # (A,B)
                if key not in self.edge_ui:
                    x2, y2 = self.graph.nodes[neighbor]
                    edge_id = self.canvas.create_line(
                        x1, y1, x2, y2, fill=default_color, width=2
                    )
                    self.edge_ui[key] = edge_id

        # Vẽ các nút (Nodes)
        for node, (x, y) in self.graph.nodes.items():
            oval_id = self.canvas.create_oval(
                x - node_radius, y - node_radius,
                x + node_radius, y + node_radius,
                fill=default_color, outline='black', width=2
            )
            text_id = self.canvas.create_text(x, y, text=node,
                                              font=('Arial', 12, 'bold'))
            self.node_ui[node] = oval_id
            self.text_ui[node] = text_id

    def update_button_states(self):
        """Cập nhật trạng thái (Enable/Disable) của các nút."""
        # Vô hiệu hóa Prev ở bước 0
        self.prev_button.config(
            state=tk.DISABLED if self.current_step_index == 0 else tk.NORMAL)

        # Vô hiệu hóa Next ở bước cuối
        self.next_button.config(
            state=tk.DISABLED if self.current_step_index == len(self.all_steps) - 1 else tk.NORMAL)

        # Cập nhật nhãn đếm bước
        self.step_label.config(
            text=f"Bước: {self.current_step_index} / {len(self.all_steps) - 1}")

        # Tắt các nút khác khi đang auto-run
        if self.is_auto_running:
            self.prev_button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)
        else:
            self.stop_button.config(state=tk.NORMAL)