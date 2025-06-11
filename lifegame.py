import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import os


class LifeGame:
    def __init__(self, width=50, height=50):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)
        self.generation = 0
    
    def set_cell(self, x, y, state=1):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y, x] = state
    
    def get_neighbors_count(self, x, y):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    count += self.grid[ny, nx]
        return count
    
    def next_generation(self):
        new_grid = np.zeros_like(self.grid)
        
        for y in range(self.height):
            for x in range(self.width):
                neighbors = self.get_neighbors_count(x, y)
                current_cell = self.grid[y, x]
                
                if current_cell == 1:
                    if neighbors in [2, 3]:
                        new_grid[y, x] = 1
                else:
                    if neighbors == 3:
                        new_grid[y, x] = 1
        
        self.grid = new_grid
        self.generation += 1
    
    def clear(self):
        self.grid = np.zeros((self.height, self.width), dtype=int)
        self.generation = 0
    
    def random_pattern(self, density=0.3):
        self.grid = np.random.choice([0, 1], size=(self.height, self.width), 
                                   p=[1-density, density])
        self.generation = 0
    
    def set_glider(self, start_x=1, start_y=1):
        pattern = [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)]
        for dx, dy in pattern:
            self.set_cell(start_x + dx, start_y + dy, 1)
    
    def set_blinker(self, start_x=10, start_y=10):
        pattern = [(0, 0), (1, 0), (2, 0)]
        for dx, dy in pattern:
            self.set_cell(start_x + dx, start_y + dy, 1)
    
    def set_block(self, start_x=20, start_y=20):
        pattern = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for dx, dy in pattern:
            self.set_cell(start_x + dx, start_y + dy, 1)
    
    def print_grid(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"Generation: {self.generation}")
        print("+" + "-" * self.width + "+")
        for row in self.grid:
            print("|" + "".join("█" if cell else " " for cell in row) + "|")
        print("+" + "-" * self.width + "+")
    
    def run_simulation(self, generations=100, delay=0.1, show_animation=False):
        if show_animation:
            self._run_matplotlib_animation(generations)
        else:
            for _ in range(generations):
                self.print_grid()
                time.sleep(delay)
                self.next_generation()
    
    def _run_matplotlib_animation(self, generations):
        fig, ax = plt.subplots(figsize=(10, 10))
        im = ax.imshow(self.grid, cmap='binary', vmin=0, vmax=1)
        ax.set_title(f'Conway\'s Game of Life - Generation: {self.generation}')
        ax.set_xticks([])
        ax.set_yticks([])
        
        def animate(frame):
            self.next_generation()
            im.set_array(self.grid)
            ax.set_title(f'Conway\'s Game of Life - Generation: {self.generation}')
            return [im]
        
        ani = animation.FuncAnimation(fig, animate, frames=generations, 
                                    interval=100, blit=True, repeat=False)
        plt.show()


def main():
    print("Conway's Game of Life Simulator")
    print("=" * 40)
    
    game = LifeGame(30, 30)
    
    print("\n1. Random pattern")
    print("2. Glider")
    print("3. Blinker")
    print("4. Block")
    print("5. Custom pattern")
    
    choice = input("\nSelect initial pattern (1-5): ").strip()
    
    if choice == "1":
        density = float(input("Enter density (0.0-1.0, default 0.3): ") or "0.3")
        game.random_pattern(density)
    elif choice == "2":
        game.set_glider()
    elif choice == "3":
        game.set_blinker()
    elif choice == "4":
        game.set_block()
    elif choice == "5":
        print("Enter coordinates for live cells (format: x,y). Press Enter when done.")
        while True:
            coord = input("Coordinate: ").strip()
            if not coord:
                break
            try:
                x, y = map(int, coord.split(','))
                game.set_cell(x, y, 1)
            except ValueError:
                print("Invalid format. Use x,y")
    
    generations = int(input("Number of generations (default 50): ") or "50")
    
    animation_choice = input("Use matplotlib animation? (y/n, default n): ").strip().lower()
    show_animation = animation_choice == 'y'
    
    print(f"\nStarting simulation for {generations} generations...")
    print("Press Ctrl+C to stop\n")
    
    try:
        game.run_simulation(generations, delay=0.2, show_animation=show_animation)
    except KeyboardInterrupt:
        print("\nSimulation stopped by user")
    
    print(f"\nFinal generation: {game.generation}")


if __name__ == "__main__":
    main()