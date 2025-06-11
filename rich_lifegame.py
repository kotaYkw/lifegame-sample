import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
import matplotlib.patches as patches
from collections import defaultdict
import time
import os


class RichLifeGame:
    def __init__(self, width=50, height=50):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)
        self.cell_age = np.zeros((height, width), dtype=int)
        self.generation = 0
        self.population_history = []
        self.birth_count = 0
        self.death_count = 0
        self.max_age = 0
        
        # カラーテーマ設定
        self.themes = {
            'classic': {'dead': '#000000', 'alive': '#FFFFFF', 'grid': '#333333'},
            'neon': {'dead': '#0a0a0a', 'alive': '#00ff41', 'grid': '#004d1a'},
            'ocean': {'dead': '#001122', 'alive': '#4da6ff', 'grid': '#002244'},
            'fire': {'dead': '#2d1b00', 'alive': '#ff6600', 'grid': '#663300'},
            'matrix': {'dead': '#000000', 'alive': '#00ff00', 'grid': '#003300'},
            'sunset': {'dead': '#1a0f0f', 'alive': '#ff8c69', 'grid': '#4d2626'}
        }
        self.current_theme = 'neon'
    
    def set_cell(self, x, y, state=1):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y, x] = state
            if state == 1:
                self.cell_age[y, x] = 1
            else:
                self.cell_age[y, x] = 0
    
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
        new_age = np.zeros_like(self.cell_age)
        births = 0
        deaths = 0
        
        for y in range(self.height):
            for x in range(self.width):
                neighbors = self.get_neighbors_count(x, y)
                current_cell = self.grid[y, x]
                
                if current_cell == 1:
                    if neighbors in [2, 3]:
                        new_grid[y, x] = 1
                        new_age[y, x] = self.cell_age[y, x] + 1
                        self.max_age = max(self.max_age, new_age[y, x])
                    else:
                        deaths += 1
                else:
                    if neighbors == 3:
                        new_grid[y, x] = 1
                        new_age[y, x] = 1
                        births += 1
        
        self.grid = new_grid
        self.cell_age = new_age
        self.generation += 1
        self.birth_count = births
        self.death_count = deaths
        self.population_history.append(np.sum(self.grid))
    
    def clear(self):
        self.grid = np.zeros((self.height, self.width), dtype=int)
        self.cell_age = np.zeros((self.height, self.width), dtype=int)
        self.generation = 0
        self.population_history = []
        self.max_age = 0
    
    def random_pattern(self, density=0.3):
        self.grid = np.random.choice([0, 1], size=(self.height, self.width), 
                                   p=[1-density, density])
        self.cell_age = self.grid.copy()
        self.generation = 0
        self.population_history = [np.sum(self.grid)]
    
    def set_glider(self, start_x=1, start_y=1):
        pattern = [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)]
        for dx, dy in pattern:
            self.set_cell(start_x + dx, start_y + dy, 1)
    
    def set_gosper_gun(self, start_x=5, start_y=5):
        gun_pattern = [
            (24, 0), (22, 1), (24, 1), (12, 2), (13, 2), (20, 2), (21, 2), 
            (34, 2), (35, 2), (11, 3), (15, 3), (20, 3), (21, 3), (34, 3), 
            (35, 3), (0, 4), (1, 4), (10, 4), (16, 4), (20, 4), (21, 4), 
            (0, 5), (1, 5), (10, 5), (14, 5), (16, 5), (17, 5), (22, 5), 
            (24, 5), (10, 6), (16, 6), (24, 6), (11, 7), (15, 7), (12, 8), (13, 8)
        ]
        for dx, dy in gun_pattern:
            if start_x + dx < self.width and start_y + dy < self.height:
                self.set_cell(start_x + dx, start_y + dy, 1)
    
    def set_pulsar(self, start_x=10, start_y=10):
        pulsar_pattern = [
            (2, 0), (3, 0), (4, 0), (8, 0), (9, 0), (10, 0),
            (0, 2), (5, 2), (7, 2), (12, 2),
            (0, 3), (5, 3), (7, 3), (12, 3),
            (0, 4), (5, 4), (7, 4), (12, 4),
            (2, 5), (3, 5), (4, 5), (8, 5), (9, 5), (10, 5),
            (2, 7), (3, 7), (4, 7), (8, 7), (9, 7), (10, 7),
            (0, 8), (5, 8), (7, 8), (12, 8),
            (0, 9), (5, 9), (7, 9), (12, 9),
            (0, 10), (5, 10), (7, 10), (12, 10),
            (2, 12), (3, 12), (4, 12), (8, 12), (9, 12), (10, 12)
        ]
        for dx, dy in pulsar_pattern:
            if start_x + dx < self.width and start_y + dy < self.height:
                self.set_cell(start_x + dx, start_y + dy, 1)
    
    def create_age_colormap(self):
        if self.max_age <= 1:
            return ListedColormap(['black', self.themes[self.current_theme]['alive']])
        
        # 年齢に基づいたカラーマップの作成
        colors = ['black']  # 死んだセル
        theme = self.themes[self.current_theme]
        
        if self.current_theme == 'neon':
            age_colors = ['#00ff41', '#00cc33', '#009926', '#006619', '#00330c']
        elif self.current_theme == 'fire':
            age_colors = ['#ff6600', '#ff4400', '#cc3300', '#992200', '#661100']
        elif self.current_theme == 'ocean':
            age_colors = ['#4da6ff', '#3d8ccc', '#2d7399', '#1d5966', '#0d4033']
        else:
            # デフォルトのグラデーション
            base_color = theme['alive']
            age_colors = [base_color] * 5
        
        # 最大年齢に応じて色を調整
        for i in range(min(self.max_age, len(age_colors))):
            colors.append(age_colors[i])
        
        return ListedColormap(colors)
    
    def setup_interactive_controls(self, fig, ax_main):
        """インタラクティブ操作の設定"""
        self.selected_cells = set()
        
        def on_click(event):
            if event.inaxes == ax_main and event.button == 1:  # 左クリック
                x, y = int(event.xdata + 0.5), int(event.ydata + 0.5)
                if 0 <= x < self.width and 0 <= y < self.height:
                    # セルの状態を切り替え
                    current_state = self.grid[y, x]
                    self.set_cell(x, y, 1 - current_state)
                    # 即座に表示更新
                    plt.draw()
        
        def on_key(event):
            if event.key == ' ':  # スペースキーで一時停止/再開
                self.is_paused = not self.is_paused
            elif event.key == 'r':  # 'r'キーでリセット
                self.clear()
                plt.draw()
            elif event.key == 'q':  # 'q'キーで終了
                plt.close()
            elif event.key.isdigit():  # 数字キーでテーマ変更
                themes = list(self.themes.keys())
                theme_idx = int(event.key) - 1
                if 0 <= theme_idx < len(themes):
                    self.current_theme = themes[theme_idx]
        
        fig.canvas.mpl_connect('button_press_event', on_click)
        fig.canvas.mpl_connect('key_press_event', on_key)
        
        # 操作説明をタイトルに追加
        help_text = "Controls: Space=Pause, R=Reset, Q=Quit, 1-6=Theme, Click=Toggle Cell"
        fig.suptitle(help_text, color='white', fontsize=10, y=0.02)
    
    def run_rich_animation(self, generations=200, interval=100, theme='neon', interactive=True):
        self.current_theme = theme
        self.is_paused = False
        self.current_frame = 0
        
        # フィギュアとサブプロットの設定
        fig = plt.figure(figsize=(16, 10))
        fig.patch.set_facecolor('#0a0a0a')
        
        # グリッドレイアウト
        gs = fig.add_gridspec(3, 3, width_ratios=[3, 1, 1], height_ratios=[2, 1, 1])
        
        # メインのライフゲームエリア
        ax_main = fig.add_subplot(gs[:, 0])
        ax_main.set_facecolor(self.themes[theme]['dead'])
        
        # 統計表示エリア
        ax_stats = fig.add_subplot(gs[0, 1])
        ax_population = fig.add_subplot(gs[1, 1])
        ax_info = fig.add_subplot(gs[2, 1])
        
        # 年齢ヒストグラム
        ax_age = fig.add_subplot(gs[:, 2])
        
        # インタラクティブ機能の設定
        if interactive:
            self.setup_interactive_controls(fig, ax_main)
        
        # 初期設定
        colormap = self.create_age_colormap()
        im = ax_main.imshow(self.cell_age, cmap=colormap, vmin=0, vmax=max(1, self.max_age))
        
        # グリッドライン
        ax_main.set_xticks(np.arange(-0.5, self.width, 1), minor=True)
        ax_main.set_yticks(np.arange(-0.5, self.height, 1), minor=True)
        ax_main.grid(which='minor', color=self.themes[theme]['grid'], linewidth=0.5, alpha=0.3)
        ax_main.tick_params(which='minor', size=0, labelbottom=False, labelleft=False)
        ax_main.set_xticks([])
        ax_main.set_yticks([])
        
        # タイトル設定
        title_color = self.themes[theme]['alive']
        ax_main.set_title('Conway\'s Game of Life - Enhanced Visualization', 
                         color=title_color, fontsize=16, fontweight='bold', pad=20)
        
        # 統計表示の初期化
        ax_stats.set_facecolor('#0f0f0f')
        ax_population.set_facecolor('#0f0f0f')
        ax_info.set_facecolor('#0f0f0f')
        ax_age.set_facecolor('#0f0f0f')
        
        # 軸の色設定
        for ax in [ax_stats, ax_population, ax_info, ax_age]:
            ax.tick_params(colors=title_color)
            for spine in ax.spines.values():
                spine.set_color(title_color)
        
        def animate(frame):
            if frame > 0 and not self.is_paused:
                self.next_generation()
                self.current_frame = frame
            
            # メイン表示の更新
            colormap = self.create_age_colormap()
            im.set_cmap(colormap)
            im.set_array(self.cell_age)
            im.set_clim(0, max(1, self.max_age))
            
            # タイトル更新
            population = np.sum(self.grid)
            ax_main.set_title(f'Generation: {self.generation} | Population: {population} | Theme: {theme.title()}',
                            color=title_color, fontsize=14, fontweight='bold')
            
            # 統計情報更新
            ax_stats.clear()
            ax_stats.set_facecolor('#0f0f0f')
            stats_text = f'Generation: {self.generation}\n'
            stats_text += f'Population: {population}\n'
            stats_text += f'Births: {self.birth_count}\n'
            stats_text += f'Deaths: {self.death_count}\n'
            stats_text += f'Max Age: {self.max_age}'
            
            ax_stats.text(0.05, 0.95, stats_text, transform=ax_stats.transAxes,
                         verticalalignment='top', color=title_color, fontsize=10,
                         fontfamily='monospace')
            ax_stats.set_title('Statistics', color=title_color, fontsize=12)
            ax_stats.set_xticks([])
            ax_stats.set_yticks([])
            
            # 人口グラフ更新
            if len(self.population_history) > 1:
                ax_population.clear()
                ax_population.set_facecolor('#0f0f0f')
                ax_population.plot(self.population_history, color=title_color, linewidth=2)
                ax_population.fill_between(range(len(self.population_history)), 
                                         self.population_history, alpha=0.3, color=title_color)
                ax_population.set_title('Population History', color=title_color, fontsize=12)
                ax_population.tick_params(colors=title_color, labelsize=8)
                ax_population.grid(True, alpha=0.3, color=title_color)
            
            # 年齢分布更新
            if self.max_age > 0:
                ax_age.clear()
                ax_age.set_facecolor('#0f0f0f')
                ages = self.cell_age[self.grid == 1]
                if len(ages) > 0:
                    bins = range(1, self.max_age + 2)
                    ax_age.hist(ages, bins=bins, color=title_color, alpha=0.7, edgecolor='black')
                ax_age.set_title('Cell Age Distribution', color=title_color, fontsize=12)
                ax_age.tick_params(colors=title_color, labelsize=8)
                ax_age.set_xlabel('Age', color=title_color, fontsize=10)
                ax_age.set_ylabel('Count', color=title_color, fontsize=10)
            
            # パフォーマンス情報
            ax_info.clear()
            ax_info.set_facecolor('#0f0f0f')
            if len(self.population_history) > 10:
                recent_pop = self.population_history[-10:]
                trend = "Stable" if max(recent_pop) - min(recent_pop) < 5 else "Changing"
                growth_rate = (recent_pop[-1] - recent_pop[0]) / len(recent_pop) if recent_pop[0] > 0 else 0
            else:
                trend = "Starting"
                growth_rate = 0
            
            info_text = f'Trend: {trend}\n'
            info_text += f'Growth Rate: {growth_rate:.2f}\n'
            info_text += f'Density: {population/(self.width*self.height)*100:.1f}%'
            
            ax_info.text(0.05, 0.95, info_text, transform=ax_info.transAxes,
                        verticalalignment='top', color=title_color, fontsize=10,
                        fontfamily='monospace')
            ax_info.set_title('Analysis', color=title_color, fontsize=12)
            ax_info.set_xticks([])
            ax_info.set_yticks([])
            
            return [im]
        
        # アニメーション実行
        ani = animation.FuncAnimation(fig, animate, frames=generations, 
                                    interval=interval, blit=False, repeat=True)
        
        plt.tight_layout()
        plt.show()
        return ani


