from random import choice, randint

import pygame as pg

pg.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 20

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pg.display.set_caption('Змейка')

clock = pg.time.Clock()


def handle_keys(game_object):
    """Обработка действий игрока"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


class GameObject:
    """Создаем базовый класс"""

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self):
        """Заглушка метода рисования"""
        pass


class Snake(GameObject):
    """Описание класса змейка"""

    def __init__(self, body_color=SNAKE_COLOR,
                 position=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))):
        super().__init__(body_color)
        self.length = 1
        self.position = position
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновление позиции змейки"""
        self.head_position = self.get_head_position()
        self.new_head_position = ((self.head_position[0] + self.direction[0]
                                  * GRID_SIZE) % SCREEN_WIDTH,
                                  (self.head_position[1] + self.direction[1]
                                  * GRID_SIZE) % SCREEN_HEIGHT)
        if self.new_head_position in self.positions:
            self.reset()
            return
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.positions.insert(0, self.new_head_position)

    def get_head_position(self):
        """Обновление положения головы змейки"""
        return self.positions[0]

    def reset(self):
        """Сброс змейки в начальное положение"""
        self.length = 1
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, RIGHT, LEFT])

    def draw(self, surface):
        """Отрисовка змейки"""
        for position in self.positions[:-1]:
            rect = (
                pg.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pg.draw.rect(surface, self.body_color, rect)
            pg.draw.rect(surface, BORDER_COLOR, rect, 1)

        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(surface, self.body_color, head_rect)
        pg.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pg.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


class Apple(GameObject):
    """Описание класса яблоко"""

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.position = self.randomize_position()

    def randomize_position(self):
        """Получение случайного местоположения на игровом поле"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )
        return self.position

    def draw(self, surface):
        """Отрисовка яблока"""
        rect = pg.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(surface, self.body_color, rect)
        pg.draw.rect(surface, BORDER_COLOR, rect, 1)


def main():
    """Объявление экземпляров классов и основная логика игры"""
    apple = Apple()
    snake = Snake()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        if snake.get_head_position() == apple.position:
            apple.randomize_position()
            snake.length += 1
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)
        snake.move()
        snake.update_direction()
        pg.display.update()


if __name__ == '__main__':
    main()
