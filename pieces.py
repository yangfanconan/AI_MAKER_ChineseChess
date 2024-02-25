import pygame  
from board import Board  

SQUARE_SIZE =60  # 方格的大小  
MARGIN_BETWEEN_SQUARES = 5  # 方格之间的间距  
MARGIN = 20  # 棋盘边缘与屏幕边缘的间距

# 棋子基类  
class Piece:  
    def __init__(self, side, image_path):  
        self.side = side  # 哪一方：'red' 或 'black'  
        self.image = pygame.image.load(image_path)  
        self.rect = self.image.get_rect()  
        self.position = None  # (row, col) 表示在棋盘上的位置，初始化为None  
      
    def draw(self, screen, position):  
        # 绘制棋子到屏幕上指定位置  
        self.rect.center = position  
        screen.blit(self.image, self.rect)  
      
    def set_position(self, row, col):  
        self.position = (row, col)  
      
    def get_position(self):  
        return self.position  
      
    def is_valid_move(self, board, from_pos, to_pos):  
        # 棋子移动的有效性检查（需要在子类中实现）  
        raise NotImplementedError  
      
    def move(self, board, to_pos):  
        # 执行移动（需要在子类中实现）  
        raise NotImplementedError  
  
# 帅/将 类  
class General(Piece):  
    def __init__(self, side):  
        super().__init__(side, f'path_to_{side}_general_image.png')  
        # 可以添加特定的初始化代码，比如设置移动范围等  
      
    def is_valid_move(self, board, from_pos, to_pos):  
        # 检查帅/将的移动是否有效（只能在九宫格内移动）  
        from_row, from_col = from_pos  
        to_row, to_col = to_pos  
          
        # 检查移动是否在九宫格内  
        if not (0 <= to_row < 3 if self.side == 'red' else 7 <= to_row < 10) or not (0 <= to_col < 3 or 6 <= to_col < 9):  
            return False  
          
        # 检查移动距离是否为1（上下左右或斜着移动）  
        if abs(to_row - from_row) > 1 or abs(to_col - from_col) > 1:  
            return False  
          
        # 检查移动路径上是否有其他棋子阻挡（帅/将不能斜着跳过棋子移动）  
        if (to_row - from_row) != 0 and (to_col - from_col) != 0:  
            block_row, block_col = (from_row + to_row) // 2, (from_col + to_col) // 2  
            if board.get_piece_at(*self._screen_to_board_coords(block_row, block_col)):  
                return False  
          
        # 检查目标位置是否为空或者为对方的棋子（吃子）  
        target_piece = board.get_piece_at(*self._screen_to_board_coords(to_row, to_col))  
        if target_piece and target_piece.side == self.side:  
            return False  
          
        return True  
      
    def _screen_to_board_coords(self, row, col):  
        # 将屏幕坐标转换为棋盘坐标的辅助方法（这里需要根据实际情况调整）  
        # 注意：这个方法在这里可能并不准确，因为屏幕坐标和棋盘坐标的转换通常在Board类中处理。  
        # 这里只是为了演示目的而包含了这个方法。在实际应用中，你应该使用Board类提供的方法来转换坐标。  
        return (row // (SQUARE_SIZE + MARGIN_BETWEEN_SQUARES), col // (SQUARE_SIZE + MARGIN_BETWEEN_SQUARES))  
      
    def move(self, board, to_pos):  
        # 执行帅/将的移动  
        to_row, to_col = to_pos  
        from_row, from_col = self.get_position()  
        board.move_piece(self._board_to_screen_coords(from_row, from_col)[0],   
                         self._board_to_screen_coords(from_row, from_col)[1],   
                         self._board_to_screen_coords(to_row, to_col)[0],   
                         self._board_to_screen_coords(to_row, to_col)[1])  
        self.set_position(to_row, to_col)  
      
    def _board_to_screen_coords(self, row, col):  
        # 将棋盘坐标转换为屏幕坐标的辅助方法（与_screen_to_board_coords相反）  
        # 注意：这个方法同样可能不准确，并且应该由Board类来处理坐标转换。  
        return (MARGIN + col * SQUARE_SIZE + SQUARE_SIZE // 2, MARGIN + row * SQUARE_SIZE + SQUARE_SIZE // 2)  
  
# 其他棋子类（如车、马、炮等）也可以按照类似的方式实现，但会有不同的移动规则。  
# 例如，车可以在任何方向上直行；马走“日”字形；炮需要隔一个棋子跳吃等。  
  
# 这里只是给出了一个简化的框架和帅/将类的部分实现作为示例。你需要根据实际的游戏规则和图像资源来完成所有棋子类的实现。