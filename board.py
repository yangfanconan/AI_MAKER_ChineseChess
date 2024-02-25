import pygame  
  
# 假设每个格子的尺寸  
SQUARE_SIZE = 60  
# 棋盘边界和起始位置调整  
MARGIN = 20  
  
class Board:  
    def __init__(self):  
        # 初始化一个10x9的二维数组来表示棋盘上的位置  
        # 这里简化处理，只记录棋盘上是否有棋子，而不区分是哪一方的棋子  
        self.grid = [[None for _ in range(9)] for _ in range(10)]  
          
        # 加载棋盘图片（这里只是一个占位符，你需要替换为实际的图片路径）  
        self.board_image = pygame.image.load('/assets/images/boardchess.jpg')  
          
        # 设置棋盘尺寸和位置  
        self.rect = self.board_image.get_rect()  
        self.rect.topleft = (MARGIN, MARGIN)  
          
        # 初始化棋子（这里只是一个示例，你需要根据实际的初始位置来放置棋子）  
        self.init_pieces()  
      
    def init_pieces(self):  
        #     """初始化棋盘上的所有棋子。"""  
        # 这里只展示了部分棋子的初始化，你需要完成其他棋子的初始化  
        colors = ['red', 'black']  # 中国象棋通常用红色和黑色来表示双方  
  
        for color, start_row in zip(colors, [0, 8]):  
            # 初始化卒/兵  
            for col in range(5):  
                self.grid[start_row + col][col] = Soldier(color, 'P' if color == 'red' else 'p')  
  
            # 初始化炮  
            for col in [1, 8]:  
                self.grid[start_row][col] = Cannon(color, 'C' if color == 'red' else 'c')  
  
            # ... 初始化其他棋子，如车、马、士、相、帅等  
        pass  
      
    def draw(self, screen):  
        # 绘制棋盘到屏幕上  
        screen.blit(self.board_image, self.rect.topleft)  
          
        # 遍历棋盘上的所有格子，并绘制棋子（如果有的话）  
        for i in range(10):  
            for j in range(9):  
                piece = self.grid[i][j]  
                if piece:  
                    # 计算棋子的屏幕位置  
                    x = MARGIN + j * SQUARE_SIZE + SQUARE_SIZE // 2  
                    y = MARGIN + i * SQUARE_SIZE + SQUARE_SIZE // 2  
                    # 绘制棋子（这里假设棋子类有一个draw方法）  
                    piece.draw(screen, (x, y))  
      
    def get_piece_at(self, x, y):  
        # 将屏幕坐标转换为棋盘坐标  
        col = (x - MARGIN) // SQUARE_SIZE  
        row = (y - MARGIN) // SQUARE_SIZE  
          
        # 检查坐标是否在棋盘范围内  
        if 0 <= row < 10 and 0 <= col < 9:  
            return self.grid[row][col]  
        return None  
      
    def move_piece(self, from_x, from_y, to_x, to_y):  
        # 将屏幕坐标转换为棋盘坐标  
        from_col = (from_x - MARGIN) // SQUARE_SIZE  
        from_row = (from_y - MARGIN) // SQUARE_SIZE  
        to_col = (to_x - MARGIN) // SQUARE_SIZE  
        to_row = (to_y - MARGIN) // SQUARE_SIZE  
          
        # 检查移动是否有效（这里只是一个简单的示例，你需要添加实际的移动规则）  
        if self.is_valid_move(from_row, from_col, to_row, to_col):  
            # 执行移动（假设这里只是简单地交换位置）  
            piece = self.grid[from_row][from_col]  
            self.grid[from_row][from_col] = None  
            self.grid[to_row][to_col] = piece  
            # 你可能还需要更新棋子的内部状态，比如位置等  
    
    def is_valid_move(self, move, color):  
        """检查给定的移动是否合法。"""  
        from_x, from_y, to_x, to_y = move  
        piece = self.grid[from_x][from_y]  
  
        # 检查是否有棋子在起始位置  
        if piece is None or piece.color != color:  
            return False  
  
        # 检查目标位置是否为空或者为敌方棋子（吃子）  
        target_piece = self.grid[to_x][to_y]  
        if target_piece is not None and target_piece.color == color:  
            return False  
  
        # 根据棋子的类型检查移动是否合法  
        if isinstance(piece, Soldier):  
            # 卒/兵的移动规则  
            return self.is_valid_soldier_move(from_x, from_y, to_x, to_y)  
        elif isinstance(piece, Horse):  
            # 马的移动规则（日字形）  
            return self.is_valid_horse_move(from_x, from_y, to_x, to_y)  
        # ... 其他棋子的移动规则检查  
  
        return False  # 如果不是已知类型的棋子，则认为移动不合法  
    def is_valid_soldier_move(self, from_x, from_y, to_x, to_y):  
        """检查卒/兵的移动是否合法。"""  
        # 卒/兵通常只能向前移动一格，过河后可以左右移动  
        if from_y == to_y:  # 同一行  
            if abs(from_x - to_x) == 1:  # 左右移动一格  
                # 检查是否过河，过河后才能左右移动  
                if (from_x > 4 and color == 'red') or (from_x < 4 and color == 'black'):  
                    return True  
            elif from_x - to_x == 1 and color == 'red':  # 红方向前移动一格  
                return True  
            elif from_x - to_x == -1 and color == 'black':  # 黑方向前移动一格  
                return True  
        return False  
  
    def is_valid_horse_move(self, from_x, from_y, to_x, to_y):  
        """检查马的移动是否合法（日字形）。"""  
        # 马走日字形，即先横走或竖走一格，再斜走一格  
        if abs(from_x - to_x) == 2 and abs(from_y - to_y) == 1:  
            return self.check_obstacle(from_x, from_y, to_x, to_y, 1, 2) or self.check_obstacle(from_x, from_y, to_x, to_y, 2, 1)  
        elif abs(from_x - to_x) == 1 and abs(from_y - to_y) == 2:  
            return self.check_obstacle(from_x, from_y, to_x, to_y, 1, 2) or self.check_obstacle(from_x, from_y, to_x, to_y, 2, 1)  
        return False  
  
    def check_obstacle(self, from_x, from_y, to_x, to_y, dx1, dy1):  
        """检查马在走日字形时是否有障碍物。"""  
        x1, y1 = from_x + dx1, from_y + dy1  
        return 0 <= x1 < 9 and 0 <= y1 < 10 and self.grid[x1][y1] is None and  0 <= to_x < 9 and 0 <= to_y < 10 and self.grid[to_x][to_y] is None  
    def is_valid_move(self, from_row, from_col, to_row, to_col):  
        # 检查移动是否有效（这里只是一个占位符，你需要根据实际的规则来实现）  
        # 例如，检查目标位置是否为空，或者该棋子是否可以攻击到目标位置等  
        return True  # 总是返回True，这在实际游戏中是不正确的！
    
 