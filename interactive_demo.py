#!/usr/bin/env python3
from rich_lifegame import RichLifeGame

def main():
    print("🎮 Rich Interactive Life Game Demo")
    print("=" * 50)
    print()
    print("✨ Features:")
    print("   • Real-time cell age visualization")
    print("   • Multiple color themes (Neon, Fire, Ocean, etc.)")
    print("   • Live statistics and population graphs")
    print("   • Interactive controls")
    print()
    print("🎮 Controls:")
    print("   • Click: Toggle cell state")
    print("   • Space: Pause/Resume animation")
    print("   • R: Reset grid")
    print("   • Q: Quit")
    print("   • 1-6: Switch color themes")
    print()
    
    # 初期パターンを設定
    game = RichLifeGame(50, 40)
    
    # 複数のパターンを配置
    print("🚀 Setting up interesting patterns...")
    
    # グライダー
    game.set_glider(5, 5)
    game.set_glider(40, 30)
    
    # パルサー
    game.set_pulsar(20, 15)
    
    # いくつかのランダムセル
    import numpy as np
    np.random.seed(42)
    for _ in range(20):
        x, y = np.random.randint(0, game.width), np.random.randint(0, game.height)
        game.set_cell(x, y, 1)
    
    print("✅ Patterns loaded!")
    print()
    print("🎬 Starting interactive animation...")
    print("   Try clicking on cells to create new patterns!")
    print("   Press different number keys to change themes!")
    
    # リッチアニメーション開始
    try:
        game.run_rich_animation(
            generations=500,
            interval=120,
            theme='neon',
            interactive=True
        )
    except KeyboardInterrupt:
        print("\n👋 Animation stopped by user")

if __name__ == "__main__":
    main()