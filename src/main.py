from game_engine import GameEngine


def main():
    """游戏入口点"""
    print("=== 文字 MUD 游戏 ===")
    engine = GameEngine()
    engine.start_game()


if __name__ == "__main__":
    main()