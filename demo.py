#!/usr/bin/env python3
from lifegame import LifeGame
import time

def demo_glider():
    print("=== グライダーのデモ ===")
    game = LifeGame(20, 20)
    game.set_glider(5, 5)
    
    for i in range(15):
        game.print_grid()
        print(f"世代: {game.generation}")
        time.sleep(0.8)
        game.next_generation()

def demo_blinker():
    print("\n=== ブリンカーのデモ ===")
    game = LifeGame(15, 15)
    game.set_blinker(6, 6)
    
    for i in range(8):
        game.print_grid()
        print(f"世代: {game.generation}")
        time.sleep(1.0)
        game.next_generation()

def demo_random():
    print("\n=== ランダムパターンのデモ ===")
    game = LifeGame(25, 25)
    game.random_pattern(0.25)
    
    for i in range(20):
        game.print_grid()
        print(f"世代: {game.generation}")
        time.sleep(0.5)
        game.next_generation()

if __name__ == "__main__":
    print("Conway's Game of Life - デモンストレーション")
    print("=" * 50)
    
    try:
        demo_glider()
        demo_blinker()
        demo_random()
        print("\nデモンストレーション完了!")
    except KeyboardInterrupt:
        print("\n\nデモンストレーションを中止しました。")