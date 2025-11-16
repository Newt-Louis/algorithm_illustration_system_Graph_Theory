from abc import ABC, abstractmethod

class IBaseAlgorithmStrategy(ABC):
    @abstractmethod
    def run(self,graph,start_node):
        pass

    @abstractmethod
    def render_step(self, canvas, graph, all_steps, index):
        pass

    def draw_base_graph(self, canvas, graph):
        canvas.delete("all")  # Xóa mọi thứ

        node_ui = {}
        edge_ui = {}
        text_ui = {}

        node_radius = 20
        default_color = 'lightgray'

        # Vẽ các cạnh (Edges) trước
        for node, neighbors in graph.edges.items():
            x1, y1 = graph.nodes[node]
            for neighbor in neighbors:
                key = tuple(sorted((node, neighbor)))  # (A,B)
                if key not in edge_ui:
                    x2, y2 = graph.nodes[neighbor]
                    edge_id = canvas.create_line(
                        x1, y1, x2, y2, fill=default_color, width=2
                    )
                    edge_ui[key] = edge_id

        # Vẽ các nút (Nodes)
        for node, (x, y) in graph.nodes.items():
            oval_id = canvas.create_oval(
                x - node_radius, y - node_radius,
                x + node_radius, y + node_radius,
                fill=default_color, outline='black', width=2
            )
            # Tạo text, ban đầu chỉ có tên nút
            text_id = canvas.create_text(x, y, text=node,
                                         font=('Arial', 12, 'bold'))
            node_ui[node] = oval_id
            text_ui[node] = text_id

        return node_ui, edge_ui, text_ui