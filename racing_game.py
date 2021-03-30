import pygame as pg
import random, sys
from time import sleep

WINDOW_WIDTH = 486
WINDOW_HEIGHT = 798

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
RED = (255, 0, 0)

main = pg.image.load('image/main_rg.png')
rect = main.get_rect()
programIcon = pg.image.load('image/PyCar.png')
pg.display.set_icon(programIcon)

class Car:
    car_img = ['image/1.png', 'image/2.png', 'image/3.png', 'image/4.png', 'image/5.png', 'image/6.png', 'image/7.png', 'image/8.png', 'image/9.png', 'image/10.png', 'image/11.png', 'image/12.png', 'image/13.png', 'image/14.png', 'image/15.png', 'image/16.png', 'image/17.png', 'image/18.png', 'image/19.png', 'image/20.png']

    def __init__(self, x=0, y=0, dx=0, dy=0):
        self.image = ""
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def load_image(self):
        self.image = pg.image.load(random.choice(self.car_img))
        self.width = self.image.get_rect().size[0]
        self.height = self.image.get_rect().size[1]

    def draw_img(self):
        screen.blit(self.image, [self.x, self.y])

    def move_x(self):
        self.x += self.dx

    def move_y(self):
        self.y += self.dy

    def check_screen(self):
        if self.x + self.width > WINDOW_WIDTH or self.x < 0:
            self.x -= self.dx

    def check_crash(self, car):
        if (self.x + self.width > car.x) and (self.x < car.x + car.width) and (self.y < car.y + car.height) and (
                self.y + self.height > car.y):
            return True
        else:
            return False

def main_menu():

    draw_x = (WINDOW_WIDTH / 2) - 200
    draw_y = WINDOW_HEIGHT / 2
    font40 = pg.font.SysFont("FixedSys", 40, True, False)
    screen.blit(main, rect)
    score_result = font40.render("Score: " + str(score), True, BLACK)
    screen.blit(score_result, [draw_x+135, draw_y-140])
    pg.display.flip()

def game_over():
    draw_x = (WINDOW_WIDTH / 2) - 200
    draw_y = WINDOW_HEIGHT / 2
    main_img = pg.image.load('image/main_rg.png')
    screen.blit(main_img, [draw_x, draw_y - 280])
    font40 = pg.font.SysFont("FixedSys", 40, True, False)
    font30 = pg.font.SysFont("FixedSys", 30, True, False)
    score_result = font40.render("Score: " + str(score), True, WHITE)
    screen.blit(score_result, [draw_x, draw_y + 70])


def score_view():
    font30 = pg.font.SysFont("FixedSys", 30, True, False)
    score_view = font30.render("Score: " + str(score), True, WHITE)
    screen.blit(score_view, [15, 15])


if __name__ == '__main__':
    pg.init()

    screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(main, rect)
    pg.display.set_caption("RACING GAME")
    clock = pg.time.Clock()

    pg.mixer.music.load('sound/race.wav')
    crash_snd = pg.mixer.Sound('sound/crash.wav')
    engine_snd = pg.mixer.Sound('sound/engine.wav')

    player = Car(WINDOW_WIDTH/2, WINDOW_HEIGHT - 150, 0, 0)
    player.load_image()

    cars = []
    view_car = 3
    for i in range(view_car):
        x = random.randrange(0, WINDOW_WIDTH - 55)
        y = random.randrange(-150, -50)
        car = Car(x, y, 0, random.randint(5, 10))
        car.load_image()
        cars.append(car)

    lanes = []
    lane_width = 10
    lane_height = 80
    lane_margin = 20
    lane_cnt = 20
    lane_x = (WINDOW_WIDTH - lane_width) / 2
    lane_y = -10
    for i in range(lane_cnt):
        lanes.append([lane_x, lane_y])
        lane_y += lane_height + lane_margin

    score = 0
    crash = True
    play_game = True
    while play_game:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                play_game = False
            if crash:
                if event.type == pg.KEYDOWN and event.key == pg.K_KP_ENTER:
                    crash = False
                    for i in range(view_car):
                        cars[i].x = random.randrange(0, WINDOW_WIDTH - cars[i].width)
                        cars[i].y = random.randrange(-150, -50)
                        cars[i].load_image()

                    player.load_image()
                    player.x = WINDOW_WIDTH / 2
                    player.dx = 0
                    score = 0
                    pg.mouse.set_visible(False)
                    engine_snd.play()
                    sleep(3)
                    pg.mixer.music.play(-1)

            if not crash:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RIGHT:
                        player.dx = 4
                    elif event.key == pg.K_LEFT:
                        player.dx = -4

                if event.type == pg.KEYUP:
                    if event.key == pg.K_RIGHT:
                        player.dx = 0
                    elif event.key == pg.K_LEFT:
                        player.dx = 0

        screen.fill(BLACK)

        if not crash:
            for i in range(lane_cnt):
                pg.draw.rect(screen, WHITE, [lanes[i][0], lanes[i][1], lane_width, lane_height])
                lanes[i][1] += 8  # 차선 속도
                if lanes[i][1] > WINDOW_HEIGHT:
                    lanes[i][1] = -40 - lane_height

            player.draw_img()
            player.move_x()
            player.check_screen()

            for i in range(view_car):
                cars[i].draw_img()
                cars[i].y += cars[i].dy
                if cars[i].y > WINDOW_HEIGHT:
                    score += 10
                    cars[i].x = random.randrange(0, WINDOW_WIDTH - cars[i].width)
                    cars[i].y = random.randrange(-150, -50)
                    cars[i].dy = random.randint(5, 10)
                    cars[i].load_image()

            for i in range(view_car):
                if player.check_crash(cars[i]):
                    crash = True
                    pg.mixer.music.stop()
                    crash_snd.play()
                    sleep(2)
                    pg.mouse.set_visible(True)
                    break

            score_view()
            pg.display.flip()
        else:
            main_menu()
        clock.tick(60)
pg.quit()

