from .IBaseAlgorithmStrategy import IBaseAlgorithmStrategy
from collections import deque

class BFSStrategy(IBaseAlgorithmStrategy):
    def run(self,graph,start_node):
        steps = []  # Danh sách để lưu các bước
        queue = deque([start_node])
        visited = {start_node}

        # ('visit', node, highlight_color)
        steps.append(('visit', start_node, 'orange'))

        while queue:
            current_node = queue.popleft()
            # ('process', node, highlight_color)
            steps.append(('process', current_node, 'gray'))

            for neighbor in graph.edges.get(current_node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    # ('explore', from_node, to_node, highlight_color)
                    steps.append(('explore', current_node, neighbor, 'red'))
                    steps.append(('visit', neighbor, 'orange'))

        steps.append(('finish', None, None))  # Báo hiệu kết thúc
        return steps

    def render_step(self, canvas, graph, all_steps, index):
        # 1. Vẽ đồ thị ban đầu
        node_ui, edge_ui, text_ui = self.draw_base_graph(canvas, graph)

        # 2. Tính toán trạng thái màu sắc/text TÍCH LŨY đến bước 'index'
        node_colors = {}
        edge_colors = {}

        for i in range(index + 1):
            step = all_steps[i]
            action = step[0]

            # 3. "PHIÊN DỊCH" CÁC BƯỚC LOGIC CỦA BFS RA MÀU
            if action == 'visit':
                # ('visit', node)
                node = step[1]
                node_colors[node] = 'orange'  # BFS 'visit' -> màu cam

            elif action == 'process':
                # ('process', node)
                node = step[1]
                node_colors[node] = 'gray'  # BFS 'process' -> màu xám

            elif action == 'explore':
                # ('explore', from_node, to_node)
                edge_key = tuple(sorted((step[1], step[2])))
                edge_colors[edge_key] = 'red'  # BFS 'explore' -> màu đỏ

        # 4. Áp dụng các màu đã tính toán lên canvas
        for node, color in node_colors.items():
            if node in node_ui:
                canvas.itemconfig(node_ui[node], fill=color)

        for edge_key, color in edge_colors.items():
            if edge_key in edge_ui:
                canvas.itemconfig(edge_ui[edge_key], fill=color, width=3)