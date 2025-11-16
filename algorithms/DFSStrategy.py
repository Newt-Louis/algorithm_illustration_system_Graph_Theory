from algorithms.IBaseAlgorithmStrategy import IBaseAlgorithmStrategy
from collections import deque

class DFSStrategy(IBaseAlgorithmStrategy):
    def run(self,graph,start_node):
        steps = []
        visited = set()
        self._dfs_recursive(graph, start_node, visited, steps)
        return steps

    def _dfs_recursive(self, graph, current_node, visited, steps):
        # 1. Đánh dấu nút là đã thăm (visit)
        visited.add(current_node)
        # Thêm bước 'visit' (sẽ được tô màu cam)
        steps.append(('visit', current_node))

        # 2. Khám phá (explore) các hàng xóm
        for neighbor in graph.unweighted_edges.get(current_node, []):
            if neighbor not in visited:
                # Thêm bước 'explore' (cạnh sẽ được tô màu đỏ)
                steps.append(('explore', current_node, neighbor))
                # Gọi đệ quy
                self._dfs_recursive(graph, neighbor, visited, steps)

        # 3. Sau khi đã thăm xong tất cả các nhánh con,
        #    đánh dấu nút này là đã xử lý xong (process)
        # Thêm bước 'process' (sẽ được tô màu xám)
        steps.append(('process', current_node))

    def render_step(self, canvas, graph, all_steps, index):
        # 1. Vẽ đồ thị cơ sở (màu xám)
        node_ui, edge_ui, text_ui = self._draw_base_graph(canvas, graph)

        # 2. Tính toán trạng thái màu sắc TÍCH LŨY đến bước 'index'
        node_colors = {}
        edge_colors = {}

        for i in range(index + 1):
            step = all_steps[i]
            action = step[0]

            # 3. "PHIÊN DỊCH" CÁC BƯỚC LOGIC CỦA DFS RA MÀU
            if action == 'visit':
                # ('visit', node)
                node = step[1]
                node_colors[node] = 'orange'  # DFS 'visit' -> màu cam

            elif action == 'process':
                # ('process', node)
                node = step[1]
                node_colors[node] = 'gray'  # DFS 'process' -> màu xám

            elif action == 'explore':
                # ('explore', from_node, to_node)
                edge_key = tuple(sorted((step[1], step[2])))
                edge_colors[edge_key] = 'red'  # DFS 'explore' -> màu đỏ

        # 4. Áp dụng các màu đã tính toán lên canvas
        for node, color in node_colors.items():
            if node in node_ui:
                canvas.itemconfig(node_ui[node], fill=color)

        for edge_key, color in edge_colors.items():
            if edge_key in edge_ui:
                canvas.itemconfig(edge_ui[edge_key], fill=color, width=3)

    # noinspection PyMethodMayBeStatic
    def _draw_base_graph(self, canvas, graph):
        canvas.delete("all")
        node_ui = {}
        edge_ui = {}
        text_ui = {}
        node_radius = 20
        default_color = 'lightgray'

        for node, neighbors in graph.unweighted_edges.items():
            x1, y1 = graph.nodes[node]
            for neighbor in neighbors:
                key = tuple(sorted((node, neighbor)))
                if key not in edge_ui:
                    x2, y2 = graph.nodes[neighbor]
                    edge_id = canvas.create_line(
                        x1, y1, x2, y2, fill=default_color, width=2
                    )
                    edge_ui[key] = edge_id

        for node, (x, y) in graph.nodes.items():
            oval_id = canvas.create_oval(
                x - node_radius, y - node_radius,
                x + node_radius, y + node_radius,
                fill=default_color, outline='black', width=2
            )
            text_id = canvas.create_text(x, y, text=node,
                                         font=('Arial', 12, 'bold'))
            node_ui[node] = oval_id
            text_ui[node] = text_id

        return node_ui, edge_ui, text_ui