import random


class Graph:
    def __init__(self, nodes):
        self.nodes = nodes
        self.radius = 10
        self.queue = []
        self.visited = []

    def add_node(self, node_id, x, y):
        node = Node(node_id, x, y)
        self.nodes.append(node)

    def render_node(self, canvas):
        node = self.nodes[-1]
        canvas.create_oval(
            node.x + self.radius,
            node.y + self.radius,
            node.x - self.radius,
            node.y - self.radius,
        )

        canvas.create_text(
            node.x,
            node.y + self.radius + 10,
            text=node.node_id + 1
        )

        canvas.update()

    def color_node(self, node, color, canvas):
        canvas.create_oval(
            node.x + self.radius,
            node.y + self.radius,
            node.x - self.radius,
            node.y - self.radius,
            fill=color
        )

        canvas.update()

    def identify_node(self, x, y):
        area = self.radius + 5
        for node in self.nodes:
            if (node.x - area) <= x <= (node.x + area) and \
                    (node.y - area) <= y <= (node.y + area):
                return node

    def create_edge(self, node_a, node_b, canvas):
        if (node_a not in node_b.linked) and (node_b not in node_a.linked):
            node_a.linked.append(node_b)
            node_b.linked.append(node_a)

            canvas.create_line(
                node_a.x, node_a.y,
                node_b.x, node_b.y
            )

            canvas.update()

    def clear_visited(self):
        self.visited = []
        return self

    def initialize_visited(self):
        self.visited = [False for i in range(len(self.nodes))]
        return self

    def analyze_components(self, colors, canvas):
        self.clear_visited()
        self.initialize_visited()

        remaining_colors = colors[:]

        for node in self.nodes:
            if not self.visited[node.node_id]:
                color = random.choice(remaining_colors)
                remaining_colors.remove(color)
                if not remaining_colors:
                    remaining_colors = colors[:]
                self.color_component(node, color, canvas)

    # TODO - proper BFS algorithm
    def color_component(self, node, color, canvas):
        self.visited[node.node_id] = True
        self.color_node(node, color, canvas)

        for linked_node in node.linked:
            if not self.visited[linked_node.node_id]:
                self.color_component(linked_node, color, canvas)

    def temp_function(self):
        print('clicked a button')


class Node:
    def __init__(self, node_id, x, y):
        self.node_id = node_id
        self.x = x
        self.y = y
        self.linked = []
