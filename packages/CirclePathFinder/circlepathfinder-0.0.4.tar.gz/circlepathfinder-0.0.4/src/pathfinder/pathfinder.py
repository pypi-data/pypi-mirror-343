
import math
from collections import defaultdict
from heapq import heappush, heappop
from scipy.spatial import KDTree

def arc_distance(p1, p2, center):
    a = math.atan2(p1[1] - center[1], p1[0] - center[0])
    b = math.atan2(p2[1] - center[1], p2[0] - center[0])
    angle = abs(b - a)
    angle = min(angle, 2 * math.pi - angle)
    radius = math.dist(center, p1)
    return radius * angle

class FastCircleGraph:
    def __init__(self, points, k_neighbors=10):
        self.white_points = [tuple(p) for p in points]
        self.k = k_neighbors
        self.graph = defaultdict(list)

    def build(self):
        tree = KDTree(self.white_points)

        circle_map = {}
        pink_points = set()

        for i, p1 in enumerate(self.white_points):
            dists, indices = tree.query(p1, k=self.k + 1)
            for j in indices[1:]:  # skip self
                p2 = self.white_points[j]
                if (i, j) in circle_map or (j, i) in circle_map:
                    continue
                center = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
                radius = math.dist(p1, p2) / 2
                angle_offset = math.pi / 3  # Approximate intersection angle
                for sign in [1, -1]:
                    angle = math.atan2(p2[1] - p1[1], p2[0] - p1[0]) + sign * angle_offset
                    px = center[0] + radius * math.cos(angle)
                    py = center[1] + radius * math.sin(angle)
                    pink = (round(px, 5), round(py, 5))
                    pink_points.add(pink)
                    self.graph[p1].append((pink, math.dist(p1, pink)))
                    self.graph[p2].append((pink, math.dist(p2, pink)))
                    self.graph[pink].append((p1, math.dist(p1, pink)))
                    self.graph[pink].append((p2, math.dist(p2, pink)))
                circle_map[(i, j)] = True

        # Optionally connect pink-pink if they share a center (here we omit this for speed)

    def find_shortest_path(self, start_white, end_white):
        start = tuple(start_white)
        end = tuple(end_white)
        queue = [(0, start, [start])]
        visited = set()

        while queue:
            cost, node, path = heappop(queue)
            if node in visited:
                continue
            visited.add(node)
            if node == end:
                return cost, path
            for neighbor, weight in self.graph[node]:
                if neighbor not in visited:
                    heappush(queue, (cost + weight, neighbor, path + [neighbor]))

        return float('inf'), None

def calculate_shortest_path(points):
    graph = FastCircleGraph(points)
    graph.build()
    return graph.find_shortest_path(points[0], points[-1])
