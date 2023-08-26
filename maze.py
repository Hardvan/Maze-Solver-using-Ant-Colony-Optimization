import tkinter as tk
import heapq


class MazeSolver:
    def __init__(self, maze, start, end):
        self.maze = maze
        self.start = start
        self.end = end
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.visited = set()
        self.distances = {(i, j): float('inf')
                          for i in range(self.rows) for j in range(self.cols)}
        self.distances[start] = 0
        self.prev = {}
        self.queue = [(0, start)]

    def solve(self):
        while self.queue:
            dist, current = heapq.heappop(self.queue)
            if current == self.end:
                break
            if current in self.visited:
                continue
            self.visited.add(current)

            for neighbor in self.get_neighbors(current):
                if neighbor not in self.visited:
                    new_dist = dist + 1
                    if new_dist < self.distances[neighbor]:
                        self.distances[neighbor] = new_dist
                        self.prev[neighbor] = current
                        heapq.heappush(self.queue, (new_dist, neighbor))

    def get_neighbors(self, cell):
        i, j = cell
        neighbors = []
        if i > 0 and not self.maze[i - 1][j]:
            neighbors.append((i - 1, j))
        if i < self.rows - 1 and not self.maze[i + 1][j]:
            neighbors.append((i + 1, j))
        if j > 0 and not self.maze[i][j - 1]:
            neighbors.append((i, j - 1))
        if j < self.cols - 1 and not self.maze[i][j + 1]:
            neighbors.append((i, j + 1))
        return neighbors

    def reconstruct_path(self):
        path = []
        current = self.end
        while current != self.start:
            path.append(current)
            current = self.prev[current]
        path.append(self.start)
        return path[::-1]


class MazeGUI:
    def __init__(self, root, maze):
        self.root = root
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.canvas = tk.Canvas(
            root, width=self.cols * 30, height=self.rows * 30)
        self.canvas.pack()
        self.draw_maze()
        self.solve_maze()

    def draw_maze(self):
        for i in range(self.rows):
            for j in range(self.cols):
                color = "white" if not self.maze[i][j] else "black"
                self.canvas.create_rectangle(
                    j * 30, i * 30, (j + 1) * 30, (i + 1) * 30, fill=color)

                if (i, j) == (0, 0):
                    self.canvas.create_rectangle(
                        j * 30, i * 30, (j + 1) * 30, (i + 1) * 30, fill="yellow"
                    )
                if (i, j) == (self.rows - 1, self.cols - 1):
                    self.canvas.create_rectangle(
                        j * 30, i * 30, (j + 1) * 30, (i + 1) * 30, fill="green"
                    )

    def solve_maze(self):
        solver = MazeSolver(self.maze, (0, 0), (self.rows - 1, self.cols - 1))
        solver.solve()
        path = solver.reconstruct_path()
        self.animate_path(path)

    def animate_path(self, path):
        for i, (row, col) in enumerate(path):
            x, y = col * 30, row * 30
            self.canvas.create_oval(x + 5, y + 5, x + 25, y + 25, fill="blue")
            self.root.update()
            self.root.after(100)  # Add a delay of 100 milliseconds
            if i < len(path) - 1:
                self.canvas.create_line(
                    x + 15, y + 15, path[i + 1][1] * 30 + 15, path[i + 1][0] * 30 + 15, fill="blue", width=2)
                self.root.update()
                self.root.after(100)  # Add a delay of 100 milliseconds
                self.canvas.delete("all")
                self.draw_maze()


def main():
    maze = [
        [0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ]
    root = tk.Tk()
    gui = MazeGUI(root, maze)
    root.mainloop()


if __name__ == "__main__":
    main()
