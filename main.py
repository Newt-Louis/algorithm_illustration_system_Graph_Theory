import tkinter as tk
from collections import deque


# --- 1. PHẦN LOGIC (MODEL) ---
# (Không thay đổi gì so với code sườn trước)
class Graph:
    def __init__(self):
        # self.nodes chứa tọa độ (x, y) để GUI biết vẽ ở đâu
        self.nodes = {
            'A': (50, 50),
            'B': (150, 50),
            'C': (50, 150),
            'D': (150, 150),
            'E': (250, 150),
            'F': (250, 50)
        }
        # self.edges là danh sách kề
        self.edges = {
            'A': ['B', 'C'],
            'B': ['A', 'D', 'F'],
            'C': ['A', 'D'],
            'D': ['B', 'C', 'E'],
            'E': ['D', 'F'],
            'F': ['B', 'E']
        }

    def bfs(self, start_node):
        queue = deque([start_node])
        visited = {start_node}
        yield ('visit', start_node)
        while queue:
            current_node = queue.popleft()
            yield ('process', current_node)
            for neighbor in self.edges.get(current_node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    yield ('explore', current_node, neighbor)
                    yield ('visit', neighbor)


# --- 2. PHẦN GIAO DIỆN (VIEW/CONTROLLER) ---
class GraphVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Minh họa Thuật toán Đồ thị")

        self.graph = Graph()
        self.node_ui = {}
        self.edge_ui = {}
        self.steps_generator = None

        # --- BIẾN MỚI CHO TÍNH NĂNG TỰ ĐỘNG CHẠY ---
        self.is_auto_running = False
        self.auto_run_delay_ms = 500  # 500ms = 0.5 giây mỗi bước

        # --- Tạo các thành phần GUI ---
        control_frame = tk.Frame(root)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        self.bfs_button = tk.Button(control_frame, text="Chạy BFS (từ A)", command=self.start_bfs)
        self.bfs_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.next_step_button = tk.Button(control_frame, text="Bước tiếp theo", command=self.next_step,
                                          state=tk.DISABLED)
        self.next_step_button.pack(side=tk.LEFT, padx=5, pady=5)

        # --- NÚT MỚI ---
        self.auto_run_button = tk.Button(control_frame, text="Tự động chạy", command=self.toggle_auto_run,
                                         state=tk.DISABLED)
        self.auto_run_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.reset_button = tk.Button(control_frame, text="Reset", command=self.reset_graph)
        self.reset_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.canvas = tk.Canvas(root, width=400, height=300, bg='white')
        self.canvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.draw_graph()

    def draw_graph(self):
        # (Không thay đổi gì so với code sườn trước)
        self.canvas.delete("all")
        self.node_ui = {}
        self.edge_ui = {}
        node_radius = 20
        for node, neighbors in self.graph.edges.items():
            x1, y1 = self.graph.nodes[node]
            for neighbor in neighbors:
                if (neighbor, node) not in self.edge_ui:
                    x2, y2 = self.graph.nodes[neighbor]
                    edge_id = self.canvas.create_line(x1, y1, x2, y2, fill='black', width=2)
                    self.edge_ui[(node, neighbor)] = edge_id
        for node, (x, y) in self.graph.nodes.items():
            oval_id = self.canvas.create_oval(
                x - node_radius, y - node_radius,
                x + node_radius, y + node_radius,
                fill='lightblue', outline='black', width=2
            )
            text_id = self.canvas.create_text(x, y, text=node, font=('Arial', 12, 'bold'))
            self.node_ui[node] = oval_id

    def start_bfs(self):
        self.reset_graph()
        self.steps_generator = self.graph.bfs(start_node='A')

        # Cập nhật trạng thái các nút
        self.bfs_button.config(state=tk.DISABLED)
        self.next_step_button.config(state=tk.NORMAL)
        self.auto_run_button.config(state=tk.NORMAL)  # Kích hoạt nút tự động chạy

        # Tự động chạy bước đầu tiên (tô màu nút 'A')
        self.next_step()

    def next_step(self):
        """Thực thi MỘT bước của thuật toán."""
        if not self.steps_generator:
            return

        try:
            step = next(self.steps_generator)
            self.visualize_step(step)
        except StopIteration:
            # Thuật toán đã chạy xong
            print("BFS hoàn thành!")
            self.finish_algorithm()  # Gọi hàm dọn dẹp mới

    def visualize_step(self, step):
        # (Không thay đổi gì so với code sườn trước)
        action = step[0]
        if action == 'visit':
            node = step[1]
            print(f"Thăm: {node}")
            self.canvas.itemconfig(self.node_ui[node], fill='orange')
        elif action == 'process':
            node = step[1]
            print(f"Đang xử lý: {node}")
            self.canvas.itemconfig(self.node_ui[node], fill='gray')
        elif action == 'explore':
            from_node, to_node = step[1], step[2]
            print(f"Khám phá: {from_node} -> {to_node}")
            edge_id = self.edge_ui.get((from_node, to_node)) or self.edge_ui.get((to_node, from_node))
            if edge_id:
                self.canvas.itemconfig(edge_id, fill='red', width=3)

    def reset_graph(self):
        """Vẽ lại đồ thị và reset các trạng thái."""
        print("--- Reset đồ thị ---")

        # --- DỪNG VÒNG LẶP TỰ ĐỘNG ---
        self.is_auto_running = False

        self.draw_graph()
        self.bfs_button.config(state=tk.NORMAL)
        self.next_step_button.config(state=tk.DISABLED)
        self.auto_run_button.config(state=tk.DISABLED, text="Tự động chạy")
        self.steps_generator = None

    def finish_algorithm(self):
        """Dọn dẹp khi thuật toán chạy xong."""
        self.is_auto_running = False
        self.steps_generator = None
        self.next_step_button.config(state=tk.DISABLED)
        self.auto_run_button.config(state=tk.DISABLED, text="Tự động chạy")
        self.bfs_button.config(state=tk.NORMAL)  # Cho phép chạy lại

    # --- HÀM MỚI QUAN TRỌNG ---
    def toggle_auto_run(self):
        """Bật/Tắt chế độ tự động chạy."""
        self.is_auto_running = not self.is_auto_running

        if self.is_auto_running:
            self.auto_run_button.config(text="Tạm dừng")
            self.next_step_button.config(state=tk.DISABLED)  # Tắt nút 'Next' khi đang auto
            self.auto_run_loop()  # Bắt đầu vòng lặp
        else:
            self.auto_run_button.config(text="Tự động chạy")
            self.next_step_button.config(state=tk.NORMAL)  # Bật lại nút 'Next'

    def auto_run_loop(self):
        """Vòng lặp chính cho việc tự động chạy."""
        # Điều kiện dừng: 1. Người dùng nhấn Tạm dừng (is_auto_running = False)
        #                 2. Thuật toán đã chạy xong (steps_generator = None)
        if not self.is_auto_running or self.steps_generator is None:
            return

            # 1. Thực thi một bước
        self.next_step()

        # 2. Lên lịch để chạy bước tiếp theo sau một khoảng delay
        #    Kiểm tra lại self.steps_generator vì next_step() có thể đã
        #    set nó = None nếu thuật toán vừa kết thúc.
        if self.is_auto_running and self.steps_generator is not None:
            self.root.after(self.auto_run_delay_ms, self.auto_run_loop)
        elif self.steps_generator is None:
            # Thuật toán vừa kết thúc trong lần gọi next_step() ở trên
            # self.finish_algorithm() đã được gọi bên trong next_step()
            pass


# --- 3. PHẦN KHỞI CHẠY (MAIN) ---
if __name__ == "__main__":
    root = tk.Tk()
    app = GraphVisualizer(root)
    root.mainloop()