from .IBaseAlgorithmStrategy import IBaseAlgorithmStrategy
import heapq

class DijkstraStrategy(IBaseAlgorithmStrategy):
    def run(self, graph, start_node):
        steps = []
        distances = {node: float('inf') for node in graph.dijkstra_nodes}
        parent = {}
        pq = []
        visited = set()
        distances[start_node] = 0
        heapq.heappush(pq, (0, start_node))
        steps.append(('update_distance', start_node, 0, None))

        while pq:
            current_distance, current_node = heapq.heappop(pq)
            if current_distance > distances[current_node]:
                continue
            if current_node in visited:
                continue
            visited.add(current_node)
            steps.append(('visit', current_node))

            for neighbor, weight in graph.dijkstra_weighted_edges.get(current_node, {}).items():
                if neighbor not in visited:
                    steps.append(('explore', current_node, neighbor))
                    new_distance = current_distance + weight
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        parent[neighbor] = current_node
                        heapq.heappush(pq, (new_distance, neighbor))
                        steps.append(('update_distance', neighbor, new_distance, current_node))
        return steps

    def render_step(self, canvas, graph, all_steps, index):
        node_ui, edge_ui, text_ui = self._draw_base_graph(canvas, graph)

        node_colors = {}
        edge_colors = {}
        node_texts = {node: "∞" for node in graph.nodes}
        visited = set()
        pq = []
        distances = {node: float('inf') for node in graph.nodes}
        parent = {}

        for i in range(index + 1):
            step = all_steps[i]
            action = step[0]
            if action == 'update_distance':
                node = step[1]
                distance = step[2]
                node_texts[node] = str(distance)
                distances[node] = distance
                pq.append((distance, node))

                if len(step) > 3: # có parent
                    parent[node] = step[3]

                if node not in node_colors or node_colors[node] != 'lightgreen':
                    node_colors[node] = 'orange'

            elif action == 'visit':
                node = step[1]
                node_colors[node] = 'lightgreen'
                visited.add(node)
                pq = [(d, n) for (d, n) in pq if n != node]
            elif action == 'explore':
                # (step[1], step[2]) == from_node, to_node
                edge_key = tuple(sorted((step[1], step[2])))
                edge_colors[edge_key] = 'red'

        # Áp dụng màu và text
        for node, color in node_colors.items():
            if node in node_ui:
                canvas.itemconfig(node_ui[node], fill=color)
        for edge_key, color in edge_colors.items():
            if edge_key in edge_ui:
                canvas.itemconfig(edge_ui[edge_key], fill=color, width=3)
        for node, dist_text in node_texts.items():
            if node in text_ui:
                canvas.itemconfig(text_ui[node], text=f"{node}\n{dist_text}")

        canvas.delete("info_text")

        visited_text = "Visited: " + ", ".join(sorted(visited))
        pq_text = "Priority Queue: " + ", ".join([f"{n}({d})" for d, n in sorted(pq)])
        dist_text = "Distances: " + ", ".join(
            [f"{n}={distances[n] if distances[n] != float('inf') else '∞'}" for n in sorted(distances)])
        parent_text = "Parent: " + ", ".join([f"{child}←{par}" for child, par in parent.items()])

        canvas_height = 600
        canvas.create_text(20, canvas_height-120, anchor="w", text=visited_text,
                           font=("Helvetica", 14, "bold"), fill="blue", tags="info_text")
        canvas.create_text(20, canvas_height-150, anchor="w", text=pq_text,
                           font=("Helvetica", 14, "bold"), fill="green", tags="info_text")
        canvas.create_text(20, canvas_height-180, anchor="w", text=dist_text,
                           font=("Helvetica", 14, "bold"), fill="purple", tags="info_text")
        canvas.create_text(20, canvas_height-210, anchor="w", text=parent_text,
                           font=("Helvetica", 14, "bold"), fill="brown", tags="info_text")

    def _draw_base_graph(self, canvas, graph):
        """Vẽ đồ thị có trọng số"""
        canvas.delete("all")
        node_ui = {}
        edge_ui = {}
        text_ui = {}
        node_radius = 20
        default_color = 'lightgray'

        for node, neighbors in graph.dijkstra_weighted_edges.items():
            x1, y1 = graph.dijkstra_nodes[node]
            # 'neighbors' là một dict: {'B': 10, 'C': 3}
            for neighbor, weight in neighbors.items():
                key = tuple(sorted((node, neighbor)))
                if key not in edge_ui:
                    x2, y2 = graph.dijkstra_nodes[neighbor]
                    edge_id = canvas.create_line(
                        x1, y1, x2, y2, fill=default_color, width=2
                    )
                    edge_ui[key] = edge_id

                    # Vẽ trọng số (weight) ở giữa cạnh
                    mid_x = (x1 + x2) / 2
                    mid_y = (y1 + y2) / 2
                    canvas.create_text(
                        mid_x, mid_y,
                        text=str(weight),
                        font=('Arial', 10, 'bold'),
                        fill='blue'
                    )

        # Vẽ các nút (Nodes)
        for node, (x, y) in graph.dijkstra_nodes.items():
            oval_id = canvas.create_oval(
                x - node_radius, y - node_radius,
                x + node_radius, y + node_radius,
                fill=default_color, outline='black', width=2
            )
            # Text sẽ được cập nhật bởi hàm render_step
            text_id = canvas.create_text(x, y, text=node,
                                         font=('Arial', 12, 'bold'))
            node_ui[node] = oval_id
            text_ui[node] = text_id

        return node_ui, edge_ui, text_ui