def demo_rich_patterns():
    """リッチなアニメーションのデモンストレーション"""
    
    print("🎮 Rich Life Game Demonstrations")
    print("=" * 50)
    
    # 1. グライダーのデモ（ネオンテーマ）
    print("\n🚀 Glider Pattern - Neon Theme")
    game1 = RichLifeGame(40, 30)
    game1.set_glider(5, 5)
    game1.set_glider(15, 10)
    game1.set_glider(25, 15)
    
    print("Starting glider animation...")
    ani1 = game1.run_rich_animation(generations=100, interval=150, theme='neon')
    
    # 2. パルサーのデモ（ファイアテーマ）
    print("\n💫 Pulsar Pattern - Fire Theme")
    game2 = RichLifeGame(50, 40)
    game2.set_pulsar(15, 10)
    game2.set_pulsar(30, 20)
    
    print("Starting pulsar animation...")
    ani2 = game2.run_rich_animation(generations=150, interval=200, theme='fire')
    
    # 3. ランダムパターン（オーシャンテーマ）
    print("\n🌊 Random Pattern - Ocean Theme")
    game3 = RichLifeGame(60, 45)
    game3.random_pattern(0.35)
    
    print("Starting random pattern animation...")
    ani3 = game3.run_rich_animation(generations=200, interval=100, theme='ocean')


