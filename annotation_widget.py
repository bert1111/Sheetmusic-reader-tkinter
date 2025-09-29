import tkinter as tk

class AnnotationWidget(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<ButtonPress-1>", self.start_draw)
        self.bind("<B1-Motion>", self.draw)
        self.bind("<ButtonRelease-1>", self.end_draw)

        self.drawing = False
        self.lines = []  # lijsten van relatieve coördinaten per lijn
        self.current_line = []

    def start_draw(self, event):
        self.drawing = True
        x, y = event.x, event.y
        self.current_line = [(x, y)]

    def draw(self, event):
        if not self.drawing:
            return
        x, y = event.x, event.y
        self.create_line(self.current_line[-1][0], self.current_line[-1][1], x, y,
                         fill='red', width=2)
        self.current_line.append((x, y))

    def end_draw(self, event):
        if not self.drawing:
            return
        self.drawing = False
        width = self.winfo_width()
        height = self.winfo_height()
        # converteer absolute pixels naar relatieve coördinaten 0-1
        rel_points = [(x/width, y/height) for x, y in self.current_line]
        self.lines.append(rel_points)
        self.current_line = []

    def clear(self):
        self.delete("all")
        self.lines.clear()

    def load_lines(self, lines):
        self.clear()
        width = self.winfo_width()
        height = self.winfo_height()
        for line in lines:
            points = [(x*width, y*height) for x, y in line]
            for i in range(1, len(points)):
                self.create_line(points[i-1][0], points[i-1][1], points[i][0], points[i][1],
                                 fill='red', width=2)
            self.lines.append(line)
