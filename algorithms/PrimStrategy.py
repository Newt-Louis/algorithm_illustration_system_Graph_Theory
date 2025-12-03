from .IBaseAlgorithmStrategy import IBaseAlgorithmStrategy
import heapq


class PrimStrategy(IBaseAlgorithmStrategy):
    def run(self, graph, start_node):
        steps = []

        # Hàng đợi ưu tiên, lưu các cạnh: (weight, from_node, to_node)
        pq = []

        # Set các đỉnh đã có trong Cây bao trùm (MST = Minimum Spanning Tree)
        nodes_in_mst = set()
        # Thêm đỉnh bắt đầu vào MST
        nodes_in_mst.add(start_node)
        steps.append(('add_node_to_mst', start_node))

        # Thêm tất cả các cạnh kề với đỉnh bắt đầu vào hàng đợi (PQ)
        for neighbor, weight in graph.weighted_edges.get(start_node, {}).items():
            heapq.heappush(pq, (weight, start_node, neighbor))
            # 'explore_edge': Cạnh được đưa vào PQ để xem xét
            steps.append(('explore_edge', start_node, neighbor))

        # Bắt đầu vòng lặp chính
        while pq:
            # Lấy cạnh có trọng số nhỏ nhất ra khỏi PQ
            weight, from_node, to_node = heapq.heappop(pq)

            # 'test_edge': Cạnh đang được kiểm tra
            steps.append(('test_edge', from_node, to_node))

            # Kiểm tra: Nếu đỉnh 'to_node' đã ở trong MST,
            #    cạnh này tạo ra chu trình -> BỎ QUA
            if to_node in nodes_in_mst:
                # 'discard_edge': Cạnh bị loại bỏ
                steps.append(('discard_edge', from_node, to_node))
                continue

            # (THÀNH CÔNG) Nếu 'to_node' là đỉnh mới:
            #    Thêm đỉnh mới vào MST
            nodes_in_mst.add(to_node)
            steps.append(('add_node_to_mst', to_node))
            #    Thêm cạnh này vào MST
            # 'add_edge_to_mst': Cạnh được xác nhận là thuộc MST
            steps.append(('add_edge_to_mst', from_node, to_node))

            # Thêm tất cả các cạnh kề với đỉnh 'to_node' (đỉnh mới)
            #    vào PQ để xem xét, miễn là nó không dẫn đến đỉnh đã ở trong MST
            for neighbor, weight in graph.weighted_edges.get(to_node, {}).items():
                if neighbor not in nodes_in_mst:
                    heapq.heappush(pq, (weight, to_node, neighbor))
                    steps.append(('explore_edge', to_node, neighbor))

        return steps

    def render_step(self, canvas, graph, all_steps, index):
        # Vẽ đồ thị cơ sở (màu xám, có trọng số)
        node_ui, edge_ui, text_ui = self._draw_base_graph(canvas, graph)

        # Tính toán trạng thái TÍCH LŨY đến bước 'index'
        node_colors = {}
        edge_colors = {}
        mst_edges_so_far = set()
        visited = set()
        pq = []
        parent = {}

        for i in range(index + 1):
            step = all_steps[i]
            action = step[0]

            # Logic của Prim
            if action == 'add_node_to_mst':
                # ('add_node_to_mst', node)
                node = step[1]
                node_colors[node] = 'lightgreen'  # Đỉnh đã vào MST
                visited.add(node)

            elif action == 'add_edge_to_mst':
                # ('add_edge_to_mst', from, to)
                edge_key = tuple(sorted((step[1], step[2])))
                edge_colors[edge_key] = 'green'  # Cạnh đã vào MST
                mst_edges_so_far.add(edge_key)
                parent[step[2]] = step[1]

            elif action == 'explore_edge':
                # ('explore_edge', from, to)
                edge_key = tuple(sorted((step[1], step[2])))
                # Chỉ tô màu nếu nó chưa phải là cạnh MST
                if edge_key not in mst_edges_so_far:
                    edge_colors[edge_key] = 'orange'  # Cạnh nằm trong PQ
                    pq.append((step[1], step[2]))

            elif action == 'test_edge':
                # ('test_edge', from, to)
                edge_key = tuple(sorted((step[1], step[2])))
                if edge_key not in mst_edges_so_far:
                    edge_colors[edge_key] = 'red'  # Cạnh đang được kiểm tra

            elif action == 'discard_edge':
                # ('discard_edge', from, to)
                edge_key = tuple(sorted((step[1], step[2])))
                if edge_key not in mst_edges_so_far:
                    edge_colors[edge_key] = 'gray'  # Cạnh bị loại (tạo chu trình)

        # Áp dụng các màu đã tính toán lên canvas
        for node, color in node_colors.items():
            if node in node_ui:
                canvas.itemconfig(node_ui[node], fill=color)

        for edge_key, color in edge_colors.items():
            if edge_key in edge_ui:
                canvas.itemconfig(edge_ui[edge_key], fill=color, width=3)

        canvas.delete("info_text")
        canvas_height = 600
        visited_text = "Visited: " + ", ".join(sorted(visited))
        pq_text = "Priority Queue: " + ", ".join([f"{u}-{v}" for u, v in pq])
        parent_text = "Parent: " + ", ".join([f"{par}→{child}" for child, par in parent.items()])
        mst_text = "MST Edges: " + ", ".join([f"{u}-{v}" for u, v in mst_edges_so_far])

        canvas.create_text(20, canvas_height - 120, anchor="w",
                           text=visited_text, font=("Helvetica", 14, "bold"),
                           fill="blue", tags="info_text")
        canvas.create_text(20, canvas_height - 150, anchor="w",
                           text=pq_text, font=("Helvetica", 14, "bold"),
                           fill="orange", tags="info_text")
        canvas.create_text(20, canvas_height - 180, anchor="w",
                           text=parent_text, font=("Helvetica", 14, "bold"),
                           fill="brown", tags="info_text")
        canvas.create_text(20, canvas_height - 210, anchor="w",
                           text=mst_text, font=("Helvetica", 14, "bold"),
                           fill="green", tags="info_text")

    # noinspection PyMethodMayBeStatic
    def _draw_base_graph(self, canvas, graph):
        canvas.delete("all")
        node_ui = {}
        edge_ui = {}
        text_ui = {}
        node_radius = 20
        default_color = 'lightgray'

        # Dùng dữ liệu có trọng số
        for node, neighbors in graph.weighted_edges.items():
            x1, y1 = graph.weighted_nodes[node]
            for neighbor, weight in neighbors.items():
                key = tuple(sorted((node, neighbor)))
                if key not in edge_ui:
                    x2, y2 = graph.weighted_nodes[neighbor]
                    edge_id = canvas.create_line(
                        x1, y1, x2, y2, fill=default_color, width=2
                    )
                    edge_ui[key] = edge_id

                    # Vẽ trọng số (weight)
                    mid_x = (x1 + x2) / 2
                    mid_y = (y1 + y2) / 2
                    canvas.create_text(
                        mid_x, mid_y,
                        text=str(weight),
                        font=('Arial', 10, 'bold'),
                        fill='blue'
                    )

        # Vẽ các đỉnh (Nodes)
        for node, (x, y) in graph.weighted_nodes.items():
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