if __name__ == "__main__":
    print("Rich Conway's Game of Life")
    print("=" * 40)
    print("Available demos:")
    print("1. Interactive rich patterns")
    print("2. Automated demo sequence")
    
    try:
        choice = input("\nSelect option (1-2, default 2): ").strip() or "2"
        
        if choice == "1":
            # インタラクティブモード
            game = RichLifeGame(50, 40)
            
            print("\nPattern options:")
            print("1. Random")
            print("2. Gliders")
            print("3. Pulsar")
            print("4. Gosper Gun")
            
            pattern = input("Select pattern (1-4, default 1): ").strip() or "1"
            
            if pattern == "1":
                density = float(input("Density (0.1-0.5, default 0.3): ") or "0.3")
                game.random_pattern(density)
            elif pattern == "2":
                game.set_glider(10, 10)
                game.set_glider(20, 15)
            elif pattern == "3":
                game.set_pulsar(15, 10)
            elif pattern == "4":
                game.set_gosper_gun(5, 15)
            
            print("\nTheme options:")
            themes = list(game.themes.keys())
            for i, theme in enumerate(themes, 1):
                print(f"{i}. {theme.title()}")
            
            theme_choice = input(f"Select theme (1-{len(themes)}, default 2): ").strip() or "2"
            theme = themes[int(theme_choice) - 1]
            
            generations = int(input("Generations (default 200): ") or "200")
            speed = int(input("Animation speed ms (default 100): ") or "100")
            
            print(f"\nStarting rich animation with {theme} theme...")
            game.run_rich_animation(generations=generations, interval=speed, theme=theme)
            
        else:
            # デモモード
            demo_rich_patterns()
            
    except KeyboardInterrupt:
        print("\n\nAnimation stopped by user")
    except Exception as e:
        print(f"\nError: {e}")
        print("Running with default settings...")
        game = RichLifeGame(40, 30)
        game.random_pattern(0.3)
        game.run_rich_animation(generations=150, interval=150, theme='neon')