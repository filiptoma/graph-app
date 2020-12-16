import tkinter as tk
from GraphClasses import Graph


class App:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title('Graph App')

        self.nodes = []
        self.node_id = 0

        self.right_click_counter = 0
        self.selected_node_a = None
        self.selected_node_b = None

        with open('colors.txt', 'r') as source:
            self.colors = source.read().split('\n')

        width = 800
        height = 600
        self.canvas = tk.Canvas(width=width, height=height, bg='white')
        self.canvas.pack()

        self.graph = Graph(self.nodes)
        self.render_ui()

    def render_ui(self):
        components_btn = tk.Button(
            self.root,
            text='Components',
            command=self.component_analysis
        )
        path_btn = tk.Button(
            self.root,
            text='Shortest path',
            command=self.graph.temp_function
        )
        skeleton_btn = tk.Button(
            self.root,
            text='Skeleton',
            command=self.graph.temp_function
        )

        components_btn.place(x=20, y=20, height=30, width=100)
        path_btn.place(x=20, y=60, height=30, width=100)
        skeleton_btn.place(x=20, y=100, height=30, width=100)

        # command box borders
        self.canvas.create_rectangle(
            0, 0, 140, 150
        )

    def component_analysis(self):
        self.graph.analyze_components(self.colors, self.canvas)

    def left_click(self, event):
        x = event.x
        y = event.y

        # ignore click in the command box
        if 0 <= x <= 140 and 0 <= y <= 150:
            return

        self.graph.add_node(self.node_id, x, y)
        self.graph.render_node(self.canvas)
        self.node_id += 1

    def right_click(self, event):
        x = event.x
        y = event.y

        # ignore click in the command box
        if 0 <= x <= 140 and 0 <= y <= 150:
            return

        identified = self.graph.identify_node(x, y)
        if identified and self.right_click_counter == 0:
            self.selected_node_a = identified
            self.right_click_counter += 1
            return

        if identified and self.right_click_counter == 1:
            self.selected_node_b = identified

            self.graph.create_edge(
                self.selected_node_a,
                self.selected_node_b,
                self.canvas
            )

            self.right_click_counter = 0
            self.selected_node_a = None
            self.selected_node_b = None

    def init_mouse_clicks(self):
        self.canvas.bind_all('<Button-1>', self.left_click)
        self.canvas.bind_all('<Button-3>', self.right_click)

    def run(self) -> None:
        self.init_mouse_clicks()
        self.root.mainloop()


if __name__ == '__main__':
    App().run()
