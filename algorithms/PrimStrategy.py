from .IBaseAlgorithmStrategy import IBaseAlgorithmStrategy
import heapq


class PrimStrategy(IBaseAlgorithmStrategy):
    def run(self, graph, start_node):
        steps = []

        # Hàng đợi ưu tiên, lưu các cạnh: (weight, from_node, to_node)
        pq = []

        # Set các nút đã có trong Cây bao trùm (MST)
        nodes_in_mst = set()
        # 1. Thêm nút bắt đầu vào MST
        nodes_in_mst.add(start_node)
        steps.append(('add_node_to_mst', start_node))

        # 2. Thêm tất cả các cạnh kề với nút bắt đầu vào hàng đợi (PQ)
        for neighbor, weight in graph.weighted_edges.get(start_node, {}).items():
            heapq.heappush(pq, (weight, start_node, neighbor))
            # 'explore_edge': Cạnh được đưa vào PQ để xem xét
            steps.append(('explore_edge', start_node, neighbor))

        # 3. Bắt đầu vòng lặp chính
        while pq:
            # 4. Lấy cạnh có trọng số nhỏ nhất ra khỏi PQ
            weight, from_node, to_node = heapq.heappop(pq)

            # 'test_edge': Cạnh đang được kiểm tra
            steps.append(('test_edge', from_node, to_node))

            # 5. Kiểm tra: Nếu nút 'to_node' đã ở trong MST,
            #    cạnh này tạo ra chu trình -> BỎ QUA
            if to_node in nodes_in_mst:
                # 'discard_edge': Cạnh bị loại bỏ
                steps.append(('discard_edge', from_node, to_node))
                continue

            # 6. (THÀNH CÔNG) Nếu 'to_node' là nút mới:
            #    Thêm nút mới vào MST
            nodes_in_mst.add(to_node)
            steps.append(('add_node_to_mst', to_node))
            #    Thêm cạnh này vào MST
            # 'add_edge_to_mst': Cạnh được xác nhận là thuộc MST
            steps.append(('add_edge_to_mst', from_node, to_node))

            # 7. Thêm tất cả các cạnh kề với nút 'to_node' (nút mới)
            #    vào PQ để xem xét, miễn là nó không dẫn đến nút đã ở trong MST
            for neighbor, weight in graph.weighted_edges.get(to_node, {}).items():
                if neighbor not in nodes_in_mst:
                    heapq.heappush(pq, (weight, to_node, neighbor))
                    steps.append(('explore_edge', to_node, neighbor))

        return steps

    def render_step(self, canvas, graph, all_steps, index):
        # 1. Vẽ đồ thị cơ sở (màu xám, có trọng số)
        node_ui, edge_ui, text_ui = self._draw_base_graph(canvas, graph)

        # 2. Tính toán trạng thái TÍCH LŨY đến bước 'index'
        node_colors = {}
        edge_colors = {}
        # Dùng set này để theo dõi các cạnh đã vào MST
        mst_edges_so_far = set()

        for i in range(index + 1):
            step = all_steps[i]
            action = step[0]

            # 3. "PHIÊN DỊCH" CÁC BƯỚC LOGIC CỦA PRIM

            if action == 'add_node_to_mst':
                # ('add_node_to_mst', node)
                node = step[1]
                node_colors[node] = 'lightgreen'  # Nút đã vào MST

            elif action == 'add_edge_to_mst':
                # ('add_edge_to_mst', from, to)
                edge_key = tuple(sorted((step[1], step[2])))
                edge_colors[edge_key] = 'green'  # Cạnh đã vào MST
                mst_edges_so_far.add(edge_key)

            elif action == 'explore_edge':
                # ('explore_edge', from, to)
                edge_key = tuple(sorted((step[1], step[2])))
                # Chỉ tô màu nếu nó chưa phải là cạnh MST
                if edge_key not in mst_edges_so_far:
                    edge_colors[edge_key] = 'orange'  # Cạnh nằm trong PQ

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

        # Dùng dữ liệu CÓ trọng số
        for node, neighbors in graph.weighted_edges.items():
            x1, y1 = graph.nodes[node]
            for neighbor, weight in neighbors.items():
                key = tuple(sorted((node, neighbor)))
                if key not in edge_ui:
                    x2, y2 = graph.nodes[neighbor]
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

        # Vẽ các nút (Nodes)
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