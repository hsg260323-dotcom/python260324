#cmd
#pip install pygame

import pygame
import random
from enum import Enum

# 초기화
pygame.init()

# 색상 정의
class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 165, 0)

# 게임 설정
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30
SIDE_PANEL_WIDTH = 150
WINDOW_WIDTH = GRID_WIDTH * BLOCK_SIZE + SIDE_PANEL_WIDTH
WINDOW_HEIGHT = GRID_HEIGHT * BLOCK_SIZE
FPS = 60
FALL_SPEED = 15  # 게임 틱마다 블록이 내려오는 속도

# 테트로미노 블록의 모양 정의
TETROMINOS = {
    'I': {
        'shape': [
            [1, 1, 1, 1]
        ],
        'color': Color.CYAN
    },
    'O': {
        'shape': [
            [1, 1],
            [1, 1]
        ],
        'color': Color.YELLOW
    },
    'T': {
        'shape': [
            [0, 1, 0],
            [1, 1, 1]
        ],
        'color': Color.MAGENTA
    },
    'S': {
        'shape': [
            [0, 1, 1],
            [1, 1, 0]
        ],
        'color': Color.GREEN
    },
    'Z': {
        'shape': [
            [1, 1, 0],
            [0, 1, 1]
        ],
        'color': Color.RED
    },
    'J': {
        'shape': [
            [1, 0, 0],
            [1, 1, 1]
        ],
        'color': Color.BLUE
    },
    'L': {
        'shape': [
            [0, 0, 1],
            [1, 1, 1]
        ],
        'color': Color.ORANGE
    }
}

class Tetromino:
    """테트로미노 블록 클래스"""
    def __init__(self, shape_type):
        self.shape_type = shape_type
        self.shape = [row[:] for row in TETROMINOS[shape_type]['shape']]
        self.color = TETROMINOS[shape_type]['color']
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
    
    def rotate(self):
        """블록을 시계 방향으로 회전"""
        rotated = [[self.shape[y][x] for y in range(len(self.shape))]
                   for x in range(len(self.shape[0]) - 1, -1, -1)]
        self.shape = rotated
    
    def move_left(self):
        """블록을 왼쪽으로 이동"""
        self.x -= 1
    
    def move_right(self):
        """블록을 오른쪽으로 이동"""
        self.x += 1
    
    def move_down(self):
        """블록을 아래로 이동"""
        self.y += 1
    
    def get_blocks(self):
        """블록의 모든 셀 위치 반환"""
        blocks = []
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    blocks.append((self.x + x, self.y + y))
        return blocks

