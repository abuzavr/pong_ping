import arcade
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "PONG PING"
BEST_SCORE_FILE = "best_score.txt"


class Ball(arcade.Sprite):
    def __init__(self):
        super().__init__('ball.png', 0.05)
        self.change_x = 10
        self.change_y = 10
        self.moving_down = True  # Флаг для проверки направления движения

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Меняем флаг в зависимости от направления движения
        self.moving_down = self.change_y < 0

        if self.right >= SCREEN_WIDTH or self.left <= 0:
            self.change_x = -self.change_x
        if self.top >= SCREEN_HEIGHT:
            self.change_y = -self.change_y
        if self.bottom <= 0:
            self.change_y = -self.change_y


class Bar(arcade.Sprite):
    def __init__(self):
        super().__init__('platform.png', 0.15)

    def update(self):
        self.center_x += self.change_x
        if self.right >= SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
        if self.left <= 0:
            self.left = 0


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bar = Bar()
        self.ball = Ball()
        self.score = 0
        self.best_score = self.load_best_score()
        self.game_started = False  # Флаг для экрана меню
        self.setup()

    def load_best_score(self):
        if os.path.exists(BEST_SCORE_FILE):
            with open(BEST_SCORE_FILE, 'r') as file:
                return int(file.read())
        return 0

    def save_best_score(self):
        with open(BEST_SCORE_FILE, 'w') as file:
            file.write(str(self.best_score))

    def setup(self):
        self.bar.center_x = SCREEN_WIDTH / 2
        self.bar.center_y = SCREEN_HEIGHT / 10
        self.ball.center_x = SCREEN_WIDTH / 2
        self.ball.center_y = SCREEN_HEIGHT / 2
        self.ball.change_x = 10
        self.ball.change_y = 10
        self.score = 0

    def on_draw(self):
        self.clear((255, 255, 255))
        if self.game_started:
            self.bar.draw()
            self.ball.draw()
            arcade.draw_text(f"СЧЁТ: {self.score}", 10, SCREEN_HEIGHT - 40, arcade.color.BLACK, 20)
            arcade.draw_text(f"ЛУЧШИЙ СЧЁТ: {self.best_score}", 10, SCREEN_HEIGHT - 70, arcade.color.BLACK, 20)
        else:
            # Центрируем текст по экрану
            arcade.draw_text("PONG PING", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
                             arcade.color.BLACK, 40, anchor_x="center")
            arcade.draw_text("НАЖМИТЕ ENTER ДЛЯ СТАРТА", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 20,
                             arcade.color.GRAY, 20, anchor_x="center")

    def update(self, delta):
        if self.game_started:
            # Проверяем столкновение только если мяч движется вниз
            if self.ball.moving_down and arcade.check_for_collision(self.bar, self.ball):
                self.ball.change_y = abs(self.ball.change_y)  # Исправляем направление, чтобы мяч не "залезал" в ракетку
                self.score += 1
                if self.score > self.best_score:
                    self.best_score = self.score
                    self.save_best_score()

            self.ball.update()
            self.bar.update()

            if self.ball.bottom <= 0:  # Мяч касается нижней части экрана — игра окончена
                self.setup()  # Перезапуск игры

    def on_key_press(self, key, modifiers):
        if not self.game_started and key == arcade.key.ENTER:
            self.game_started = True  # Начать игру при нажатии ENTER

        if self.game_started:
            if key == arcade.key.RIGHT:
                self.bar.change_x = 5
            if key == arcade.key.LEFT:
                self.bar.change_x = -5

    def on_key_release(self, key, modifiers):
        if key == arcade.key.RIGHT or key == arcade.key.LEFT:
            self.bar.change_x = 0


if __name__ == '__main__':
    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()
