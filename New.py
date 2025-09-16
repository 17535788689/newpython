import pygame
import sys

# 初始化
pygame.init()
pygame.font.init()

# 常量定义
BOARD_COLS = 9
BOARD_ROWS = 10
CELL_SIZE = 60
MARGIN = 30
SCREEN_WIDTH = BOARD_COLS * CELL_SIZE + 2 * MARGIN
SCREEN_HEIGHT = BOARD_ROWS * CELL_SIZE + 2 * MARGIN

# 颜色
BOARD_COLOR = (210, 180, 140)
LINE_COLOR = (0, 0, 0)
RED_PIECE_COLOR = (255, 0, 0)
BLACK_PIECE_COLOR = (0, 0, 0)
HIGHLIGHT_COLOR = (255, 255, 0, 100)

# 棋子类型
PIECES = {
    'r_king': '帅', 'r_advisor': '仕', 'r_elephant': '相',
    'r_horse': '马', 'r_chariot': '车', 'r_cannon': '炮', 'r_pawn': '兵',
    'b_king': '将', 'b_advisor': '士', 'b_elephant': '象',
    'b_horse': '马', 'b_chariot': '车', 'b_cannon': '炮', 'b_pawn': '卒'
}


class ChessPiece:
    def __init__(self, type, row, col):
        self.type = type
        self.row = row
        self.col = col
        self.selected = False

    def draw(self, screen):
        color = RED_PIECE_COLOR if self.type.startswith('r_') else BLACK_PIECE_COLOR
        x = MARGIN + self.col * CELL_SIZE
        y = MARGIN + self.row * CELL_SIZE

        if self.selected:
            pygame.draw.circle(screen, HIGHLIGHT_COLOR, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 2 - 5)

        pygame.draw.circle(screen, color, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 3)
        font = pygame.font.SysFont('simhei', 30)
        text = font.render(PIECES[self.type], True, (255, 255, 255))
        screen.blit(text, (x + CELL_SIZE // 2 - 10, y + CELL_SIZE // 2 - 15))


class ChessGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("中国象棋")
        self.board = self.create_board()
        self.selected_piece = None
        self.current_player = 'red'  # 红方先行
        self.game_over = False

    def create_board(self):
        board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        # 初始化红方
        board[0][0] = ChessPiece('r_chariot', 0, 0)
        board[0][1] = ChessPiece('r_horse', 0, 1)
        board[0][2] = ChessPiece('r_elephant', 0, 2)
        board[0][3] = ChessPiece('r_advisor', 0, 3)
        board[0][4] = ChessPiece('r_king', 0, 4)
        board[0][5] = ChessPiece('r_advisor', 0, 5)
        board[0][6] = ChessPiece('r_elephant', 0, 6)
        board[0][7] = ChessPiece('r_horse', 0, 7)
        board[0][8] = ChessPiece('r_chariot', 0, 8)
        board[2][1] = ChessPiece('r_cannon', 2, 1)
        board[2][7] = ChessPiece('r_cannon', 2, 7)
        for i in range(0, 9, 2):
            board[3][i] = ChessPiece('r_pawn', 3, i)

        # 初始化黑方
        board[9][0] = ChessPiece('b_chariot', 9, 0)
        board[9][1] = ChessPiece('b_horse', 9, 1)
        board[9][2] = ChessPiece('b_elephant', 9, 2)
        board[9][3] = ChessPiece('b_advisor', 9, 3)
        board[9][4] = ChessPiece('b_king', 9, 4)
        board[9][5] = ChessPiece('b_advisor', 9, 5)
        board[9][6] = ChessPiece('b_elephant', 9, 6)
        board[9][7] = ChessPiece('b_horse', 9, 7)
        board[9][8] = ChessPiece('b_chariot', 9, 8)
        board[7][1] = ChessPiece('b_cannon', 7, 1)
        board[7][7] = ChessPiece('b_cannon', 7, 7)
        for i in range(0, 9, 2):
            board[6][i] = ChessPiece('b_pawn', 6, i)

        return board

    def draw_board(self):
        self.screen.fill(BOARD_COLOR)
        # 绘制横线
        for row in range(BOARD_ROWS):
            y = MARGIN + row * CELL_SIZE
            pygame.draw.line(self.screen, LINE_COLOR,
                             (MARGIN, y),
                             (MARGIN + (BOARD_COLS - 1) * CELL_SIZE, y), 2)
        # 绘制竖线
        for col in range(BOARD_COLS):
            x = MARGIN + col * CELL_SIZE
            pygame.draw.line(self.screen, LINE_COLOR,
                             (x, MARGIN),
                             (x, MARGIN + (BOARD_ROWS - 1) * CELL_SIZE), 2)

        # 绘制楚河汉界
        font = pygame.font.SysFont('simhei', 40)
        text = font.render("楚河        汉界", True, (0, 0, 0))
        self.screen.blit(text, (MARGIN + CELL_SIZE, MARGIN + 4.5 * CELL_SIZE - 20))

    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col = round((x - MARGIN) / CELL_SIZE)
                    row = round((y - MARGIN) / CELL_SIZE)

                    if 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
                        self.handle_click(row, col)

            self.draw_board()
            self.draw_pieces()
            self.draw_player_turn()
            pygame.display.flip()

    def handle_click(self, row, col):
        piece = self.board[row][col]

        # 如果已经选中棋子，尝试移动
        if self.selected_piece:
            if self.is_valid_move(self.selected_piece, row, col):
                self.move_piece(self.selected_piece, row, col)
                self.selected_piece = None
                self.current_player = 'black' if self.current_player == 'red' else 'red'
            else:
                # 如果点击的是自己的其他棋子，切换选中
                if piece and ((self.current_player == 'red' and piece.type.startswith('r_')) or
                              (self.current_player == 'black' and piece.type.startswith('b_'))):
                    self.selected_piece = piece
                    self.clear_selections()
                    piece.selected = True
                else:
                    self.clear_selections()
                    self.selected_piece = None
        else:
            # 如果没有选中棋子，选中当前点击的棋子
            if piece and ((self.current_player == 'red' and piece.type.startswith('r_')) or
                          (self.current_player == 'black' and piece.type.startswith('b_'))):
                self.selected_piece = piece
                self.clear_selections()
                piece.selected = True

    def is_valid_move(self, piece, target_row, target_col):
        # 简化版移动规则，实际象棋规则更复杂
        if target_row < 0 or target_row >= BOARD_ROWS or target_col < 0 or target_col >= BOARD_COLS:
            return False

        target_piece = self.board[target_row][target_col]
        if target_piece and ((piece.type.startswith('r_') and target_piece.type.startswith('r_')) or
                             (piece.type.startswith('b_') and target_piece.type.startswith('b_'))):
            return False

        # 这里应该实现各种棋子的具体移动规则
        # 简化版只允许移动一格
        return abs(piece.row - target_row) <= 1 and abs(piece.col - target_col) <= 1

    def move_piece(self, piece, target_row, target_col):
        self.board[piece.row][piece.col] = None
        piece.row = target_row
        piece.col = target_col
        self.board[target_row][target_col] = piece
        piece.selected = False

        # 检查是否将死
        if self.board[target_row][target_col] and (
                (self.current_player == 'red' and self.board[target_row][target_col].type == 'b_king') or
                (self.current_player == 'black' and self.board[target_row][target_col].type == 'r_king')):
            self.game_over = True
            print(f"{self.current_player} wins!")

    def clear_selections(self):
        for row in self.board:
            for piece in row:
                if piece:
                    piece.selected = False

    def draw_pieces(self):
        for row in self.board:
            for piece in row:
                if piece:
                    piece.draw(self.screen)

    def draw_player_turn(self):
        font = pygame.font.SysFont('simhei', 24)
        text = font.render(f"当前回合: {'红方' if self.current_player == 'red' else '黑方'}", True, (0, 0, 0))
        self.screen.blit(text, (MARGIN, 10))


if __name__ == "__main__":
    game = ChessGame()
    game.run()
