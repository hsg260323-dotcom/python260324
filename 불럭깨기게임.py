import sys
import random
import pygame

# ====== 설정 ======
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

BRICK_ROWS = 6
BRICK_COLS = 10
BRICK_WIDTH = 70
BRICK_HEIGHT = 25
BRICK_GAP = 5
TOP_OFFSET = 60

PADDLE_WIDTH = 110
PADDLE_HEIGHT = 18
PADDLE_SPEED = 8
BALL_RADIUS = 10
BALL_SPEED = 5

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
COLORS = [
    (255, 99, 71),   # tomato
    (60, 179, 113),  # medium sea green
    (70, 130, 180),  # steel blue
    (238, 232, 170), # pale goldenrod
    (218, 112, 214), # orchid
    (255, 215, 0),   # gold
]

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
        self.image.fill(color)
        pygame.draw.rect(self.image, BLACK, (0, 0, BRICK_WIDTH, BRICK_HEIGHT), 2)
        self.rect = self.image.get_rect(topleft=(x, y))

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(WHITE)
        pygame.draw.rect(self.image, BLACK, (0, 0, PADDLE_WIDTH, PADDLE_HEIGHT), 2)
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.speed = 0

    def update(self):
        self.rect.x += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.vel = pygame.Vector2(random.choice((-1, 1)) * BALL_SPEED, -BALL_SPEED)

    def update(self):
        self.rect.x += round(self.vel.x)
        self.rect.y += round(self.vel.y)

        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.vel.x *= -1

        if self.rect.top <= 0:
            self.vel.y *= -1

    def reset(self):
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.vel = pygame.Vector2(random.choice((-1, 1)) * BALL_SPEED, -BALL_SPEED)

class BreakoutGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("파이썬 블럭깨기 게임")
        self.clock = pygame.time.Clock()

        # 한글이 깨지지 않도록 윈도우 기본 한글 폰트 우선 사용
        available_fonts = pygame.font.get_fonts()
        if "malgungothic" in available_fonts:
            self.font = pygame.font.SysFont("malgungothic", 28)
        elif "gulim" in available_fonts:
            self.font = pygame.font.SysFont("gulim", 28)
        else:
            self.font = pygame.font.SysFont(None, 28)

        self.all_sprites = pygame.sprite.Group()
        self.bricks = pygame.sprite.Group()

        self.paddle = Paddle()
        self.ball = Ball()

        self.all_sprites.add(self.paddle, self.ball)
        self._create_bricks()

        self.score = 0
        self.lives = 3
        self.running = True
        self.game_over = False

    def _create_bricks(self):
        for row in range(BRICK_ROWS):
            y = TOP_OFFSET + row * (BRICK_HEIGHT + BRICK_GAP)
            for col in range(BRICK_COLS):
                x = BRICK_GAP + col * (BRICK_WIDTH + BRICK_GAP)
                color = COLORS[row % len(COLORS)]
                brick = Brick(x, y, color)
                self.bricks.add(brick)
                self.all_sprites.add(brick)

    def run(self):
        while self.running:
            self._handle_events()
            if not self.game_over:
                self._update()
                self._check_collisions()
            self._draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    self.paddle.speed = -PADDLE_SPEED
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.paddle.speed = PADDLE_SPEED
                if event.key == pygame.K_SPACE and self.game_over:
                    self._reset_game()

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d):
                    self.paddle.speed = 0

    def _update(self):
        self.all_sprites.update()

    def _check_collisions(self):
        if pygame.sprite.collide_rect(self.ball, self.paddle) and self.ball.vel.y > 0:
            diff = (self.ball.rect.centerx - self.paddle.rect.centerx) / (PADDLE_WIDTH / 2)
            self.ball.vel.x = diff * BALL_SPEED * 1.5
            self.ball.vel.y *= -1

        hit_bricks = pygame.sprite.spritecollide(self.ball, self.bricks, dokill=True)
        if hit_bricks:
            self.score += len(hit_bricks) * 10
            self.ball.vel.y *= -1

        if not self.bricks:
            self.game_over = True

        if self.ball.rect.bottom >= SCREEN_HEIGHT:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                self.ball.reset()

    def _draw_text(self, text, x, y, color=WHITE):
        surf = self.font.render(text, True, color)
        self.screen.blit(surf, (x, y))

    def _draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        self._draw_text(f"점수: {self.score}", 15, 10)
        self._draw_text(f"목숨: {self.lives}", SCREEN_WIDTH - 110, 10)

        if self.game_over:
            if self.bricks:
                msg = "게임 오버! 스페이스로 재시작"
            else:
                msg = "모든 블럭 파괴! 스페이스로 재시작"
            text_surface = self.font.render(msg, True, WHITE)
            rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text_surface, rect)

        pygame.display.flip()

    def _reset_game(self):
        self.bricks.empty()
        self.all_sprites.empty()
        self.paddle = Paddle()
        self.ball = Ball()
        self.all_sprites.add(self.paddle, self.ball)
        self._create_bricks()
        self.score = 0
        self.lives = 3
        self.game_over = False


if __name__ == "__main__":
    game = BreakoutGame()
    game.run()