class Game:
    """테트리스 게임 클래스"""
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('테트리스')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_tetromino = Tetromino(random.choice(list(TETROMINOS.keys())))
        self.next_tetromino = Tetromino(random.choice(list(TETROMINOS.keys())))
        self.score = 0
        self.lines = 0
        self.game_over = False
        self.fall_counter = 0
    
    def spawn_new_tetromino(self):
        """새로운 테트로미노 생성"""
        self.current_tetromino = self.next_tetromino
        self.next_tetromino = Tetromino(random.choice(list(TETROMINOS.keys())))
        
        # 충돌 확인 (게임 오버)
        if self.collides():
            self.game_over = True
    
    def collides(self, tetromino=None, offset_x=0, offset_y=0):
        """충돌 검사"""
        if tetromino is None:
            tetromino = self.current_tetromino
        
        for x, y in tetromino.get_blocks():
            new_x = x + offset_x
            new_y = y + offset_y
            
            # 경계 확인
            if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                return True
            
            # 이미 채워진 블록과의 충돌
            if new_y >= 0 and self.grid[new_y][new_x]:
                return True
        
        return False
    
    def place_tetromino(self):
        """현재 테트로미노를 그리드에 배치"""
        for x, y in self.current_tetromino.get_blocks():
            if y >= 0:
                self.grid[y][x] = self.current_tetromino.color
        
        self.clear_lines()
        self.spawn_new_tetromino()
    
    def clear_lines(self):
        """완성된 줄 제거"""
        lines_to_remove = []
        
        for y in range(GRID_HEIGHT):
            if all(self.grid[y]):
                lines_to_remove.append(y)
        
        for y in reversed(lines_to_remove):
            del self.grid[y]
            self.grid.insert(0, [0] * GRID_WIDTH)
        
        if lines_to_remove:
            cleared = len(lines_to_remove)
            self.lines += cleared
            self.score += cleared * 100
    
    def handle_input(self):
        """사용자 입력 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not self.collides(offset_x=-1):
                        self.current_tetromino.move_left()
                
                elif event.key == pygame.K_RIGHT:
                    if not self.collides(offset_x=1):
                        self.current_tetromino.move_right()
                
                elif event.key == pygame.K_DOWN:
                    if not self.collides(offset_y=1):
                        self.current_tetromino.move_down()
                        self.score += 1
                
                elif event.key == pygame.K_UP:
                    # 회전 시도
                    old_shape = self.current_tetromino.shape
                    self.current_tetromino.rotate()
                    
                    if self.collides():
                        # 회전 불가능하면 돌리기 전 상태로 복원
                        self.current_tetromino.shape = old_shape
                
                elif event.key == pygame.K_SPACE:
                    # 하드 드롭
                    while not self.collides(offset_y=1):
                        self.current_tetromino.move_down()
                        self.score += 2
        
        return True
    
    def update(self):
        """게임 상태 업데이트"""
        if self.game_over:
            return
        
        self.fall_counter += 1
        
        if self.fall_counter >= FALL_SPEED:
            self.fall_counter = 0
            
            if self.collides(offset_y=1):
                self.place_tetromino()
            else:
                self.current_tetromino.move_down()
    
    def draw(self):
        """게임 화면 그리기"""
        self.screen.fill(Color.BLACK)
        
        # 그리드 그리기
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, 
                                  BLOCK_SIZE, BLOCK_SIZE)
                
                if self.grid[y][x]:
                    pygame.draw.rect(self.screen, self.grid[y][x], rect)
                
                pygame.draw.rect(self.screen, Color.GRAY, rect, 1)
        
        # 현재 테트로미노 그리기
        if not self.game_over:
            for x, y in self.current_tetromino.get_blocks():
                if y >= 0:
                    rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(self.screen, self.current_tetromino.color, rect)
                    pygame.draw.rect(self.screen, Color.WHITE, rect, 1)
        
        # 사이드 패널 (점수, 다음 블록)
        side_x = GRID_WIDTH * BLOCK_SIZE
        
        # 점수 표시
        score_text = self.font.render(f'점수: {self.score}', True, Color.WHITE)
        self.screen.blit(score_text, (side_x + 10, 20))
        
        # 줄 표시
        lines_text = self.small_font.render(f'줄: {self.lines}', True, Color.WHITE)
        self.screen.blit(lines_text, (side_x + 10, 70))
        
        # 다음 블록 표시
        next_text = self.small_font.render('다음:', True, Color.WHITE)
        self.screen.blit(next_text, (side_x + 10, 120))
        
        for x, y in self.next_tetromino.get_blocks():
            rect = pygame.Rect(side_x + 10 + x * BLOCK_SIZE, 150 + y * BLOCK_SIZE,
                              BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(self.screen, self.next_tetromino.color, rect)
            pygame.draw.rect(self.screen, Color.WHITE, rect, 1)
        
        # 게임 오버 표시
        if self.game_over:
            game_over_text = self.font.render('게임 오버!', True, Color.RED)
            self.screen.blit(game_over_text, (GRID_WIDTH * BLOCK_SIZE // 2 - 50, 
                                             GRID_HEIGHT * BLOCK_SIZE // 2))
        
        pygame.display.flip()
    
    def run(self):
        """게임 루프"""
        running = True
        
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
