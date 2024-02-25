from borad import Board
from ai import AI  
import sys  
  
def print_board(board):  
    """打印当前棋盘状态。"""  
    print(board)  
  
def get_human_move(board, color):  
    """获取人类玩家的移动。"""  
    # 这里应该有一个更复杂的输入验证机制来处理不合法的移动  
    try:  
        move = input(f"Player {color}, enter your move (from-to): ")  
        from_pos, to_pos = move.split('-')  
        from_x, from_y = int(from_pos[0]), int(from_pos[1])  
        to_x, to_y = int(to_pos[0]), int(to_pos[1])  
        return Move(from_x, from_y, to_x, to_y)  
    except ValueError:  
        print("Invalid move format. Please enter it like 'e2-e4'.")  
        return None  
    except Exception as e:  
        print(f"An error occurred: {e}")  
        return None  
  
def main():  
    # 初始化棋盘  
    board = Board()  
    print_board(board)  
  
    # 设置AI玩家和人类玩家的颜色  
    ai_color = 'red'  # 假设AI玩家为红色  
    human_color = board.get_opponent_color(ai_color)  
  
    # 初始化AI  
    ai_player = AI(board, ai_color)  
  
    # 游戏主循环  
    while not board.is_game_over():  
        # 人类玩家移动  
        human_move = get_human_move(board, human_color)  
        while human_move is None or not board.is_valid_move(human_move, human_color):  
            print("Invalid move. Try again.")  
            human_move = get_human_move(board, human_color)  
        board.make_move(human_move)  
        print_board(board)  
  
        # 检查游戏是否结束  
        if board.is_game_over():  
            print(f"Game over! Player {board.get_winner()} wins!")  
            break  
  
        # AI玩家移动  
        ai_move = ai_player.make_move()  
        if ai_move is not None:  
            board.make_move(ai_move)  
            print_board(board)  
  
if __name__ == "__main__":  
    main()