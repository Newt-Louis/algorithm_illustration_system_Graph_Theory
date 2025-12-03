from .IBaseAlgorithmStrategy import IBaseAlgorithmStrategy


class KruskalStrategy(IBaseAlgorithmStrategy):

    def _find(self, parent_map, node):
        """Hàm 'Find' (Tìm): Tìm đỉnh đại diện cho tập hợp chứa 'node'."""
        if parent_map[node] == node:
            return node
        # Đệ quy tìm gốc
        return self._find(parent_map, parent_map[node])

    def _union(self, parent_map, node1, node2):
        """Hàm 'Union' (Gộp): Gộp hai tập hợp chứa 'node1' và 'node2'."""
        root1 = self._find(parent_map, node1)
        root2 = self._find(parent_map, node2)
        if root1 != root2:
            parent_map[root2] = root1  # Gộp tập 2 vào tập 1
            return True
        return False  # Trả về False nếu chúng đã cùng 1 tập (tạo chu trình)

    def run(self, graph, start_node):
        steps = []

        # Tạo một danh sách TẤT CẢ các cạnh: (weight, from, to)
        all_edges = []
        for node, neighbors in graph.weighted_edges.items():
            for neighbor, weight in neighbors.items():
                # Thêm cạnh 1 lần duy nhất (ví dụ A-B, không thêm B-A)
                if node < neighbor:
                    all_edges.append((weight, node, neighbor))

        # Sắp xếp tất cả các cạnh theo trọng số (weight) tăng dần
        all_edges.sort()

        # Khởi tạo cấu trúc Union-Find
        # Ban đầu, mỗi đỉnh là 'cha' của chính nó (mỗi đỉnh là 1 tập riêng)
        parent_map = {node: node for node in graph.weighted_nodes}

        # Duyệt qua các cạnh đã sắp xếp
        for weight, node1, node2 in all_edges:
            # Cạnh đang được xét
            steps.append(('test_edge', node1, node2))
            # Dùng Union-Find để kiểm tra chu trình
            # Gộp 2 tập chứa node1 và node2.
            # Nếu chúng đã ở chung 1 tập, _union sẽ trả về False.
            if self._union(parent_map, node1, node2):
                # ('add_edge_to_mst', from, to)
                steps.append(('add_edge_to_mst', node1, node2))
                # ('add_node_to_mst', node)
                steps.append(('add_node_to_mst', node1))
                steps.append(('add_node_to_mst', node2))
            else:
                # ('discard_edge', from, to)
                steps.append(('discard_edge', node1, node2))

        return steps

    def render_step(self, canvas, graph, all_steps, index):
        # Vẽ đồ thị cơ sở (màu xám, có trọng số)
        node_ui, edge_ui, text_ui = self._draw_base_graph(canvas, graph)

        # Tính toán trạng thái TÍCH LŨY đến bước 'index'
        node_colors = {}
        edge_colors = {}
        mst_edges_so_far = set()  # Dùng set này để theo dõi các cạnh đã vào MST
        parent_map = {node: node for node in graph.weighted_nodes}  # Union-Find parent
        edge_list = [] # danh sách cạnh

        # Hàm find để dựng lại tập hợp
        def find(node):
            while parent_map[node] != node:
                node = parent_map[node]
            return node

        for i in range(index + 1):
            step = all_steps[i]
            action = step[0]

            # CÁC BƯỚC LOGIC CỦA KRUSKAL
            if action == 'add_node_to_mst':
                # ('add_node_to_mst', node)
                node = step[1]
                node_colors[node] = 'lightgreen'  # đỉnh đã vào MST

            elif action == 'add_edge_to_mst':
                # ('add_edge_to_mst', from, to)
                edge_key = tuple(sorted((step[1], step[2])))
                edge_colors[edge_key] = 'green'  # Cạnh đã vào MST
                mst_edges_so_far.add(edge_key)
                root1, root2 = find(step[1]), find(step[2])
                if root1 != root2:
                    parent_map[root2] = root1

            elif action == 'test_edge':
                # ('test_edge', from, to)
                edge_key = tuple(sorted((step[1], step[2])))
                edge_list.append(edge_key)
                if edge_key not in mst_edges_so_far:
                    edge_colors[edge_key] = 'red'  # Cạnh đang được kiểm tra

            elif action == 'discard_edge':
                # ('discard_edge', from, to)
                edge_key = tuple(sorted((step[1], step[2])))
                edge_list.append(edge_key)
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
        edge_list_text = "Edge List: " + ", ".join([f"{u}-{v}" for u, v in edge_list])
        parent_text = "Parent: " + ", ".join([f"{par}→{node}" for node, par in parent_map.items()])
        # dựng lại các tập hợp từ parent_map
        sets = {}
        for node in parent_map:
            root = find(node)
            sets.setdefault(root, []).append(node)
        sets_text = "Sets: " + ", ".join(["{" + ",".join(sorted(members)) + "}" for members in sets.values()])
        mst_text = "MST Edges: " + ", ".join([f"{u}-{v}" for u, v in mst_edges_so_far])

        canvas.create_text(20, canvas_height-120, anchor="w",
                           text=edge_list_text, font=("Helvetica", 14, "bold"),
                           fill="orange", tags="info_text")
        canvas.create_text(20, canvas_height-150, anchor="w",
                           text=sets_text, font=("Helvetica", 14, "bold"),
                           fill="blue", tags="info_text")
        canvas.create_text(20, canvas_height-180, anchor="w",
                           text=parent_text, font=("Helvetica", 14, "bold"),
                           fill="brown", tags="info_text")
        canvas.create_text(20, canvas_height-210, anchor="w",
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

        # Dùng dữ liệu CÓ trọng số
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