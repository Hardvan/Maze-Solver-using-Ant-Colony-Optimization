import tkinter as tk
import heapq
import random


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
        self.square_size = 42  # Adjust the size of each square

        self.canvas = tk.Canvas(
            root, width=self.cols * self.square_size, height=self.rows * self.square_size)
        self.canvas.pack()
        self.draw_maze()
        self.solve_maze()

    def draw_maze(self):
        for i in range(self.rows):
            for j in range(self.cols):
                color = "white" if not self.maze[i][j] else "black"
                self.canvas.create_rectangle(
                    j * self.square_size, i * self.square_size, (j + 1) * self.square_size, (i + 1) * self.square_size, fill=color)

                if (i, j) == (0, 0):
                    self.canvas.create_rectangle(
                        j * self.square_size, i * self.square_size, (j + 1) * self.square_size, (i + 1) * self.square_size, fill="yellow"
                    )
                if (i, j) == (self.rows - 1, self.cols - 1):
                    self.canvas.create_rectangle(
                        j * self.square_size, i * self.square_size, (j + 1) * self.square_size, (i + 1) * self.square_size, fill="green"
                    )

    def solve_maze(self):
        solver = MazeSolver(self.maze, (0, 0), (self.rows - 1, self.cols - 1))
        solver.solve()
        path = solver.reconstruct_path()
        self.animate_path(path)

    def animate_path(self, path):
        for i, (row, col) in enumerate(path):
            x, y = col * self.square_size, row * self.square_size

            # Blinking effect for source (yellow) and goal (green) squares
            if (row, col) == (0, 0) or (row, col) == (self.rows - 1, self.cols - 1):
                for _ in range(3):  # Blink for 3 iterations
                    self.canvas.create_oval(
                        x + 5, y + 5, x + self.square_size - 5, y + self.square_size - 5, fill="blue")
                    self.root.update()
                    self.root.after(300)  # Delay of 300 milliseconds

                    self.canvas.delete("all")
                    self.draw_maze()
                    self.root.update()
                    self.root.after(300)  # Delay of 300 milliseconds
            else:
                self.canvas.create_oval(
                    x + 5, y + 5, x + self.square_size - 5, y + self.square_size - 5, fill="blue")
                self.root.update()
                self.root.after(100)  # Add a delay of 100 milliseconds

                if i < len(path) - 1:
                    self.canvas.create_line(
                        x + self.square_size // 2, y + self.square_size // 2, path[i + 1][1] * self.square_size + self.square_size // 2, path[i + 1][0] * self.square_size + self.square_size // 2, fill="blue", width=2)
                    self.root.update()
                    self.root.after(100)  # Add a delay of 100 milliseconds
                    self.canvas.delete("all")
                    self.draw_maze()

        # After the animation is finished, display the final path
        for row, col in path:
            x, y = col * self.square_size, row * self.square_size
            self.canvas.create_oval(
                x + 5, y + 5, x + self.square_size - 5, y + self.square_size - 5, fill="blue")
            self.root.update()
            self.root.after(100)  # Add a delay of 100 milliseconds


def generate_random_maze(rows, cols):
    maze = [[random.randint(0, 1) for _ in range(cols)] for _ in range(rows)]
    maze[0][0] = 0  # Ensure the source remains open
    maze[rows - 1][cols - 1] = 0  # Ensure the goal remains open

    return maze


def main():
    # maze = [
    #     [0, 1, 0, 0, 0],
    #     [0, 0, 0, 1, 0],
    #     [1, 1, 0, 0, 0],
    #     [0, 0, 1, 1, 0],
    #     [0, 0, 0, 0, 0]
    # ]

    maze_sizes = [3, 5, 7]  # Define maze sizes to generate
    for size in maze_sizes:
        maze = generate_random_maze(size, size)
        root = tk.Tk()
        gui = MazeGUI(root, maze)
        root.mainloop()


if __name__ == "__main__":
    main()
