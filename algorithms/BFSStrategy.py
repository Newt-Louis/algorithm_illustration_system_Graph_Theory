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